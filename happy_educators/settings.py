from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------
# SECURITY
# ---------------------------------------------------

SECRET_KEY = 'django-insecure-change-this-in-production'

DEBUG = False

ALLOWED_HOSTS = ["*"]


# ---------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'academics',
]


# ---------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',  # REQUIRED
    'django.contrib.messages.middleware.MessageMiddleware',      # REQUIRED

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# ---------------------------------------------------
# URL CONFIG
# ---------------------------------------------------

ROOT_URLCONF = 'happy_educators.urls'


# ---------------------------------------------------
# TEMPLATES
# ---------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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


# ---------------------------------------------------
# WSGI
# ---------------------------------------------------

WSGI_APPLICATION = 'happy_educators.wsgi.application'


# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ---------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------

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


# ---------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# ---------------------------------------------------
# STATIC FILES
# ---------------------------------------------------

STATIC_URL = 'static/'


# ---------------------------------------------------
# LOGIN / AUTH FLOW (VERY IMPORTANT)
# ---------------------------------------------------

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"