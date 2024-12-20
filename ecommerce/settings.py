import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*1=0jc_n2onbu0)+9^edjfcu9m_k&11(0i2upymw#j5z_z+d6c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["merdemdeneme.pythonanywhere.com", "localhost"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ####
    'article.apps.ArticleConfig',
    'store.apps.StoreConfig',
    'accounts.apps.AccountsConfig',
    'settings.apps.SettingsConfig',
    ###
    'hitcount',
    'django_cleanup',
    "django_bootstrap5",
    'django_ckeditor_5',
    'sorl.thumbnail',
    'galleryfield',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'tr'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",

]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticFiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = "/media/"

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', "|", "FullScreen"],

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'language': 'tr',
        'toolbar': [
            "Essentials", "UploadAdapter", "CodeBlock", "Autoformat", "Bold", "Italic", "Underline", "Strikethrough",
            "Code",
            "Subscript",
            "Superscript", "BlockQuote", "Heading", "Image", "ImageCaption", "ImageStyle", "ImageToolbar",
            "ImageResize",
            "Link", "List", "Paragraph",
            "Alignment", "Font", "PasteFromOffice", "SimpleUploadAdapter", "MediaEmbed", "RemoveFormat", "Table",
            "TableToolbar", "TableCaption",
            "TableProperties", "TableCellProperties", "Indent", "IndentBlock", "Highlight", "TodoList",
            "ListProperties",
            "SourceEditing",
            "GeneralHtmlSupport", "ImageInsert", "WordCount", "Mention", "Style", "HorizontalLine", "LinkImage",
            "HtmlEmbed",
            "FullPage",
            "SpecialCharacters", "ShowBlocks", "SelectAll", "FindAndReplace", "FullScreen"
        ],

        'SourceEditing': {'toolbar': ['source']},
        'upload': {'blocking': True, 'showUploadProgress': True},
        "SimpleUploadAdapter": {"uploadPath": "/media/", "withCredentials": True},
        "uploadAdapter": {
            "uploadPath": "/upload/image/",
            "withCredentials": True,
        },
        "mediaEmbed": {"previewsInData": "true"},
        "FullScreen": {"toolbarCanCollapse": True, "title": "Full screen", "exit full screen": "Exit full screen"},
        "GeneralHtmlSupport": {"allowedContent": True, "allowedAttributes": True, "allowedElements": "*"},
        "PasteFromOffice": {"promptBeforePaste": True},
        "imageCaption": {"allowTitle": True},
        "imageTextAlternative": {"label": "Image description"},
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|' 'imageTitle',
                        'imageCaption',
                        ],
            'styles': [
                'fullWidth',
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells',
                               'tableProperties', 'tableCellProperties'],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_IMAGE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_IMAGE_UPLOAD_BACKEND = "django_cleanup.backends.imagekit.ImageKitBackend"

CKEDITOR_5_IMAGE_BACKEND = "sorl.thumbnail"
CKEDITOR_5_THUMBNAIL_BACKEND = "sorl.thumbnail"

CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME = "ckeditor5_upload_file"

CKEDITOR_5_IMAGE_THUMBNAIL_PROCESSORS = (
    'thumbnailor.processors.fit_in',
    'thumbnailor.processors.format',
    'thumbnailor.processors.resize',
    'thumbnailor.processors.rotate',
    'thumbnailor.processors.flip',
    'thumbnailor.processors.flop',
    'thumbnailor.processors.exif',
    'thumbnailor.processors.quality',
    'thumbnailor.processors.progressive',
    'thumbnailor.processors.format_opt',
    'thumbnailor.processors.background',
    'thumbnailor.processors.blur',
    'thumbnailor.processors.contrast',
    'thumbnailor.processors.sharpen',
    'thumbnailor.processors.grayscale',
    'thumbnailor.processors.colorize',
    'thumbnailor.processors.emboss',
    'thumbnailor.processors.edge_enhance',
)

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
]

CKEDITOR_5_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True

# email configs
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''