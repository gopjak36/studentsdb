# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

# Views For Journal

def journal_list(request):
    return render(request, 'students/journal_list.html', {})
