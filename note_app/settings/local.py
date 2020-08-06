from .base import *
import environ


# SECURITY
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = True
ALLOWED_HOST = ['*']


# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}

# media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# logging
LOGGING = {

    # 初期化
    'version': 1,
    'disable_existing_loggers': False,
    
    # logger
    'loggers': {
        
        # Django
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        
        # apps
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagete': False,
        },
        
        # db
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
    },
    
    # handler
    'handlers': {
        
        # condole
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'develop',
        },
    },
    
    # formatter
    'formatters': {
        # develop
        'develop': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s'
        },
    },
}