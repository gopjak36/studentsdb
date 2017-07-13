# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Group, Student

# Views For Groups

def groups_list(request):
    groups = Group.objects.all()

    # Order By groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    # Paginator groups list
    paginator = Paginator(groups,3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/groups_list.html',{'groups': groups})

def groups_add(request):

    # Form POST == YES:
    if request.method == 'POST':
        # add_button == push:
        if request.POST.get('add_button') is not None:
            # TODO: Validate input from user:
            errors ={}

            if not errors:
                # create new group object:
                group = Group(
                title=request.POST['title'],
                leader=Student.objects.get(pk=request.POST['leader']),
                notes=request.POST['notes'],
                )
                # save group to database:
                group.save()
                # redirect to group list:
                return HttpResponseRedirect(reverse('groups'))
            else:
                # redirect form with erros and previus user input:
                return render(request, 'students/groups_add.html', {'groups':Group.objects.all().order_by('last_name'),'errors': errors})
        # cancel_button == push:
        elif request.POST.get('cancel_button') is not None:
            # redirect to group_list:
            return HttpResponseRedirect(reverse('groups'))
    # Form POST == NO:
    else:
        # initial form render:
        return render(request, 'students/groups_add.html', {'students': Student.objects.all().order_by('last_name')})

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
