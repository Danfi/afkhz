#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'extensions':['jinja2.ext.i18n'],
        'GOOGLE_OAUTH2_CLIENT_ID': settings.GOOGLE_OAUTH2_CLIENT_ID
    })
    return env
