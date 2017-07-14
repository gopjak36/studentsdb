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
            # errors collection:
            errors ={}
            # don't validate student data:
            data = {'notes': request.POST.get('notes')}
            # Title validate:
            title = request.POST.get('title').strip()
            if not title:
                errors['title'] = u"Назва є обов'язковою"
            else:
                data['title'] = title
            # Leader validate:
            leader = request.POST.get('leader')
            if not leader:
                errors['leader'] = u"Оберіть старосту для групи "
            else:
                leader = Student.objects.get(pk=request.POST['leader'])
                data['leader'] = leader
            if not errors:
                # create new group object:
                group = Group(**data)
                # save group to database:
                group.save()
                # redirect to group list and success status message:
                return HttpResponseRedirect(u'%s?status_message=Групу %s успішно додано!' % (reverse('groups'), title))
            else:
                # redirect form with erros and previus user input:
                return render(request, 'students/groups_add.html', {'students': Student.objects.all().order_by('last_name'),
                                                                    'errors': errors})
        # cancel_button == push:
        elif request.POST.get('cancel_button') is not None:
            # redirect to group_list and cancel status message:
            return HttpResponseRedirect(u'%s?status_message=Додавання скасовано!' % reverse('groups'))
    # Form POST == NO:
    else:
        # initial form render:
        return render(request, 'students/groups_add.html', {'students': Student.objects.all().order_by('last_name')})

def groups_edit(request, gid):
    # Form POST == YES:
    if request.method == 'POST':
        # add_button == PUSH:
        if request.POST.get('add_button') is not None:
            # TODO: errors validation:
            errors = {}
            if not errors:
                # update date in group:
                Group.objects.filter(pk=gid).update(
                    title = request.POST.get('title'),
                    leader = Student.objects.get(pk=request.POST['leader']),
                    notes = request.POST.get('notes')
                )

                # redirect to groups page:
                return HttpResponseRedirect(reverse('groups'))
            else:
                # redirect form with errors and previus user input:
                return render(reqeust, 'students/groups_edit', {'group':Group.objects.get(pk=gid),
                                                                'students': Student.objects.all().order_by('last_name'),
                                                                'errors': errors})
        # cancel_button == PUSH:
        if request.POST.get('cancel_button') is not None:
            # redirect to groups page:
            return HttpResponseRedirect(reverse('groups'))
    # Form POST == NO:
    else:
        # Initial Form render:
        return render(request, 'students/groups_edit.html', {'group':Group.objects.get(pk=gid),
                                                            'students': Student.objects.all().order_by('last_name')})

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
