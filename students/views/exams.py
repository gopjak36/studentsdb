# -*- coding: utf-8 -*-
from ..models import Exams

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def exams_list(request):
    ''' Exams List method '''
    exams = Exams.objects.all() # Exams models

    # Order By Exams:
    order_by = request.GET.get('order_by')
    if order_by in ('id', 'title', 'group_name', 'datetime'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse') == '1':
            exams = exams.reverse()

    # Pagination Exams:
    paginator = Paginator(exams, 3) # Show 3 contacts per page
    page = request.GET.get('page')
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        exams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        exams = paginator.page(paginator.num_pages)

    # initial all Exams:
    return render(request, 'students/exams_list.html', {'exams': exams})
