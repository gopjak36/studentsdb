# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from ..models import Exam

# Views for Exam

def exams_list(request):
    exams = Exam.objects.all()

    return render(request, 'students/exams_list.html', {'exams': exams})
