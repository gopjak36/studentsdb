# -*- coding: utf-8 -*-
from ..models import Exams, Result, Student

from django.shortcuts import render
# help variable:
ids = [1,2,3] # ids of Result Exams

def results_list(request):
    ''' Results list method '''

    # help variable
    results_list = Exams.objects.all() # all Exams objects

    # Render Page:
    return render(request, 'students/results_list.html', {'results_list': results_list,'ids':ids})

def results_result(request,eid):
    ''' Result method '''

    # help variables:
    students = Student.objects.all().order_by('last_name') # all Student objects sorted by Last Name
    eid = Exams.objects.get(id=eid) # Exams object with current id
    results = Result.objects.filter(exams_name=eid) # All Result objects for current Exams

    # Render Page:
    return render(request, 'students/results_result.html', {'students':students,'results':results,'eid':eid})

def result_view(request, eid, sid):
    ''' View Result method '''
    eid = Exams.objects.get(id=eid) # Get current Exams
    sid = Student.objects.get(id=sid) # Get current Student
    # Check if Student have mark:
    try:
        # Student have mark == YES:
        result = Result.objects.get(exams_name=eid,student=sid) # return Result objects
    except Exception:
        # Student have mark == NO:
        result = 'Not Result' # return error as result

    # Render Page:
    return render(request, 'students/result_view.html',{'eid':eid,'sid':sid,'result':result})
