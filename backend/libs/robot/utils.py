# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import re
import datetime
from selenium import webdriver
from django.utils import timezone
from pyvirtualdisplay import Display


def robot_login(robot):
    from backend.libs.dashboard.models import Dashboard
    display = Display(visible=0, size=(1024, 768))
    display.start()
    browser = webdriver.Chrome()
    try:
        time.sleep(5)
        browser.get('https://www.ingress.com/intel')
        time.sleep(4)
        btn = browser.find_element_by_class_name('button_link')
        btn.click()
        time.sleep(5)
        email = browser.find_element_by_id('identifierId')
        email.send_keys(robot.email)
        next_btn = browser.find_element_by_id('identifierNext')
        next_btn.click()
        time.sleep(2)
        pwd = browser.find_element_by_name('password')
        pwd.send_keys(robot.password)
        sing_in_btn = browser.find_element_by_id('passwordNext')
        sing_in_btn.click()
        time.sleep(5)
        token = browser.get_cookie('csrftoken').get('value')
        sacsid = browser.get_cookie('SACSID').get('value')
        if token and sacsid and len(sacsid) > 50:
            if not robot.login_latest or robot.login_latest + datetime.timedelta(minutes=5) < timezone.now():
                robot.csrf_token = token
                robot.sacsid = sacsid
                robot.login_latest = datetime.datetime.now()
                robot.need_login = 0
                robot.save()
            intel_html = browser.page_source
            vs_pattern = re.compile(r'gen_dashboard_\w*.js')
            v = vs_pattern.findall(intel_html)[0].split('_')[2].split('.')[0]
            try:
                dashboard = Dashboard.objects.get(id=1)
            except Dashboard.DoesNotExist:
                dashboard = Dashboard()
            dashboard.version = v
            dashboard.save()
        # browser.close()
        browser.quit()
        display.stop()
    except:
        # browser.close()
        browser.quit()
        display.stop()


def need_login(robot):
    robot.need_login += 1
    robot.save()
