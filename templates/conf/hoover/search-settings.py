from pathlib import Path
base_dir = Path(__file__).absolute().parent.parent.parent.parent
SECRET_KEY = '--- secret key ---'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hoover-search',
    },
}

INSTALLED_APPS = (
    #'hoover.contrib.oauth2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hoover.search',
)

ALLOWED_HOSTS = ['hoover.{{liquid_domain}}']

STATIC_ROOT = str(base_dir / 'static')
HOOVER_UPLOADS_ROOT = str(base_dir / 'uploads')
HOOVER_ELASTICSEARCH_URL = 'http://localhost:14352'
HOOVER_UI_ROOT = '/opt/hoover/ui/build'

#HOOVER_OAUTH_LIQUID_URL = None
#HOOVER_OAUTH_LIQUID_CLIENT_ID = None
#HOOVER_OAUTH_LIQUID_CLIENT_SECRET = None
