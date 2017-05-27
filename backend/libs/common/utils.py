# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime
import calendar
import ast
from django.utils import timezone
from backend.libs.robot.utils import need_login
from backend.utils import do_post


ACTION_RESULT = {
    'destroyed a Resonator on': 'destroy',
    'deployed a Resonator on': 'deploy',
    'created a Control Field @': 'control_field',
    'linked': 'link',
    'captured': 'capture',
    'destroyed a Control Field @': 'destroy_control_field',
    'destroyed the Link': 'destroy_link',
    'created their first Link.': 'first_link',
    'captured their first Portal.': 'first_portal',
    'has completed training.': 'traning',
    'created their first Control Field.': 'first_control_field',
    'created their first Control Field': 'first_control_field',
    'deployed a Portal Fracker on': 'portal_fracker',
    'deployed a Beacon on': 'beacon'
}


def get_plexts(robot, version, task, get_log=False):
    if get_log:
        print('get_plexts')
    latest = task.latest
    send = True
    now = timezone.now()
    if task.max_time and now < task.max_time:
        send = False
    if send:
        if latest:
            data_dict = {
                'maxTimestampMs': -1,
                'minTimestampMs': -1,
                'maxLatE6': 30404323,
                'maxLngE6': 120625806,
                'minLatE6': 30107768,
                'minLngE6': 119788098,
                'v': version,
                'tab': 'all'
            }
        else:
            data_dict = {
                'ascendingTimestampOrder': True,
                'maxTimestampMs': -1,
                'minTimestampMs': int(calendar.timegm(task.now_time.timetuple())*1e3 + task.now_time.microsecond/1e3),
                'maxLatE6': 30404323,
                'maxLngE6': 120625806,
                'minLatE6': 30107768,
                'minLngE6': 119788098,
                'v': version,
                'tab': 'all'
            }
        if get_log:
            print('data_dict')
            print(data_dict)
        result = do_post(robot, 'getPlexts', json.dumps(data_dict))
        if result:
            if get_log:
                print(result.text)
            handle_plexts(robot, result.text, task, get_log)


def handle_plexts(robot, text, task, get_log=False):
    from backend.libs.common.models import Common
    try:
        t = json.loads(text)
        error = t.get('error')
        if error:
            need_login(robot)
            print('handle_plexts has error need login')
        else:
            result = t.get('result')
            if result:
                if get_log:
                    print('has result')
                max_time = start_time = task.now_time
                if get_log:
                    print('*'*80)
                    print('max_time', max_time)
                    print('start_time', start_time)
                if not max_time:
                    max_time = timezone.now()
                for x in result:
                    common_id = x[0]
                    action_time = datetime.datetime.fromtimestamp(float(x[1])/1000.0, timezone.utc)
                    if get_log:
                        print('action_time', action_time)
                        print('max_time', max_time)
                    if action_time > max_time:
                        max_time = action_time
                    if get_log:
                        print('max_time', max_time)
                    if not Common.objects.filter(common_id=common_id).exists():
                        plext = x[2].get('plext')
                        plextType = plext.get('plextType')
                        text = plext.get('markup')
                        markup = plext.get('markup')
                        team = plext.get('team')
                        if plextType == 'SYSTEM_BROADCAST':
                            tab = 'system'
                            player = markup[0][1].get('plain')
                            late6 = markup[2][1].get('latE6')
                            lnge6 = markup[2][1].get('lngE6')
                            plain = markup[1][1].get('plain').strip()
                        else:
                            late6 = None
                            lnge6 = None
                            plain = ''
                            if markup[0][0] == 'SECURE':
                                markup_dict = dict(markup)
                                tab = 'faction'
                                player_dict = markup_dict.get('SENDER') if markup_dict.get('SENDER') else markup_dict.get('PLAYER')
                                player = player_dict.get('plain').strip().rstrip(':')
                                if markup_dict.get('AT_PLAYER'):
                                    text = plext.get('text')
                                else:
                                    if len(markup) == 3 and markup[1][1].get('plain').find(':'):
                                        plain = markup[2][1].get('plain').strip()
                                        if plain != 'has completed training.':
                                            text = plext.get('text')
                                    elif len(markup) == 4:
                                        plain = markup[3][1].get('plain').strip()
                                    else:
                                        text = plext.get('text')
                            else:
                                player = markup[0][1].get('plain').strip().rstrip(':')
                                text = plext.get('text')
                                tab = 'all'
                        action = ACTION_RESULT.get(plain, None)
                        if action:
                            if action in ['destroy_link', 'destroy_control_field', 'destroy', 'deploy', 'capture']:
                                text = '%s' % x
                                markup_dict = dict(markup)
                                player_dict = markup_dict.get('PLAYER')
                                player_team = player_dict.get('team')
                                if action == 'destroy_link':
                                    team = player_team
                            elif plextType == 'SYSTEM_BROADCAST':
                                text = '%s' % x
                            # else:
                                # text = ''
                        if get_log:
                            print('player', player)
                        Common.objects.create(
                            common_id=common_id,
                            team=team,
                            player=player,
                            text=text,
                            action=action,
                            action_time=action_time,
                            late6=late6,
                            lnge6=lnge6,
                            tab=tab
                        )
                        if get_log:
                            print('saved')
                if get_log:
                    print('loop end')
                    print('max_time', max_time)
                    print('start_time', start_time)
                if max_time == start_time:
                    max_time += datetime.timedelta(microseconds=1000)
                task.now_time = max_time
                task.save()
    except Exception as e:
        print(e)
        need_login(robot)
        print('handle_plexts need login')


