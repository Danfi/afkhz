# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def get_dashboard_version():
    from backend.libs.dashboard.models import Dashboard
    try:
        return Dashboard.objects.get(id=1).version
    except:
        return ''