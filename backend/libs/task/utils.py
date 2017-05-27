# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from backend.libs.common.utils import get_plexts
from backend.libs.dashboard.utils import get_dashboard_version


def do_task(team='R', latest=True):
    from backend.libs.task.models import Task
    try:
        t = Task.objects.filter(robot__team=team, latest=latest).order_by('?')[0]
        get_plexts(t.robot, get_dashboard_version(), t)
    except:
        pass
