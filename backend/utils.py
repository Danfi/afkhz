#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from django.conf import settings
from backend.libs.robot.utils import need_login


def do_post(robot, method, data_json):
    csrftoken = robot.csrf_token
    headers = {
        'X-CSRFToken': csrftoken,
        'Referer': 'https://www.ingress.com/intel',
        'Origin': 'https://www.ingress.com/intel',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36'
    }
    send_cookies = {
        'SACSID': robot.sacsid,
        'csrftoken': csrftoken,
        'ingress.intelmap.lat': settings.LAT,
        'ingress.intelmap.lng': settings.LNG,
        'ingress.intelmap.zoom': '11',
        '__utma': settings.UTMA,
        '__utmb': settings.UTMB,
        '__utmc': settings.UTMC,
        '__utmz': settings.UTMZ,
        '__utmt': '1',
        'ingress.intelmap.shflt': 'viz',
    }
    try:
        req = requests.post(
            'https://www.ingress.com/r/' + method,
            headers=headers,
            data=data_json,
            cookies=send_cookies,
            timeout=15
        )
        if req.status_code != 200:
            print('do_post 200 need login')
            need_login(robot)
            req = None
    except Exception as e:
        print(e)
        print('do_post need login')
        need_login(robot)
        req = None
    return req