def do_statistics(cal_date):
    from backend.libs.common.models import Common, CommonStatistics, Newbie
    from django.db.models import Count
    start_date = cal_date
    end_date= cal_date + datetime.timedelta(days=1)
    queryset = Common.objects.filter(action_time__gte=start_date, action_time__lt=end_date).exclude(action__isnull=True)
    # newbie
    newbie_qs = queryset.filter(action__in=['traning', 'first_link', 'first_portal', 'first_control_field']).values('team', 'player')
    newbie_count = res_count = enl_count = 0
    for t in newbie_qs:
        newbie_obj, created = Newbie.objects.get_or_create(player=t.get('player'), team=t.get('team'), defaults={'join_date': cal_date})
        if created:
            newbie_count += 1
            if t.get('team') == 'RESISTANCE':
                res_count += 1
            else:
                enl_count += 1
    CommonStatistics.objects.create(
        staticstics_date=cal_date,
        action='newbie',
        points=newbie_count
    )
    CommonStatistics.objects.create(
        staticstics_date=cal_date,
        team='RESISTANCE',
        action='newbie',
        points=res_count
    )
    CommonStatistics.objects.create(
        staticstics_date=cal_date,
        team='ENLIGHTENED',
        action='newbie',
        points=enl_count
    )
    queryset = queryset.filter(tab='system')
    action_list = list(set(queryset.values_list('action', flat=True)))
    # all
    CommonStatistics.objects.create(
        action='all',
        staticstics_date=cal_date,
        points=queryset.count()
    )
    # team
    team_ac_qs = queryset.values('team').annotate(ac=Count('id'))
    for t in team_ac_qs:
        CommonStatistics.objects.create(
            action='all',
            staticstics_date=cal_date,
            team=t.get('team'),
            points=t.get('ac')
        )
    # player
    player_ac_qs = queryset.values('team', 'player').annotate(ac=Count('id'))
    for t in player_ac_qs:
        CommonStatistics.objects.create(
            action='all',
            staticstics_date=cal_date,
            team=t.get('team'),
            player=t.get('player'),
            points=t.get('ac')
        )
    # action
    action_ac_qs = queryset.values('action').annotate(ac=Count('id'))
    for t in action_ac_qs:
        CommonStatistics.objects.create(
            staticstics_date=cal_date,
            action=t.get('action'),
            points=t.get('ac')
        )
    # team action
    team_action_ac_qs = queryset.values('team', 'action').annotate(ac=Count('id'))
    for t in team_action_ac_qs:
        CommonStatistics.objects.create(
            staticstics_date=cal_date,
            team=t.get('team'),
            action=t.get('action'),
            points=t.get('ac')
        )
    # player action
    player_action_ac_qs = queryset.values('team', 'player', 'action').annotate(ac=Count('id'))
    for t in player_action_ac_qs:
        CommonStatistics.objects.create(
            staticstics_date=cal_date,
            team=t.get('team'),
            player=t.get('player'),
            action=t.get('action'),
            points=t.get('ac')
        )
    # TODO ada, jvs


def do_player_statistics(cal_date, old_player, new_player):
    from backend.libs.common.models import Common, CommonStatistics, Newbie
    from django.db.models import Count
    CommonStatistics.objects.filter(staticstics_date=cal_date, player=old_player).delete()
    CommonStatistics.objects.filter(staticstics_date=cal_date, player=new_player).delete()
    CommonStatistics.objects.filter(player=old_player).update(player=new_player)
    Common.objects.filter(player=old_player).update(player=new_player)
    start_date = cal_date
    end_date= cal_date + datetime.timedelta(days=1)
    queryset = Common.objects.filter(action_time__gte=start_date, action_time__lt=end_date, player=new_player).exclude(action__isnull=True)

    queryset = queryset.filter(tab='system')
    # all
    # player
    player_ac_qs = queryset.values('team', 'player').annotate(ac=Count('id'))
    for t in player_ac_qs:
        CommonStatistics.objects.create(
            action='all',
            staticstics_date=cal_date,
            team=t.get('team'),
            player=t.get('player'),
            points=t.get('ac')
        )
    # player action
    player_action_ac_qs = queryset.values('team', 'player', 'action').annotate(ac=Count('id'))
    for t in player_action_ac_qs:
        CommonStatistics.objects.create(
            staticstics_date=cal_date,
            team=t.get('team'),
            player=t.get('player'),
            action=t.get('action'),
            points=t.get('ac')
        )
    # TODO ada, jvs


