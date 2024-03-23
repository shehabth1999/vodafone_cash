""" Django 4.1.1. """
# region Imports
from pathlib import Path
import os,datetime,sys
# endregion 

# region Networking
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-#2+kf%!ig^*rfz4p@%ox+ir)e&aqnil6%nrj%9hb1du)8u=z!d'
DEBUG = True
ALLOWED_HOSTS = ['soleilacademy.herokuapp.com','127.0.0.1']
INTERNAL_IPS = [ '127.0.0.1',]
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'
SITE_ID = 1
AUTH_USER_MODEL = 'authentication.User'
#CORS_ALLOW_ALL_ORIGINS= True
# endregion Networking

# region Internationalization
LANGUAGE_CODE   = 'en-us'               # 'ar'
TIME_ZONE       = 'Africa/Cairo'        #'UTC'
USE_I18N        = True
USE_L10N        = True
USE_TZ          = True
LANGUAGES       = (  ('en', 'English'),  ('ar', 'عربى'),  )
#DATETIME_FORMAT = '%Y-%m-%d %H:%m'
# endregion Internationalization

# region Static files
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760 # 10mb = 10 * 1024 *1024
STATIC_URL = '/static/'
MEDIA_URL = '/images/'
MEDIA_ROOT = 'static/images'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STSTICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# endregion Static files

# region Email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# endregion Email

# region API Settings
REST_FRAMEWORK = {
    # handel errors
    'NON_FIELD_ERRORS_KEY': 'error',
    'EXCEPTION_HANDLER': 'core.utils.exceptions.custom_exception_handler',


    # pagination
    'PAGE_SIZE':100,
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    
    # Default Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),

    # Default Permission
    'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
    
    # Default Filter
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=1),
#     'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
# }

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# endregion API Settings

# region APPS
INSTALLED_APPS = [
    # 'jazzmin',
    'jet.dashboard',
    'jet',



    # Builtin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Utils
    'django_extensions',
    'drf_yasg',
    'debug_toolbar',
    'django_seed',
    'django_filters',
    'corsheaders',
    # API Utils
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework.authtoken',

    # Apps
    'authentication',
    'social_auth',
    'institution',
    'vcash.apps.VcashConfig',
    'customers.apps.CustomersConfig',
]
# endregion APPS




# region JET Settings 
JET_THEMES = [
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]
JET_SIDE_MENU_COMPACT = False #  will list applications and models in the side menu without need to move pointer over applications to show models.
# endregion JET Settings
"""
JET_SIDE_MENU_ITEMS = {
    'admin': [
        {'label': _('General'), 'app_label': 'core', 'items': [
            {'name': 'help.question'},
            {'name': 'pages.page'},
            {'name': 'city'},
            {'name': 'validationcode'},
        ]},
        ...
    ],
    'custom_admin': [
        {'app_label': 'talks', 'items': [
            {'name': 'talk'},
            {'name': 'talkmessage'},
        ]},
        ...
    ]
}

JET_SIDE_MENU_CUSTOM_APPS = [
    ('core', [ # Each list element is a tuple with application name (app_label) and list of models
        'User',
        'MenuItem',
        'Block',
    ]),
    ('shops', [
        'Shop',
        'City',
        'MetroStation',
    ]),
    ('feedback', [
        'Feedback',
    ]),
]

JET_SIDE_MENU_ITEMS = [  # A list of application or custom item dicts
    {'label': _('General'), 'app_label': 'core', 'items': [
        {'name': 'help.question'},
        {'name': 'pages.page', 'label': _('Static page')},
        {'name': 'city'},
        {'name': 'validationcode'},
        {'label': _('Analytics'), 'url': 'http://example.com', 'url_blank': True},
    ]},
    {'label': _('Users'), 'items': [
        {'name': 'core.user'},
        {'name': 'auth.group'},
        {'name': 'core.userprofile', 'permissions': ['core.user']},
    ]},
    {'app_label': 'banners', 'items': [
        {'name': 'banner'},
        {'name': 'bannertype'},
    ]},
]
"""

# region Security
AUTHENTICATION_BACKENDS = ( 
    'django.contrib.auth.backends.AllowAllUsersModelBackend', 
    # 'authentication.backends.CaseInsensitiveModelBackend',
    )
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]
# endregion Security

# region WEB

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Added
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]
# endregion WEB

# region Database
# DB_NAME         = "d2a6pcr8617jdq"
# DB_USER         = "gufeuqzmjvtyjj"
# DB_PASSWORD     = "c10c3442ac6a371123e776c4af4ffa294db075a559a9455ae94d6a4b45836f78"
# DB_HOST         = "ec2-52-214-178-113.eu-west-1.compute.amazonaws.com"
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': DB_NAME,
#         'USER': DB_USER,
#         'PASSWORD': DB_PASSWORD,
#         'HOST': DB_HOST,
#         'PORT': '5432',
#     }
# }

# MYSQL ---------------------------------------------
# DATABASES = {  
#     'default': {  
#         'ENGINE': 'django.db.backends.mysql',  
#         'NAME': 'malomaTest',  
#         'USER': 'root',  
#         'PASSWORD': 'm195825735',  
#         'HOST': '127.0.0.1',  
#         'PORT': '3306',  
#         'OPTIONS': {  
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
#         }  
#     }  
# }

# POSTGRES ---------------------------------------------
DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.postgresql_psycopg2',
        'NAME'      : 'hekfzpkk',
        'USER'      : 'hekfzpkk',
        'PASSWORD'  : 'BQy_sfaSL3uXg9h7SU5HS3_miSDcI-ET',
        'HOST'      : 'surus.db.elephantsql.com',
        'PORT'      : '5432',
    }
}

# SQLITE ---------------------------------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# endregion Database

# region Test
TESTING = 'test' in sys.argv[1:]
# endregion Test

# region CORS WHITELIST
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "https://relaxed-curie-e9a516.netlify.app",
    "http://127.0.0.1:8080"
]

CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https://\w+\.netlify\.app$",
]
# endregion CORS WHITELIST

