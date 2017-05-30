# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from ..models import Journal

# Views For Journal

def journal_list(request):
    journal = Journal.objects.all()

    # Order By journal list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id',):
        journal = journal.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            journal = journal.reverse()

    return render(request, 'students/journal_list.html', {'journal': journal})
