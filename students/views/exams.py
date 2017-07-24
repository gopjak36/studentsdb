# -*- coding: utf-8 -*-
from ..models import Exams, Group

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from datetime import datetime

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

def exams_add(request):
    ''' Exams Add method '''
     # Form POST == YES:
    if request.method == 'POST':
        # add_button == PUSH:
        if request.POST.get('add_button') is not None:
            errors = {} # errors collection
            data = {'notes': request.POST.get('notes')} # data collection

            # Validation data:

            # Title validation:
            title = request.POST.get('title')
            if not title:
                errors['title'] = u" Назва Іспиту є є обов’язковою"
            else:
                data['title'] = title
            # Group name validation:
            group_name = request.POST.get('group_name')
            if not group_name:
                errors['group_name'] = u" Оберіть групу для іспиту"
            else:
                data['group_name'] = Group.objects.get(pk=group_name)
            # Lecture validatin:
            lecture = request.POST.get('lecture')
            if not lecture:
                errors['lecture'] = u" Викладач для Іспиту є є обов’язковим"
            else:
                data['lecture'] = lecture
            # DataTime validation:
            time = request.POST.get('datetime').strip()
            if not datetime:
                errors['datetime'] = u"Дата Іспиту є є обов’язковою"
            else:
                try:
                    datetime.strptime(time, '%Y-%m-%d %H:%M')
                except ValueError:
                    errors['datetime'] = u"Введіть коректний формат дати (Наприклад: 2017-9-25 9:30)"
                else:
                    data['datetime'] = time

            # Not errors:
            if not errors:
                # create Exams object:
                exams = Exams(**data)
                # save exam in database:
                exams.save()
                # redirect to exams page with success mwssage:
                return HttpResponseRedirect(u'%s?status_message=Іспит %s успішно додано!' % (reverse('exams_list'), exams.title))
            # Yes errors:
            else:
                # redirect form with errors and previus input data:
                return render(request, 'students/exams_add.html',{'groups': Group.objects.all(),'errors': errors})
        # cancel_button == PUSH:
        elif request.POST.get('cancel_button') is not None:
            # redirect to exams page with cancel message:
            return HttpResponseRedirect(u'%s?status_message=Додавання Іспиту скасовано!' % reverse('exams_list'))
    # Form POST == NO:
    else:
        # initial form:
        return render(request, 'students/exams_add.html',{'groups': Group.objects.all()})
