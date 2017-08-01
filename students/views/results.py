# -*- coding: utf-8 -*-
from ..models import Exams, Result, Student

from django.shortcuts import render
# help variable:
ids = [1,2,3] # ids of Result Exams

def results_list(request):
    ''' Results list method '''

    results_list = Exams.objects.all()

    return render(request, 'students/results_list.html', {'results_list': results_list,'ids':ids})

def results_result(request,rid):
    ''' Result method '''

    result = Student.objects.all().order_by('last_name')
    rid = Exams.objects.get(id=rid)

    return render(request, 'students/results_result.html', {'result':result,'rid':rid})
