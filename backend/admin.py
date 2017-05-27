#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from .libs.robot.models import Robot
from .libs.task.models import Task
from .libs.common.models import Common, BlockAd, CommonStatistics, Newbie
from .libs.user.models import SystemUser


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ('team', 'email', 'login_latest', 'login_latest', 'need_login', 'action_latest')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('robot', 'min_time', 'max_time', 'now_time', 'latest')


@admin.register(Common)
class CommonAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'player_show', 'action', 'get_text')
    list_filter = ('action', 'tab',)
    ordering = ('-action_time',)

    def get_queryset(self, request):
        qs = super(CommonAdmin, self).get_queryset(request)
        return qs.exclude(player__in=BlockAd.objects.all().values_list('player', flat=True))

    def get_text(self, obj):
        if obj.tab == 'system':
            return ''
        return obj.text
    get_text.short_description = u'Text'

    def player_show(self, obj):
        result = u''
        if obj.team == 'RESISTANCE':
            color = '1681A3'
        else:
            color = '008000'
        result = u'<a style="color:#%s" href="%s?player=%s">%s</a>' % (color, reverse('admin:backend_common_changelist'), obj.player, obj.player)
        return mark_safe(result)
    player_show.admin_order_field = 'player'
    player_show.short_description = u'Player'


@admin.register(BlockAd)
class BlockAdAdmin(admin.ModelAdmin):
    list_display = ('player',)


@admin.register(CommonStatistics)
class CommonStatisticsAdmin(admin.ModelAdmin):
    list_display = ('staticstics_date', 'team', 'player', 'action', 'points',)
    list_filter = ('action',)
    ordering = ('-staticstics_date', 'action', '-points',)


@admin.register(Newbie)
class NewbieAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'join_date',)
    ordering = ('-join_date',)

@admin.register(SystemUser)
class SystemUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'nickname', 'register_time')
    list_filter = ('is_active',)

admin.site.unregister(Group)
