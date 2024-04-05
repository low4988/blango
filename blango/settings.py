"""
Django settings for blango project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from configurations import Configuration
from configurations import values
import dj_database_url
# for JWT token
from datetime import timedelta

class Dev(Configuration):


    # for JWT token, 
    SIMPLE_JWT = {
        # only while testing, normal access5min refresh1 day
        "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    }
    
    # User two-step user activation, debug sends activation link to terminal
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    # User Registaration allowed while REGISTRATION_OPEN = True
    REGISTRATION_OPEN = True
    # User two-step user activation time limit for verification email-link
    # Without activation, users registered but not activated
    ACCOUNT_ACTIVATION_DAYS = 7
    
    LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Enable media saving and serving. 
    # MEDIA_ROOT, which defines where uploaded files are saved.
    MEDIA_ROOT = BASE_DIR / "media"
    # URL/path to serve media from, needent match
    MEDIA_URL = "/media/"

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-+sn%dpa!086+g+%44z9*^j^q-u4n!j(#wl)x9a%_1op@zz2+1-'

    # SECURITY WARNING: don't run with debug turned on in production!
    #DEBUG = True
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = ['*']
    X_FRAME_OPTIONS = 'ALLOW-FROM ' + os.environ.get('CODIO_HOSTNAME') + '-8000.codio.io'
    CSRF_COOKIE_SAMESITE = None
    CSRF_TRUSTED_ORIGINS = [os.environ.get('CODIO_HOSTNAME') + '-8000.codio.io']
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SAMESITE = 'None'

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
    CRISPY_TEMPLATE_PACK = "bootstrap5"

    ''' Django allauth
    Next we need to add a setting so the Django knows which 
    Site object our settings file applies to. 
    Django will automatically create one when we next migrate, 
    and we'll only use this single Site object in Blango. 
    The site will have the ID 1 so we need to add this setting:
    '''
    SITE_ID = 1

    ''' Django allauth
    Normally when Django Allauth creates a User object 
    from a social account login, it will generate it a username 
    based on the user ID at the third party. 
    Since our custom User model doesn't have a username field, 
    Django Allauth will fail, unless we make some settings changes.
    '''
    # There is no username field on the User model.
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    # The third-party provider must provide an email address when authenticating.
    ACCOUNT_EMAIL_REQUIRED = True
    # The username of the User is not required.
    ACCOUNT_USERNAME_REQUIRED = False
    # The user authenticates by entering their email address.
    ACCOUNT_AUTHENTICATION_METHOD = "email"


    # Application definition
    # 'blango_auth', # for custom user model before 
    # django.contrib.admin in the INSTALLED_APPS setting.
    # else same logout page, Django will load the Admin apps's templates as they have the same name. 
    # Moving blango_auth earlier in the list gives it precedence.

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        # Django Allauth Setup, after 'django.contrib.messages',
        'django.contrib.sites', 
        'django.contrib.staticfiles',
        'blog',
        'crispy_forms',
        'crispy_bootstrap5',
        'blango_auth', # for custom user model, moved here to give 
        'debug_toolbar', #for DjDT
        # Django Allauth Setup, at end, The first three are required
        'allauth', 
        'allauth.account', 
        'allauth.socialaccount', 
        # then you’ll add the provider modules that you’re using for authentication. 
        # For Blango, it’s just Google,
        #'allauth.socialaccount.providers.google' # stopped working middle REST API serialisers
        
        'rest_framework', # for REST API, serializers
        'rest_framework.authtoken', # for REST API, authenticating with token
        # DRF swagger yet another swagger generator
        'drf_yasg',
        # Django filters, available in page 
        'django_filters',
        # versatileimagefield, replaces standard imagefield 
        'versatileimagefield',
        
    ]
    # Swagger settings
    SWAGGER_SETTINGS = {
        "SECURITY_DEFINITIONS": {
            "Token": {"type": "apiKey", "name": "Authorization", "in": "header"},
            "Basic": {"type": "basic"},
        }
    }
    # REST FRAMEWORK settings
    REST_FRAMEWORK = {
      # JWT JSON WebTtoken 
      "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.BasicAuthentication",
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.TokenAuthentication",
            "rest_framework_simplejwt.authentication.JWTAuthentication"
      ],


      "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
      ],
    
      "DEFAULT_THROTTLE_CLASSES": [
            "blog.api.throttling.AnonSustainedThrottle",
            "blog.api.throttling.AnonBurstThrottle",
            "blog.api.throttling.UserSustainedThrottle",
            "blog.api.throttling.UserBurstThrottle",
        ],
        
      "DEFAULT_THROTTLE_RATES": {
            "anon_sustained": "500/day",
            "anon_burst": "10/minute",
            "user_sustained": "5000/day",
            "user_burst": "100/minute",
        },
      "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 100, 
      
      "DEFAULT_FILTER_BACKENDS": [
            "django_filters.rest_framework.DjangoFilterBackend",
            "rest_framework.filters.OrderingFilter"

        ],         
    }
    '''
    # CSRF stands for cross-site request forgery, 
    #which is a way for a malicious actor to force a user to perform an unintended action.
    Reminder: these changes only apply to working with Django on Codio. 
    Do not make these changes to a project you plan on making available on the internet.
    '''
    '''
    The official Django Debug Toolbar configuration guide gives the 
    following warning:
    The order of MIDDLEWARE is important. 
    You should include the Debug Toolbar middleware as early as possible in the list. 
    However, it must come after any other middleware that encodes 
    the response's content, such as GZipMiddleware.

    '''
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware", # for DjDT
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
    #   'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    #   'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    # use get_ip() view to return current IP-in-venv, run server root/ip 
    INTERNAL_IPS = ["192.168.10.156"] # update as needed

    ROOT_URLCONF = 'blango.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'], # default for all templates
            'APP_DIRS': True, # automatically find templates in templates/<app>/ dir
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

    WSGI_APPLICATION = 'blango.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
    ''' # default setting, empty
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    '''
    '''
    The last Value class that we're going to look at is DatabaseURLValue, 
    which parses a database URL: 
    mysql://username:password@mysql-host.example.com:3306/db_name?option1=value1&option2=value2
     -> into a dictionary for Django's DATABASES setting.
    
    # Two nested dictionaries, 
    DATABASES for all possibe setups, 

    actual settings by setting key/name
    'default' is the default db
    'alternative' allows for other option, e.g PostgreSQL - postgres://
    'alternative2' allows for other option, e.g MySQL - mssql://

    DatabaseURLValue parses the URL into a dictionary 
    and populates the 'default' key.
    so it's not possible to handle multiple databases,  with DatabaseURLValue

    Notice that we don't need username, password, and host for SQLLite. 
    Also notice that there are 3 slashes after the schema: 
    this indicates the empty hostname.
    DATABASES = values.DatabaseURLValue(f"sqlite:///{BASE_DIR}/db.sqlite3")

    To use multiple databases, we need to drop down into the lower level 
    dj_database_url library and make use of its 
    config() function. 
    dj_database_url.config() # returns lower level dict ONLY to be nested in DATABASES

    dj_database_url.config() similar to DatabaseURLValue(single DB) in that you can provide a 
    default, but it returns the database config dictionary ONLY
    rather than the enclosing dictionary for DATABASES.

    default-key dictionary looks in enviroment variable DATABASES_URL
    alternative-key , has a named enviroment variable, 
    first arg "ALTERNATIVE_DATABASE_URL",

    default     - DATABASES_URL - alias -default- has special significance
      - used when no other database has been selected, must be specified, but can be empty
    alternative - "ALTERNATIVE_DATABASE_URL" (passed in as arg) 

    Django allows you to work with different databases for different models. 
    '''
    DATABASES = {
      "default"    : dj_database_url.config(
        default=f"sqlite:///{BASE_DIR}/db.sqlite3"),

      "alternative": dj_database_url.config(
          "ALTERNATIVE_DATABASE_URL",
          default=f"sqlite:///{BASE_DIR}/alternative_db.sqlite3",
      ),
    }

    # Custom user model, and  INSTALLED_APPS += 'blango_auth'
    AUTH_USER_MODEL = "blango_auth.User"

    # All allowed hashes, deafult at top (Argon2) 
    PASSWORD_HASHERS = [
      'django.contrib.auth.hashers.Argon2PasswordHasher',
      'django.contrib.auth.hashers.PBKDF2PasswordHasher',
      'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
      'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    ]


    # Password validation
    # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/3.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    #TIME_ZONE = 'UTC'
    #TIME_ZONE = values.Value("UTC", environ_prefix="BLANGO")
    TIME_ZONE = values.Value("UTC")

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/

    STATIC_URL = '/static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



class Prod(Dev):
    # inherit all settings from values. class in parent
    # then able to use simple settings like DEBUG = False, as parent handles boolean coversion
    DEBUG = False

    # never set hardcoded value SECRET_KEY, inherit from development key
    # setting with SecretValue('hardcoded') will raise exepiton when using SecretValue class
    SECRET_KEY = values.SecretValue() 
