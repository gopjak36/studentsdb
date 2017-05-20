# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from ..models import Journal

# Views For Journal

def journal_list(request):
    journal = Journal.objects.all()
    return render(request, 'students/journal_list.html', {'journal': journal})
