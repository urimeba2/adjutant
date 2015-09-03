# Copyright (C) 2015 Catalyst IT Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Django settings for user_reg project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import yaml
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'stacktask.base',
    'stacktask.api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'stacktask.middleware.KeystoneHeaderUnwrapper',
    'stacktask.middleware.RequestLoggingMiddleware'
)

if 'test' in sys.argv:
    # modify MIDDLEWARE_CLASSES
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.remove('stacktask.middleware.KeystoneHeaderUnwrapper')
    MIDDLEWARE_CLASSES.append('stacktask.middleware.TestingHeaderUnwrapper')

ROOT_URLCONF = 'stacktask.urls'

WSGI_APPLICATION = 'stacktask.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# Setup of local settings data
if 'test' in sys.argv:
    from stacktask import test_settings
    CONFIG = test_settings.conf_dict
else:
    with open("/etc/stacktask/conf.yaml") as f:
        CONFIG = yaml.load(f)

SECRET_KEY = CONFIG['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get('DEBUG', False)

if not DEBUG:
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        )
    }

ALLOWED_HOSTS = CONFIG.get('ALLOWED_HOSTS', [])

for app in CONFIG['ADDITIONAL_APPS']:
    INSTALLED_APPS = list(INSTALLED_APPS)
    INSTALLED_APPS.append(app)

DATABASES = CONFIG['DATABASES']

LOGGING = CONFIG['LOGGING']


EMAIL_BACKEND = CONFIG['EMAIL_SETTINGS']['EMAIL_BACKEND']
EMAIL_TIMEOUT = 60

if CONFIG['EMAIL_SETTINGS'].get('EMAIL_HOST'):
    EMAIL_HOST = CONFIG['EMAIL_SETTINGS']['EMAIL_HOST']

if CONFIG['EMAIL_SETTINGS'].get('EMAIL_PORT'):
    EMAIL_PORT = CONFIG['EMAIL_SETTINGS']['EMAIL_PORT']

if CONFIG['EMAIL_SETTINGS'].get('EMAIL_HOST_USER'):
    EMAIL_HOST_USER = CONFIG['EMAIL_SETTINGS']['EMAIL_HOST_USER']

# setting to control if user name and email are allowed
# to have different values.
USERNAME_IS_EMAIL = CONFIG['USERNAME_IS_EMAIL']

# Keystone admin credentials:
KEYSTONE = CONFIG['KEYSTONE']

DEFAULT_REGION = CONFIG['DEFAULT_REGION']

# Additonal actions for views:
# - The order of the actions matters. These will run after the default action,
#   in the given order.
ACTIONVIEW_SETTINGS = CONFIG['ACTIONVIEW_SETTINGS']

ACTION_SETTINGS = CONFIG['ACTION_SETTINGS']

# Dict of actions and their serializers.
# - This is populated from the various model modules at startup:
ACTION_CLASSES = {}