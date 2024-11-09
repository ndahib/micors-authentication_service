from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "www.google.com"]
AUTH_USER_MODEL = "authentication_app.CustomUser"

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'authlib',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_email',

    'qrcode',
    'authentication_app',
    'social_authentication',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
]

ROOT_URLCONF = 'service_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
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

ASGI_APPLICATION = 'service_core.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
from password_strength import PasswordPolicy

PASSWORD_POLICY = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    special=0,
    strength=(0.33, 30),
)


# Internationali  zation
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_URL = 'static/'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # for debug
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # for deploy
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')



#####################SOCIAL_AUTH_VARIABLES######################
GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_SECRET_KEY = os.environ.get('GOOGLE_OAUTH2_SECRET_KEY')
GOOGLE_OAUTH2_REDIRECT_URI = os.environ.get('GOOGLE_OAUTH2_REDIRECT_URI')
GOOGLE_OAUTH2_CLIENT_SECRET_JSON = os.environ.get('GOOGLE_CLIENT_SECRET_JSON')
DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD')


#######################Session Settings########################
SESSION_COOKIE_AGE = 1200
SESSION_EXPIRE_AT_BROWSER_CLOSE = True



########################42 Authentication########################

AUTHLIB_OAUTH_CLIENTS = {
    '42': {
        'client_id': os.environ.get("INTRA_OAUTH2_CLIENT_ID"),
        'client_secret': os.environ.get("INTRA_OAUTH2_SECRET_KEY"),
        'api_base_url': os.environ.get("INTRA_API_BASE_URL"),
        'access_token_url': os.environ.get("INTRA_API_TOKEN_URL"),
        'authorize_url': os.environ.get("INTRA_API_AUTHORIZE_URL"),
        "redirect_uri": os.environ.get("INTRA_OAUTH2_REDIRECT_URI"),
    },
}


########################## OTP settings for email########################
OTP_EMAIL_SENDER        = os.environ.get('OTP_EMAIL_SENDER')
OTP_EMAIL_SUBJECT       = os.environ.get('OTP_EMAIL_SUBJECT')
OTP_EMAIL_TOKEN_VALIDIT =  os.environ.get('OTP_EMAIL_TOKEN_VALIDITY')


from  datetime import timedelta
######################### Simple jwt settings ########################
SIMPLE_JWT = {
    # 'ROTATE_REFRESH_TOKENS': True,
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # 'BLACKLIST_AFTER_ROTATION': True,
    # "CHECK_REVOKE_TOKEN": True,
    # add setting for Secret Key
}