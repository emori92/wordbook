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
DATABASES['default']['ATOMIC_REQUESTS'] = True


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
