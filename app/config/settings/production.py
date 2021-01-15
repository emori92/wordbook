"""local test environment"""


from .base import *
import environ


# environ variable
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


# security
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# database
DATABASES = {
    'default': env.db()
}
# transaction
DATABASES['default']['ATOMIC_REQUESTS'] = True


# AWS S3
if env('USE_S3'):
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    # S3 domain
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    # permission
    AWS_DEFAULT_ACL = None
    # static
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    # media
    MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'config.custom_storage.MediaStorage'


# GCS
if env('USE_GCS'):
    from google.oauth2 import service_account
    # 認証
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        env('GS_CREDENTIALS')
    )
    # storage
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = env('GS_BUCKET_NAME')
    # static
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'


# logging
LOGGING = {

    # 初期化
    'version': 1,
    'disable_existing_loggers': False,
    
    # logger
    'loggers': {
        # Django
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        # apps
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagete': False,
        },
    },
    
    # handler
    'handlers': {
        # condole
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/wordbook.log'),
            'formatter': 'production',
            'when': 'D',
            'backupCount': 7,
        },
    },
    
    # formatter
    'formatters': {
        # production
        'production': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s'
        },
    },
    
}
