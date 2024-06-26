"""
Django settings for Car_Renting_System project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%f3z_ue)bvn^40%2s$aklvq!gktn!6f(h-w311^jx$%s37j%x2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# CSRF_COOKIE_SECURE = False 
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.humanize",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    "allauth_ui",
    'core',
    'userauths',
    'users',
    'cars',
    'rent',
    'ckeditor',
    'django_filters',
    "django_htmx",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

LOGIN_REDIRECT_URL = '/'

SITE_ID = 1

AUTH_USER_MODEL = 'userauths.User'

ROOT_URLCONF = 'Car_Renting_System.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'core.context_processors.default',
                'users.context_processors.default',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'Car_Renting_System.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db_new.sqlite3',
#     }
# }

# DATABASES = {

#     'default': {

#         'ENGINE': 'django.db.backends.postgresql_psycopg2',

#         'NAME': 'DaisyRoom Django',

#         'USER': 'postgres',

#         'PASSWORD': 'hangon1@',

#         'HOST': 'localhost',

#         'PORT': '5432',

#     }

# }

# internal database
# DATABASES = {
#    'default': dj_database_url.parse("postgres://daisyroom:ycpwnaJ0auuMwYhYohchY1GNA8igV8wg@dpg-co3foagl5elc73dcm990-a/daisyroom_18o3") 
# }

# external database
DATABASES = {
    'default': dj_database_url.parse("postgres://daisyroom:ycpwnaJ0auuMwYhYohchY1GNA8igV8wg@dpg-co3foagl5elc73dcm990-a.singapore-postgres.render.com/daisyroom_18o3") 
}
# DATABASES = {

#     'default': {

#         'ENGINE': 'django.db.backends.postgresql_psycopg2',

#         'NAME': os.environ.get('SQL_NAME'),

#         'USER': os.environ.get('SQL_USER'),

#         'PASSWORD': os.environ.get('SQL_PASSWORD'),

#         'HOST': os.environ.get('HOST'),

#         'PORT': os.environ.get('PORT'),

#     }

# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static')
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = '/DaisyRoom/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'DaisyRoom')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'userauths.User'

CKEDITOR_UPLOAD_PATH = 'DaisyRoom/uploads/contents/'

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'codeSnippet_theme': 'monokai',
        'toolbar': 'all',
        'extraPlugins': ','.join(
            [
                'codesnippet',
                'widget',
                'dialog',
            ]
        ),
        'height': 300,
        'width': '120%',
    }
}

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True 
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587 
EMAIL_HOST_USER = 'shaheer.mudassar13@gmail.com'  
EMAIL_HOST_PASSWORD = "zxgttnzevzbflmdw" 
EMAIL_USE_TLS = True 
DEFAULT_FROM_EMAIL = 'DaisyRoom<noreply@daisyroom.com>'

# Google Authentication
# client_id = 717710135674-metvdkoncj0uvekh65rlarct12r82re2.apps.googleusercontent.com
# client_secret = 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

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        
        'OAUTH_PKCE_ENABLED': True,
    }
}

JAZZMIN_SETTINGS = {
    "site_title": "DaisyRoom Admin",
    "login_logo": None,
    "site_logo": "images/admin-logo.png",
    "copyright": "DaisyRoom Ltd",
    "search_model": "cars.Car",
    "show_ui_builder": True,
    "site_brand": "DaisyRoom Admin",
    "welcome_sign": "Welcome to DaisyRoom Admin",
    "custom_links": {
        "core": [{
            "name": "Ownerboard", 
            "url": "ownerboard", 
            "icon": "fas fa-user",
        }]
    },
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dy74qr0ho',
    'API_KEY': '181326364429617',
    'API_SECRET': 'rSqFkGorD1jJld8vqgzc80aHLeg'
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
