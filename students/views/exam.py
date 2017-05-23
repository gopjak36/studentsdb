# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from ..models import Exam

# Views for Exam

def exams_list(request):
    exams = Exam.objects.all()

    # Order By exams list
    order_by = request.GET.get('order_by', '')
    if order_by in ('name', 'groups', 'time'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    return render(request, 'students/exams_list.html', {'exams': exams})
