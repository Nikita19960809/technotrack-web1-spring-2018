# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

def jobs_detail(request,job_id):
    if job_id == "":
        return HttpResponse("List of jobs")
    return HttpResponse("That's job number {}".format(job_id))