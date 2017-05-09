# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

#Views for Students

def students_list(request):
    students = (
        {'id':1,
         'first_name': u'Віталій',
         'second_name': u'Подоба',
         'ticket':2123,
         'image': 'img/me.jpeg'},
         {'id':2,
          'first_name': u'Василь',
          'second_name': u'Петрович',
          'ticket':1988,
          'image': 'img/piv.png'},
         {'id':3,
          'first_name': u'Корост',
          'second_name': u'Андрій',
          'ticket': 2001,
          'image':'img/podoba3.jpg'},
    )
    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    return HttpResponse('<h1>Students Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

# Views For Groups

def groups_list(request):
    groups = (
        {'id':1,
         'name': u'МтМ-21',
         'leader': u'Подоба Вітілій'},
        {'id':2,
         'name': u'МтМ-22',
         'leader': u'Корост Андрій'},
        {'id':3,
         'name': u'МтМ-23',
         'leader': u'Петрович Василь'},
    )
    return render(request, 'students/groups_list.html',{'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
