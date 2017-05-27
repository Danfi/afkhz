#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import datetime
from time import sleep
from uwsgidecorators import *
from django.utils import timezone
from backend.libs.task.utils import do_task


@timer(10)
def get_res_plexts(num):
    do_task(latest=False)


@timer(12)
def get_enl_plexts(num):
    do_task('E', latest=False)


@timer(16)
def get_latest_res_plexts(num):
    do_task()


@timer(17)
def get_latest_enl_plexts(num):
    do_task('E')


@timer(120)
def check_login(num):
    from backend.libs.robot.models import Robot
    from backend.libs.robot.utils import robot_login
    try:
        t = Robot.objects.filter(need_login__gt=50)[0]
        robot_login(t)
    except:
        pass


@cron(10, 0, -1, -1, -1)
def gen_statistics_data_yestaday(arg):
    from backend.libs.common.utils import do_statistics
    yestaday = datetime.datetime.now() - datetime.timedelta(days=1)
    do_statistics(datetime.datetime(yestaday.year, yestaday.month, yestaday.day, tzinfo=timezone.utc))
