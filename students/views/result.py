# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from ..models import Result

# Views for esult

def results_list(request):
    results = Result.objects.all()

    # Order By result list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id',):
        results = results.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            results = results.reverse()

    return render(request, 'students/results_list.html', {'results':results})
