"""
Django settings for Realtor project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_qj2#%-o6_kkye*ojv@x_r)(t62ns_6ozbVzskd@r#l5y2(e!_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'www.dpr.sale', 'dpr.sale', 'localhost', 'dev.dpr.sale']

INTERNAL_IPS = ['127.0.0.1', '165.227.163.99']
# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',
	'django_filters',
	'easy_thumbnails',
	'filer',
	'mptt',
	'debug_toolbar',
	'Main.apps.MainConfig',
	'API.apps.ApiConfig',
	'corsheaders',
	# 'allauth',
	# 'allauth.account',
	# 'allauth.socialaccount',
	'watermarker',
	'rest_framework',
]

WATERMARK_QUALITY = 95
WATERMARK_OBSCURE_ORIGINAL = False
WATERMARK_RANDOM_POSITION_ONCE = False

REST_FRAMEWORK = {
	'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

# Allauth config
SITE_ID = 2

# Email config
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'noreply@dpr.sale'
EMAIL_HOST_PASSWORD = 'restservice'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = True

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',

]

if DEBUG:
	DEBUG_TOOLBAR_PANELS = [
		'debug_toolbar.panels.versions.VersionsPanel',
		'debug_toolbar.panels.timer.TimerPanel',
		'debug_toolbar.panels.settings.SettingsPanel',
		'debug_toolbar.panels.headers.HeadersPanel',
		'debug_toolbar.panels.request.RequestPanel',
		'debug_toolbar.panels.sql.SQLPanel',
		'debug_toolbar.panels.staticfiles.StaticFilesPanel',
		'debug_toolbar.panels.templates.TemplatesPanel',
		'debug_toolbar.panels.signals.SignalsPanel',
		'debug_toolbar.panels.logging.LoggingPanel',
		'debug_toolbar.panels.redirects.RedirectsPanel',
		'debug_toolbar.panels.profiling.ProfilingPanel',
		'debug_toolbar.panels.cache.CachePanel'
	]
CSRF_COOKIE_SECURE = False
if DEBUG:
	CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'Realtor.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates'
		,
		'DIRS': [os.path.join(BASE_DIR, 'templates')]
		,
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

WSGI_APPLICATION = 'Realtor.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'dpr.sale',
		'USER': 'django',
		'PASSWORD': 'e1c9fd84a6eee9da02c3aacd9c7390a4',
		'HOST': '165.227.163.99',
		'PORT': '5432',
		'CONN_MAX_AGE': None,
	}
}

CACHES = {
	# 'default': {
	#     'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
	#     'LOCATION': '127.0.0.1:8000',
	# },

	# "default": {
	#     "BACKEND": "django_redis.cache.RedisCache",
	#     "LOCATION": [(os.environ['REDIS_HOST'], 6379)],
	#     "OPTIONS": {
	#         "CLIENT_CLASS": "django_redis.client.DefaultClient"
	#     },
	#     "KEY_PREFIX": "fastoran"
	# }
	'default': {
		'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
		'LOCATION': 'realtor_cache',
	}
}
CACHE_TTL = 60 * 5

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATIC_URL = '/api/static/'

# STATICFILES_DIRS = [
# 	os.path.join(BASE_DIR, 'static'),
# ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

FILER_STORAGES = {
	'public': {
		'main': {
			'ENGINE': 'filer.storage.PublicFileSystemStorage',
			'OPTIONS': {
				'location': os.path.join(BASE_DIR, 'uploads/img'),
				'base_url': '/uploads/img/',
			},
			'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
			'UPLOAD_TO_PREFIX': '',
		},

	}
}
