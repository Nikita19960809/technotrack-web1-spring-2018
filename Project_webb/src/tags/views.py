# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse

def tags_detail(request,tag_id):
    if tag_id == "":
        return HttpResponse("List of tags")
    return HttpResponse("That's tag number {}".format(tag_id))
