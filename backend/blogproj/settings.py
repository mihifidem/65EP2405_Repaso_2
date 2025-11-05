import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
import os
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

# === ENV ===
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "inseguro-dev")
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    # Terceros
    "rest_framework","django_filters","corsheaders",
    # App propia
    "core",
    'accounts',
    'drf_spectacular',
      'ckeditor',
    'ckeditor_uploader',

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS primero
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blogproj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],   # Plantillas globales
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "blogproj.wsgi.application"

# === Base de datos ===
# Por simplicidad SQLite; si quieres Postgres, usa dj-database-url o similar.
DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{os.getenv('DJANGO_DB_ENGINE', 'sqlite3')}",
        "NAME": BASE_DIR / os.getenv("DJANGO_DB_NAME", "db.sqlite3"),
    }
}

# === Idioma y zona horaria ===
LANGUAGE_CODE = "es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# === Archivos estáticos ===
STATIC_URL = os.getenv("STATIC_URL", "/static/")

# Archivos estáticos durante desarrollo
STATICFILES_DIRS = [
    BASE_DIR / 'core' / 'static',  # ✅ apunta a la carpeta static de tu app
]

STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_URL = os.getenv("MEDIA_URL", "/media/")
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === DRF ===
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),

    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

CSRF_TRUSTED_ORIGINS = [f"http://{h}" for h in ALLOWED_HOSTS if h not in ("*", "")]


# === JWT ===
# ACCESS_MIN = config("ACCESS_TOKEN_LIFETIME_MIN", default=15, cast=int)
# REFRESH_DAYS = config("REFRESH_TOKEN_LIFETIME_DAYS", default=7, cast=int)
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_MIN),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_DAYS),
# }

# === CORS ===
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = config("CORS_ALLOW_ORIGINS", default="http://localhost:3000", cast=Csv())
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # puerto de Vite
]

SPECTACULAR_SETTINGS = {
    "TITLE": "Blog API",
    "DESCRIPTION": "Documentación de la API del Blog con Django REST Framework.",
    "VERSION": "1.0.0",

    # URLs de los recursos de Swagger y Redoc (cargados desde Internet)
    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14",
    "SWAGGER_UI_FAVICON_HREF": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/favicon-32x32.png",
    "REDOC_DIST": "https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js",
}
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format', 'Font', 'FontSize', 'TextColor', 'BGColor'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'Blockquote'],
            ['CodeSnippet', 'Source'],
            ['Undo', 'Redo'],
            ['Maximize'],
        ],
        'extraPlugins': ','.join([
            'codesnippet',     # Bloques de código con resaltado
            'font',            # Cambiar fuente
            'colorbutton',     # Colores
            'justify',         # Alineación
            'uploadimage',     # Subida de imágenes
            'autogrow',        # Autoajuste del tamaño
            'clipboard',       # Mejora pegado
            'format',          # Permite seleccionar formatos (h1,h2,pre,…)
        ]),
        # 🧠 Estas tres líneas son cruciales para que NO formatee mal el código:
        'allowedContent': True,            # No limpia etiquetas <pre>, <code>, <br>
        'forcePasteAsPlainText': False,    # Permite pegar HTML y respetar formato original
        'enterMode': 2,                    # Inserta <br> en lugar de <p> al presionar Enter

        'height': 400,
        'width': '100%',
        'autoGrow_minHeight': 250,
        'autoGrow_maxHeight': 800,
        'codeSnippet_theme': 'monokai_sublime',
        'removeDialogTabs': 'image:advanced;link:advanced',

        'font_names': (
            'Arial/Arial, Helvetica, sans-serif;'
            'Courier New/Courier New, Courier, monospace;'
            'Georgia/Georgia, serif;'
            'Tahoma/Tahoma, Geneva, sans-serif;'
            'Times New Roman/Times New Roman, Times, serif;'
            'Verdana/Verdana, Geneva, sans-serif'
        ),

        'fontSize_sizes': (
            '10/10px;11/11px;12/12px;14/14px;16/16px;18/18px;20/20px;22/22px;'
            '24/24px;26/26px;28/28px;32/32px;36/36px;48/48px;'
        ),
    }
}


