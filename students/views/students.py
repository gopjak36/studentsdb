# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

            # TODO: validate input from user
            errors = {}

            if not errors:
                # create student object
                student = Student(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    middle_name=request.POST['middle_name'],
                    birthday=request.POST['birthday'],
                    ticket=request.POST['ticket'],
                    student_group=Group.objects.get(pk=request.POST['student_group']),
                    photo=request.FILES['photo'],
                )

                # save student to database
                student.save()

                #redirext user to student list
                return HttpResponseRedirect(reverse('home'))

            else:
                # redirect form with errors and previus user input
                return render(request, 'students/students_add.html',
                       {'group': Groups.objects.all().order_by('title'),
                        'errors': errors })

        # Form cancel burron clicked?
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page
            return HttpResponseRedirect(reverse('home'))
    else:
        # inital form render
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
