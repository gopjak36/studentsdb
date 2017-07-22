# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime

from ..models import Exam, Group

# Views for Exam

def exams_list(request):
    exams = Exam.objects.all()

    # Order By exams list
    order_by = request.GET.get('order_by', '')
    if order_by in ('name', 'groups', 'time'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    return render(request, 'students/exams_list.html', {'exams': exams})


def exams_add(request):
    ''' Add Exam method '''
    # Form POST == YES:
    if request.method == 'POST':
        # add_button == PUSH:
        if request.POST.get('add_button') is not None:
            errors = {} # errors collection
            data = {} # data collection

            # Validation data:

            # Name validation:
            name = request.POST.get('name')
            if not name:
                errors['name'] = u" Назва Іспиту є є обов’язковою"
            else:
                data['name'] = name
            # Group validation:
            group = request.POST.get('group')
            if not group:
                errors['group'] = u" Оберіть групу для іспиту"
            else:
                data['group'] = Group.objects.get(pk=group)
            # Lecturer validatin:
            lecturer = request.POST.get('lecturer')
            if not name:
                errors['lecturer'] = u" Викладач для Іспиту є є обов’язковим"
            else:
                data['lecturer'] = lecturer
            # DataTime validation:
            time = request.POST.get('time').strip()
            if not time:
                errors['time'] = u"Дата Іспиту є є обов’язковою"
            else:
                try:
                    datetime.strptime(time, '%Y-%m-%d %H:%M')
                except Exception:
                    errors['time'] = u"Введіть коректний формат дати (напр. 2017-9-25 9:30)"
                else:
                    data['time'] = time

            # Not errors:
            if not errors:
                # create Exams object:
                exam = Exam(**data)
                # save exam in database:
                exam.save()
                # redirect to exams page with success mwssage:
                return HttpResponseRedirect(u'%s?status_message=Іспит %s успішно додано!' % (reverse('exams'), exam.name))
            # Yes errors:
            else:
                # redirect form with errors and previus input data:
                return render(request, 'students/exams_add.html',{'groups': Group.objects.all(),'errors': errors})
        # cancel_button == PUSH:
        elif request.POST.get('cancel_button') is not None:
            # redirect to exams page with cancel message:
            return HttpResponseRedirect(u'%s?status_message=Додавання Іспиту скасовано!' % reverse('exams'))
    # Form POST == NO:
    else:
        # initial form:
        return render(request, 'students/exams_add.html',{'groups': Group.objects.all()})
