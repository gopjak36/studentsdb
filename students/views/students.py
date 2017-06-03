# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from ..models import Student, Group

#Views for Students

def students_list(request):
    students = Student.objects.all()

    # Order By students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # Paginator students list
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        students = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g 9999), delivery last page of result
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    # Form posted?
    if request.method == "POST":

        # Form add button clicked?
        if request.POST.get('add_button') is not None:

            # errors collection
            errors = {}

            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # Validate user input

            # First name validate
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім’я є обов’язковим"
            else:
                data['first_name'] = first_name

            # Last name validate
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов’язковим"
            else:
                data['last_name'] = last_name

            # Birthday validate
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов’язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday

            # Ticket validate
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов’язковим"
            else:
                    data['ticket'] = ticket

            # Student Group validate
            student_group = request.POST.get('student_group','').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) !=1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]

            # Photo validate
            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo

            # Validate form fo errors
            if not errors:
                # create student object
                student = Student(**data)

                # save student to database
                student.save()

                # redirect user to student list
                return HttpResponseRedirect(u'%s?status_message=Студента успішно додано!' % reverse('home'))

            else:
                # render form with errors and previus user input
                return render(request, 'students/students_add.html',
                       {'groups': Group.objects.all().order_by('title'),
                        'errors': errors })

        # Form cancel burron clicked?
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page
            return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
    else:
        # inital form render
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
