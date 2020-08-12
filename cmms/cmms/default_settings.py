"""
Django settings for cmms project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm-e7!9lv=s%)7nbth%@i94=txyetdqsy-r^=6j%3aon@s(2yez'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': 'cmms/mysql.cnf',
            'charset': 'utf8mb4',
        },
        'TEST': {
            'NAME': 'CMMS_test',
            'CHARSET': 'utf8mb4'
        }
    }
}