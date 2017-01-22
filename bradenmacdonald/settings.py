"""
Django settings for bradenmacdonald.com
"""
import os.path
import yaml

########################################################################################################################
# Override the following in ../private.yml:
LOCAL_SETTINGS = """
DATABASE:
    NAME: bradenmacdonald
DEBUG: false
SECRET_KEY:
# Cache setting - set to a string prefix to enable redis cache use:
USE_REDIS_CACHE_PREFIX:
ALLOWED_HOSTS:
    - .bradenmacdonald.com
"""
########################################################################################################################

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Update LOCAL_SETTINGS:
LOCAL_SETTINGS = yaml.load(LOCAL_SETTINGS)
with open(PROJECT_ROOT + "/private.yml") as fh:
    LOCAL_SETTINGS.update(yaml.load(fh.read()))

SECRET_KEY = LOCAL_SETTINGS['SECRET_KEY']
DEBUG = LOCAL_SETTINGS['DEBUG']

ALLOWED_HOSTS = LOCAL_SETTINGS['ALLOWED_HOSTS']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'blog',
    'friendly_dates',
    'bradenmacdonald.content',
    'bradenmacdonald.quotes',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bradenmacdonald.urls'
WSGI_APPLICATION = 'bradenmacdonald.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '',
    }
}
DATABASES['default'].update(LOCAL_SETTINGS['DATABASE'])

LANGUAGE_CODE = 'en-ca'
TIME_ZONE = 'America/Vancouver'
USE_I18N = False
USE_L10N = False
USE_TZ = True

STATIC_ROOT = LOCAL_SETTINGS.get('STATIC_ROOT', os.path.join(PROJECT_ROOT, "site_media"))
STATIC_URL = '/s/'
MEDIA_ROOT = LOCAL_SETTINGS.get('MEDIA_ROOT', os.path.join(PROJECT_ROOT, "user_media"))
MEDIA_URL = "/m/"
# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "bradenmacdonald", "static"),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (
            os.path.join(PROJECT_ROOT, 'bradenmacdonald', 'templates'),
        ),
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                #'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.csrf',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                # Header/footer navigation support:
                'bradenmacdonald.nav.get_nav',
            ),
        }
    },
]

# Whether Django should serve media files (user uploads) with its built-in server
SERVE_MEDIA_FILES = LOCAL_SETTINGS.get("SERVE_MEDIA_FILES", DEBUG)

# Compressor settings:
COMPRESS_ENABLED = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_OUTPUT_DIR = 'cache'  # lower-case the default "CACHE"
COMPRESS_PRECOMPILERS = (
    ("text/less", 'bradenmacdonald.utils.compressor.LessFilter'),
)
COMPRESS_CSS_FILTERS = ['bradenmacdonald.utils.compressor.CssAbsoluteFilterFixed']
if not DEBUG:
    COMPRESS_OFFLINE = True
