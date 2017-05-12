# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

# Views For Journal

def journal_list(request):
    journal = (
        {'id': 1,
         'name': u'Подоба Віталій'},
        {'id': 2,
         'name': u'Корост Андрій'},
        {'id': 3,
         'name': u'Петрович Василь'},
    )
    return render(request, 'students/journal_list.html', {'journal': journal})
