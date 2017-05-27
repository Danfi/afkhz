# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Common(models.Model):
    ACTION_CHOICES = (
        ('capture', 'capture'),
        ('traning', 'training'),
        ('first_link', 'first link'),
        ('first_portal', 'first portal'),
        ('first_control_field', 'first control field'),
        ('link', 'link'),
        ('control_field', 'control field'),
        ('deploy', 'deploy'),
        ('destroy', 'destroy'),
        ('ada', 'ada'),
        ('jvs', 'jvs'),
        ('destroy_control_field', 'destroy control field'),
        ('destroy_link', 'destroy link'),
        ('portal_fracker', 'portal fracker'),
        ('beacon', 'beacon'),
    )
    TEAM_CHOICES = (
        ('RESISTANCE', 'RESISTANCE'),
        ('ENLIGHTENED', 'ENLIGHTENED'),
    )
    common_id = models.CharField(max_length=64, db_index=True, unique=True)
    team = models.CharField(max_length=16, choices=TEAM_CHOICES, db_index=True)
    player = models.CharField(max_length=32, db_index=True)
    text = models.TextField()
    action = models.CharField(max_length=32, choices=ACTION_CHOICES, null=True, blank=True)
    action_time = models.DateTimeField()
    late6 = models.IntegerField(null=True, blank=True)
    lnge6 = models.IntegerField(null=True, blank=True)
    province = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    tab = models.CharField(max_length=8, default='all')

    def __str__(self):
        return "[{}]{} {}".format(self.team, self.player,  self.action)


class CommonStatistics(models.Model):
    ACTION_CHOICES = (
        ('all', 'all'),
        ('newbie', 'newbie'),
        ('capture', 'capture'),
        ('link', 'link'),
        ('control_field', 'control field'),
        ('deploy', 'deploy'),
        ('destroy', 'destroy'),
        ('ada', 'ada'),
        ('jvs', 'jvs'),
        ('destroy_control_field', 'destroy control field'),
        ('destroy_link', 'destroy link'),
        ('portal_fracker', 'portal fracker'),
        ('beacon', 'beacon'),
    )
    city = models.CharField(max_length=32, null=True, blank=True)
    staticstics_date = models.DateField()
    player = models.CharField(max_length=32, db_index=True, null=True, blank=True)
    team = models.CharField(max_length=16, db_index=True, null=True, blank=True)
    points = models.IntegerField()
    action = models.CharField(max_length=32, choices=ACTION_CHOICES, null=True, blank=True)

    def __str__(self):
        return "[{}]{}:{}".format(self.team, self.player,  self.points)


class BlockAd(models.Model):
    player = models.CharField(max_length=32)

    def __str__(self):
        return self.player


class Newbie(models.Model):
    join_date = models.DateField()
    team = models.CharField(max_length=16, db_index=True, null=True, blank=True)
    player = models.CharField(max_length=32)

    def __str__(self):
        return self.player
