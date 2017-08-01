# -*- coding: utf-8 -*-
from ..models import Exams, Result

from django.shortcuts import render
# help variable:
ids = [1,2,3] # ids of Result Exams

def results_list(request):
    ''' Result list method '''

    results_list = Exams.objects.all()

    return render(request, 'students/results_list.html', {'results_list': results_list,'ids':ids})
