# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Robot(models.Model):
    TEAM_CHOICES = (
        ('R', 'R'),
        ('E', 'E'),
    )
    team = models.CharField(max_length=2, choices=TEAM_CHOICES)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=32)
    sacsid = models.CharField(max_length=1024, null=True, blank=True)
    csrf_token = models.CharField(max_length=128, null=True, blank=True)
    login_latest = models.DateTimeField(null=True, blank=True)
    action_latest = models.DateTimeField(auto_now=True)
    need_login = models.IntegerField(default=0)

    def __str__(self):
        return self.email
