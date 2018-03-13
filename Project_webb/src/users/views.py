# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

def users_detail(request,user_id):
    if user_id == "":
        return HttpResponse("List of users")
    return HttpResponse("That's user number {}".format(user_id))
def user_login(request):
    return HttpResponse("User login")
def user_signup(request):
    return HttpResponse("User signup")