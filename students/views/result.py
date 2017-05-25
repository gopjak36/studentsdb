# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from ..models import Result

# Views for esult

def results_list(request):
    results = Result.objects.all()

    return render(request, 'students/results_list.html', {'results':results})
