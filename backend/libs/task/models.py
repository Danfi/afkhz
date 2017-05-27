# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Task(models.Model):
    robot = models.ForeignKey('backend.Robot')
    min_time = models.DateTimeField(null=True, blank=True)
    max_time = models.DateTimeField(null=True, blank=True)
    now_time = models.DateTimeField(null=True, blank=True)
    latest = models.BooleanField(default=False)

    def __str__(self):
        return "[{}]{} {}".format(self.robot, self.min_time,  self.latest)