def update_markup():
    from backend.libs.common.models import Common
    queryset = Common.objects.filter(tab='system', action__isnull=True)
    for t in queryset:
        markup = ast.literal_eval(t.text)
        plain = markup[1][1].get('plain').strip()
        action = ACTION_RESULT.get(plain, None)
        t.action = action
        t.save()


def get_team_compare_data(begin_date, end_date):
    from backend.libs.common.models import CommonStatistics
    queryset = CommonStatistics.objects.filter(action='all', player__isnull=True, team__isnull=False)
    queryset = queryset.filter(staticstics_date__gte=begin_date, staticstics_date__lte=end_date).order_by('staticstics_date')
    data = {
        'RESISTANCE': [],
        'ENLIGHTENED': [],
        'dates': []
    }
    for t in queryset:
        if t.team == 'RESISTANCE':
            data['RESISTANCE'].append(t.points)
        else:
            data['ENLIGHTENED'].append(t.points)
        cs_date = t.staticstics_date.strftime('%Y-%m-%d')
        if data['dates'].count(cs_date) == 0:
            data['dates'].append(cs_date)
    return data


def get_newbie_data(begin_date, end_date):
    from backend.libs.common.models import CommonStatistics
    queryset = CommonStatistics.objects.filter(action='newbie')
    queryset = queryset.filter(staticstics_date__gte=begin_date, staticstics_date__lte=end_date).order_by('staticstics_date')
    data = {
        'RESISTANCE': [],
        'ENLIGHTENED': [],
        'ALL': [],
        'dates': []
    }
    for t in queryset:
        if t.team == 'RESISTANCE':
            data['RESISTANCE'].append(t.points)
        elif t.team is None:
            data['ALL'].append(t.points)
        else:
            data['ENLIGHTENED'].append(t.points)
        cs_date = t.staticstics_date.strftime('%Y-%m-%d')
        if data['dates'].count(cs_date) == 0:
            data['dates'].append(cs_date)
    return data


def get_top_ten_data(team, begin_date, end_date, act):
    from backend.libs.common.models import CommonStatistics
    from django.db.models import Sum
    queryset = CommonStatistics.objects.filter(action=act, player__isnull=False)
    queryset = queryset.filter(staticstics_date__gte=begin_date, staticstics_date__lte=end_date)
    if team != 'all':
        queryset = queryset.filter(team=team)
    data = {
        'xAxis_data': [],
        'series_data': []
    }
    for t in queryset.values('team', 'player').annotate(ps=Sum('points')).order_by('-ps')[:30]:
        data['xAxis_data'].append(t.get('player'))
        if t.get('team') == 'ENLIGHTENED':
            point_data = {
                'value': t.get('ps'),
                'itemStyle': {
                    'normal': {
                        'color': '#008000'
                    }
                }
            }
        else:
            point_data = t.get('ps')
        data['series_data'].append(point_data)
    return data


def get_player_data(player, begin_date, end_date):
    from backend.libs.common.models import CommonStatistics
    queryset = CommonStatistics.objects.filter(action='all', player__isnull=False, player=player)
    queryset = queryset.filter(staticstics_date__gte=begin_date, staticstics_date__lte=end_date).order_by('staticstics_date')
    data = {
        'player': player,
        'points': [],
        'dates': [],
    }
    now_date = begin_date
    color = '#1681A3'
    for t in queryset:
        if t.team == 'ENLIGHTENED':
            color = '#008000'
        while now_date < t.staticstics_date:
            data['points'].append(0)
            data['dates'].append(now_date.strftime('%Y-%m-%d'))
            now_date += datetime.timedelta(days=1)
        data['points'].append(t.points)
        data['dates'].append(now_date.strftime('%Y-%m-%d'))
        now_date += datetime.timedelta(days=1)
    while now_date <= end_date:
        data['points'].append(0)
        data['dates'].append(now_date.strftime('%Y-%m-%d'))
        now_date += datetime.timedelta(days=1)
    data['color'] = color
    return data


def get_player_list_data():
    from backend.libs.common.models import Common, BlockAd
    result = list(set(Common.objects.exclude(player__in=BlockAd.objects.all().values_list('player', flat=True)).values_list('player', flat=True).order_by('player')))
    result.sort()
    return result
