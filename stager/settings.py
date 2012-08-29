""" Django settings for stager project. """
import os
from datetime import date

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = False

from local_settings import *
MEDIA_URL = BASE_URL + MEDIA_PREFIX + "/"

MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                "../" + MEDIA_PREFIX)
BASE_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")

THUMBNAIL_SUBDIR = 'images'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'stager.urls'

TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), "../templates/jira"),
				 os.path.join(os.path.dirname(__file__), "../templates/stager"), 
				 os.path.join(os.path.dirname(__file__), "../templates")]

AUTH_PROFILE_MODULE = 'stager.Client'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'stager.staging', 
    'django_evolution',
    'export',
	'sorl.thumbnail',
	'stager.jira',
    'django_extensions'
)

# Stager Settings
FILE_UPLOAD = 'upload'
MAX_UPLOAD_SIZE = 5242880
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Export Settings
MYSQLDUMP_CMD = 'mysqldump -h %s --opt --compact --skip-add-locks -u %s -p%s %s'
DATABASE_FILENAME = date.today().__str__()+'_db.sql'

# Active Directory / LDAP Settings (Requires python-ldap)
AUTHENTICATION_BACKENDS = (
    # Uncomment this for Active Directory / LDAP support
    # 'stager.backends.ActiveDirectoryGroupMembershipSSLBackend',
    'django.contrib.auth.backends.ModelBackend',
)

