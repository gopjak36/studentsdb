# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic.edit import CreateView
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

class GroupCreateView(CreateView):
    model = Group # Model for add Group
    template_name = 'students/groups_add.html' # Template for form

    # Add_button == PUSH and not ValidationErrors:
    def get_success_url(self):
        # redirect to groups page with success message:
        return u"%s?status_message=Групу %s успішно додано!" % (reverse('groups'), self.object)

    def post(self, request, *args, **kwargs):
        # Cancle_button == PUSH
        if request.POST.get('cancel_button'):
            # redirect to groups page with cancel message:
            return HttpResponseRedirect(u"%s?status_message=Додавання скасовано!" % reverse('groups'))
        else:
            # initial Form render:
            return super(GroupCreateView, self).post(request,*args,**kwargs)



def groups_edit(request, gid):
    ''' Edit groups method '''
    # Form POST == YES:
    if request.method == 'POST':
        # add_button == PUSH:
        if request.POST.get('add_button') is not None:
            # errors collection:
            errors = {}
            # don't validate group data:
            data = {'notes': request.POST.get('notes')}
            # Title validation:
            title = request.POST.get('title')
            if not title:
                errors['title'] = u"Назва є обов'язковою"
            else:
                data['title'] = title
            # Leader validation:
            leader = request.POST.get('leader')
            if not leader:
                errors['leader'] = u"Оберіть старосту для групи"
            else:
                # Validation Leader group:
                leader = Student.objects.get(pk=request.POST['leader'])
                # Student have group == NO:
                if not leader.student_group:
                    errors['leader'] = u"Студент не може бути старостою, бо не належить до жодної групи"
                # Student group title (behove) == title:
                elif leader.student_group.title != title:
                    errors['leader'] = u"Студент не може бути старостою, бо не належить до даної групи"
                else:
                    data['leader'] = leader
            if not errors:
                # update date in group:
                Group.objects.filter(pk=gid).update(**data)
                # redirect to groups page with success status message:
                return HttpResponseRedirect(u'%s?status_message=Группу %s успішно збережено!' % (reverse('groups'), title))
            else:
                # redirect form with errors and previus user input:
                return render(request, 'students/groups_edit.html', {'group': Group(**data),
                                                                    'students': Student.objects.all().order_by('last_name'),
                                                                    'errors': errors,
                                                                    'gid': gid})
        # cancel_button == PUSH:
        elif request.POST.get('cancel_button') is not None:
            # redirect to groups page with cancel status message:
            return HttpResponseRedirect(u'%s?status_message=Редагування скасовано!' % reverse('groups'))
    # Form POST == NO:
    else:
        # Initial Form render:
        return render(request, 'students/groups_edit.html', {'group':Group.objects.get(pk=gid),
                                                            'students': Student.objects.all().order_by('last_name')})

def groups_delete(request, gid):
    ''' Delete groups method '''
    # Form POST == YES:
    if request.method == 'POST':
        # delete_button = PUSH:
        if request.POST.get('delete_button') is not None:
            # get select group object:
            group = Group.objects.get(pk=gid)
            # delete select group from database:
            group.delete()
            # redirect to groups page with success message:
            return HttpResponseRedirect(u'%s?status_message=Групу %s успішно видалено!' % (reverse('groups'), group))

        # cancel_button = PUSH:
        elif request.POST.get('cancel_button') is not None:
            # redirect to groups page with cancel status message:
            return HttpResponseRedirect(u"%s?status_message=Видалення групи скасовано!" % reverse('groups'))
    else:
        # initial Form render:
        return render(request, 'students/groups_config_delete.html', {'group': Group.objects.get(pk=gid)})
