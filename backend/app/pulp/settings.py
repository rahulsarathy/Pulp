import os, sys
from celery.schedules import crontab
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

FIELD_ENCRYPTION_KEY=os.environ.get('FIELD_ENCRYPTION_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'health_check',                             # required
    'health_check.db',                          # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    # 'health_check.contrib.celery',              # requires celery
    'health_check.contrib.redis',               # required Redis broker
    'captcha',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',  # new
    'allauth.account',  # new
    # 'allauth.socialaccount',
    'corsheaders',
    'rest_framework',
    'progress',
    'reading_list.apps.ReadingListConfig',
    'payments.apps.PaymentsConfig',
    'users.apps.UsersConfig',
    'blogs.apps.BlogsConfig',
    'instapaper.apps.InstapaperConfig',
    'twitter.apps.TwitterConfig',
    'pocket.apps.PocketConfig',
    'articles.apps.ArticlesConfig',
    'coverage',
    'django_celery_beat',
    'encrypted_model_fields',
    'django_nose',
    'django_extensions',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# we whitelist localhost:3000 because that's where frontend will be served
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
)

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

ROOT_URLCONF = 'pulp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    	'DIRS': [os.path.join(BASE_DIR, './templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Celery
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_DEFAULT_QUEUE = "default"
CELERY_BEAT_SCHEDULE = {
    'sync_instapaper': {
        'task': 'sync_instapaper',
        'schedule': crontab(minute=0, hour=0),
    },
    'sync_pocket': {
        'task': 'sync_pocket',
        'schedule': crontab(minute=0, hour=0),
    },
    # run every 5 minutes
    'update_timelines': {
        'task': 'update_timelines',
        'schedule': crontab(minute='*/5')
    }
}

WSGI_APPLICATION = 'pulp.wsgi.application'

# Database
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.AllauthSignupForm'
# ACCOUNT_FORMS = {'signup': 'users.forms.MyCustomSignupForm'}
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

# emaillogin_project/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
ACCOUNT_CONFIRM_EMAIL_ON_GET = os.environ.get('ACCOUNT_CONFIRM_EMAIL_ON_GET')
ACCOUNT_EMAIL_VERIFICATION = os.environ.get('ACCOUNT_EMAIL_VERIFICATION', 'optional')
DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_HOST_USER")
LOGIN_URL = '/accounts/login'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Recaptcha
RECAPTCHA_USE_SSL = True     # Defaults to False

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
SECURE_REDIRECT_EXEMPT = ('ready/',)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

PUPPETEER_HOST = os.environ.get('PUPPETEER_HOST')
PARSER_HOST = os.environ.get('PARSER_HOST')
FRONTEND_HOST = os.environ.get('FRONTEND_HOST', '')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{REDIS_HOST}:{REDIS_PORT}/0".format(REDIS_HOST=os.environ.get('REDIS_HOST'),
                                                                 REDIS_PORT=os.environ.get('REDIS_PORT')),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Channels
ASGI_APPLICATION = 'pulp.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('REDIS_HOST'), os.environ.get('REDIS_PORT'))],
            "capacity": 350,
            "expiry": 10,
        },
    },
}

REDIS_URL = "redis://{REDIS_HOST}:{REDIS_PORT}/0".format(REDIS_HOST=os.environ.get('REDIS_HOST'),
                                                                 REDIS_PORT=os.environ.get('REDIS_PORT'))

SILENCED_SYSTEM_CHECKS = config('SILENCED_SYSTEM_CHECKS', cast=Csv())
CELERY_BROKER_URL = "redis://{REDIS_HOST}:{REDIS_PORT}/0".format(REDIS_HOST=os.environ.get('REDIS_HOST'),
                                                                 REDIS_PORT=os.environ.get('REDIS_PORT'))
CELERY_RESULT_BACKEND = "redis://{REDIS_HOST}:{REDIS_PORT}/0".format(REDIS_HOST=os.environ.get('REDIS_HOST'),
                                                                 REDIS_PORT=os.environ.get('REDIS_PORT'))

HEALTHCHECK_CELERY_TIMEOUT = os.environ.get('HEALTHCHECK_CELERY_TIMEOUT')
