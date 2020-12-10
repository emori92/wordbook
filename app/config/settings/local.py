from .base import *


# SECURITY
SECRET_KEY = '####development_secret_key####'
ALLOWED_HOSTS = ['*']
DEBUG = True


# DB
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wordbook',
        'USER': 'app_owner',
        'PASSWORD': 'dbpass',
        'HOST': 'db',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

# DB transaction
DATABASES['default']['ATOMIC_REQUESTS'] = True


# debug toolbar
if DEBUG:
    def show_toolbar(request):
        return True
    
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
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
        
        'accounts': {
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
