# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

def question_detail(request,question_id):
    print(question_id)
    if question_id == "":
        return HttpResponse("List of questions")
    return HttpResponse("That's question number {}".format(question_id))