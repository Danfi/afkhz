#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import datetime
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.template import loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render, redirect
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, InvalidPage



def pagination_func(request, queryset, default_order_field=''):
    if 'order_field' in request.GET:
        queryset = queryset.order_by(*([x.strip() for x in request.GET['order_field'].split(',')]))
    elif default_order_field:
        queryset = queryset.order_by(*([y.strip() for y in default_order_field.split(',')]))
    else:
        pass
    per_page_items = settings.PAGINATION_PER_PAGE
    per_page = getattr(request.user, 'per_page', None)
    if per_page:
        per_page_items = per_page
    if 'per_page' in request.GET:
        per_page_items = request.GET['per_page']
    paginator_obj = Paginator(queryset, per_page_items)
    if 'page' in request.GET:
        target_page = int(request.GET.get("page", 1))
    else:
        target_page = 1
    try:
        cont = paginator_obj.page(target_page)
    except(EmptyPage, InvalidPage):
        cont = paginator_obj.page(paginator_obj.num_pages)
    return cont


def response_render(f=None, default_order_field=None, t=None, mimetype=None):
    def decorator(func):
        @wraps(func)
        def wrap(request, *args, **kwargs):
            ret = func(request, *args, **kwargs)
            if isinstance(ret, type({})):
                ctx = ret
                if 'object_result' in ctx:
                    ctx['object_result'] = pagination_func(
                        request, ctx['object_result'],
                        default_order_field=ctx.get('default_order_field', default_order_field))
                redirect_to = ctx.get('redirect', None)
                json_data = ctx.get('json', None)
                if json_data is not None:
                    if not isinstance(json_data, dict):
                        is_safe = False
                    else:
                        is_safe = True
                    http_response = JsonResponse(json_data, safe=is_safe)
                else:
                    if not redirect_to:
                        if mimetype:
                            http_response = render(request, ctx.get('template_name', t), ctx, content_type=mimetype)
                        else:
                            http_response = render(request, ctx.get('template_name', t), ctx)
                    else:
                        http_response = redirect(redirect_to)
                return http_response
            else:
                return ret

        return wrap

    if f:
        return decorator(f)
    return decorator


def get_req_date(request):
    today = datetime.date.today()
    begin_date = datetime.datetime(today.year, today.month, 1).date()
    end_date = today - datetime.timedelta(days=1)
    begin_date_str = request.GET.get('begin_date')
    end_date_str = request.GET.get('end_date')
    if begin_date_str:
        try:
            begin_date = datetime.datetime.strptime(begin_date_str, '%Y-%m-%d').date()
        except:
            pass
    if end_date_str:
        try:
            new_end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            if new_end_date < end_date:
                end_date = new_end_date
        except:
            pass
    return begin_date, end_date
