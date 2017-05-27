# -*- coding: utf-8 -*-
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from oauth2client import client, crypt
from .models import SystemUser


def login_user(request):
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    if request.method == "GET":
        return render(request, "user/login.html")
    token = request.POST["token"]
    info = client.verify_id_token(token, client_id)
    if info['aud'] != client_id:
        raise crypt.AppIdentityError("Unrecognized client.")
    if info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise crypt.AppIdentityError("Wrong issuer.")
    email = info.get('email')
    try:
        user = SystemUser.objects.get(email=email)
    except SystemUser.DoesNotExist:
        user = None
    if user:
        login(request, user)
        next_url = request.GET.get("next", "frontend:index")
        return redirect(next_url)
    return redirect("backend:user:register")


def logout_user(request):
    logout(request)
    return redirect("backend:user:login")


def register(request):
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    if request.method == "GET":
        return render(request, "user/register.html")
    token = request.POST["token"]
    info = client.verify_id_token(token, client_id)
    if info['aud'] != client_id:
        raise crypt.AppIdentityError("Unrecognized client.")
    if info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise crypt.AppIdentityError("Wrong issuer.")
    email = info.get('email')
    codename = request.POST.get("codename")
    try:
        user = SystemUser.objects.get(email=email)
        if user.nickname != codename:
            user.nickname = codename
            user.save()
    except SystemUser.DoesNotExist:
        user = SystemUser(nickname=codename)
        user.email = email
        user.set_unusable_password()
        user.is_active = False
        user.save()
    login(request, user)
    return redirect("frontend:index")
