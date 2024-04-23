"""
Django settings for django_settings project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#_iipqp#$vxjow&$u8*=ha0w-1$ydn1_&)ea#6m1gcnxc@m@-_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.46']
# CORS_ORIGIN_WHITELIST = ('*')
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_ALL_ORIGINS = False


CORS_ALLOWED_ORIGINS = [
    # "https://example.com",
    # "https://sub.example.com",   
    # "exp://localhost:8081",
    # "http://localhost:8000",
    # "http://localhost:3000",   
    # "http://localhost:8081",
    # "http://192.168.1.46:8081",
    # "http://127.0.0.1:8081",
    # "http://127.0.0.1:8000",
    # "http://127.0.0.1:3000",
    # "exp://192.168.1.46:8081",
    # "http://192.168.1.46:8081",
    # "http://127.0.0.1:8081",
    # "http://localhost:19001",
    # "http://127.0.0.1:19001",
    # "http://192.168.1.46:19001",
    

     'http://localhost:8000',
    'http://localhost:8081',
    "http://127.0.0.1:8081",
    'http://localhost:3000',
    
    
    
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://localhost:8081',
    "http://127.0.0.1:8081",
    'http://localhost:3000',
   
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:8081',
    "http://127.0.0.1:8081",
    'http://localhost:3000',
  
]




# AUTH_USER_MODEL = 'django_app.User'

# Application definition


#jwt token
REST_FRAMEWORK = {
 
    'DEFAULT_AUTHENTICATION_CLASSES': (
      
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
   
}

INSTALLED_APPS = [
    'rest_framework_simplejwt',    
   
    'grappelli',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
      
    'rest_framework',
    'corsheaders',
    'django_app', 
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend/build'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',  

                'django.template.context_processors.request', 
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        #'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


WSGI_APPLICATION = 'django_settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database/db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Etc/GMT-6'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
# STATIC_ROOT = 'static'
STATICFILES_DIRS = [
    'static_external',
    # 'frontend/build/static',
    # 'public/build/static',
    'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# CORS_ALLOW_HEADERS = (
#     "accept",
#     "authorization",
#     "content-type",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# )
# 
# CORS_ALLOW_HEADERS = ('content-disposition', 'accept-encoding',
#                       'content-type', 'accept', 'origin', 'Authorization',
#                       'access-control-allow-methods')
# CORS_ALLOW_CREDENTIALS = True
# CSRF_COOKIE_SECURE = False, 
# CORS_ORIGIN_ALLOW_ALL = True