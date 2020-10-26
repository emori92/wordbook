"""local test environment"""


from .base import *
import environ


# SECURITY
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = True  # Trueにしないと、local testはエラーになる
ALLOWED_HOSTS = ['*']

# media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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
        
        'accounts': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagete': False,
        },

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
