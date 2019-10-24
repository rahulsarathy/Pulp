from fpdf import FPDF, HTMLMixin
from django.core.management.base import BaseCommand
from blogs.models import Article, Blog, BlogBlock
from magazine.html_template import template
from users.models import CustomUser as User
from utils.blog_utils import BLOGS
from datetime import datetime
import os
from utils.s3_utils import download_link
import utils.s3_utils as s3_utils
from bs4 import BeautifulSoup
from shutil import copyfile, rmtree, copytree
from blogs.serializers import BlogSerializer
import PyPDF2

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.create_magazines()

    # def add_arguments(self, parser):
    #     parser.add_argument('date_start', nargs='+', type=str)

    def create_magazines(self):
        for blog in BLOGS:
            create_block(blog)
        # for each blog create a magazine block of articles from start date to end date
        # for each user add that block in to their magazine

def create_block(blog):
    blog = blog()
    blog_name = blog.name_id
    blog_orm = Blog.objects.get(name=blog_name)

    current_time = datetime.now()
    start_date = current_time.replace(day=1)
    end_date = current_time.replace(month=current_time.month + 1)
    start_date_string = start_date.strftime('%Y-%m-%d')
    end_date_string = end_date.strftime('%Y-%m-%d')

    articles = Article.objects.filter(blog=blog_orm).filter(date_published__range=[start_date_string, end_date_string])

    for article in articles:
        author = article.author
        title = article.title

        # https://s3.console.aws.amazon.com/s3/object/pulpscrapedarticles/bryan_caplan_econlib/-3232436894135216712.html
        s3_url = article.file_link
        # bryan_caplan_econlib/file_name.html
        s3_file_path = s3_url.split('pulpscrapedarticles/')[1]
        # contains the file path
        s3_file_path_split = s3_file_path.split('/')
        # bryan_caplan_econlib
        s3_file_path_trunc = s3_file_path_split[0]
        # file_name.html
        s3_file = s3_file_path_split[1]
        no_extension = s3_file.split('.')[0]
        # dump/download/bryan_caplan_econlib/
        download_path = os.path.join('dump', 'downloads', s3_file_path_trunc)
        # dump/download/bryan_caplan_econlib/file_name.html
        download_file_path = os.path.join(download_path, s3_file)
        os.makedirs(download_path, exist_ok=True)

        download_link(s3_file_path, download_file_path)

        # magazine/blog_templates/bryan_caplan_econlib/
        template_path = os.path.join('magazine', 'blog_templates', blog_name)
        template_file_path = os.path.join(template_path, '{}.html'.format(blog_name))
        final_path = os.path.join('dump', 'pdf', blog_name)
        final_file_path = os.path.join(final_path, '{}.pdf'.format(no_extension))
        os.makedirs(final_path, exist_ok=True)

        blog_soup = BeautifulSoup(open(download_file_path))
        #grab template for blog
        soup = BeautifulSoup(open(template_file_path), "html.parser",)

        #inject html into template
        title_tag = soup.find('div', attrs={"class": "blog-title"})
        author_tag = soup.find('div', attrs={"class": "author"})
        article_tag = soup.find('div', attrs={"class": "blog-post"})
        title_tag.string = title
        author_tag.string = author
        # article_tag.string = blog_soup
        article_tag.insert(0, blog_soup)

        staging_path = os.path.join('dump', 'pdf', s3_file)
        print("input file is {}".format(staging_path))
        css_path = os.path.join(template_path, '{}.css'.format(blog_name))
        staging_path_css = os.path.join('dump', 'pdf', '{}.css'.format(blog_name))
        copyfile(css_path, staging_path_css)
        f = open(staging_path, 'w')
        f.write(str(soup))
        f.close()

        #run princexml on downloaded path (/pdf)
        cmd = 'prince {inputpath} -o {outputpath}'.format(inputpath=staging_path, outputpath=final_file_path)
        os.system(cmd)
        print(final_file_path)
        with open(final_file_path, 'rb') as pdf_obj:
            pdf = PyPDF2.PdfFileReader(pdf_obj)
            out = PyPDF2.PdfFileWriter()
            for page in range(pdf.getNumPages()):
                page = pdf.getPage(page)
                out.addPage(page)
            with open(final_file_path, 'wb') as f:
                out.removeLinks()
                out.write(f)

        upload_pdf(final_file_path, article, blog_name)

def upload_pdf(src_path, article, blog_name):

    old_pdf_link = None
    if article.pdf_link:
        old_pdf_link = article.pdf_link

    article_id = hash(article)
    s3_path = os.path.join(blog_name, '{}.pdf'.format(article_id))
    s3_utils.put_object('pulppdfs', s3_path, src_path)
    new_url = s3_utils.create_pdf_url('pulppdfs', blog_name, article_id)
    article.pdf_link = new_url
    article.save()

    if old_pdf_link:
        path = old_pdf_link.split('pulppdfs/')[1]
        s3_utils.delete_file('pulppdfs', path)

    # join all the pdfs
    # store final pdf in s3