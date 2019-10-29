from blogs.models import Blog, Article, ReadingListItem
import json
from rest_framework import serializers

class BlogSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    about = serializers.CharField(max_length=256)
    about_link = serializers.CharField(max_length=256)
    authors = serializers.ListField(
        child=serializers.JSONField()
    )
    recent_posts = serializers.ListField(
        child=serializers.JSONField()
    )
    image = serializers.CharField(max_length=256)
    categories = serializers.ListField(
        child=serializers.CharField(max_length=256)
    )

    class Meta:
        model = Blog
        fields = ['name']

    def create(self, validated_data):
        return Blog(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class ArticleSerializer(serializers.ModelSerializer):
    blog_name = serializers.ReadOnlyField(source='blog.name')
    class Meta:
        model = Article
        fields = ['title', 'permalink', 'date_published', 'author', 'blog_name']



class ReadingListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingListItem
        fields = ['title', 'link', 'date_added']
