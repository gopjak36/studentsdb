# -*- coding: utf-8 -*-
from ..models import Exams, Group

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from datetime import datetime

from django.views.generic.edit import CreateView
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

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

class ExamsForm(ModelForm):

    class Meta:
        model = Exams

    def __init__(self,*args,**kwargs):
        super(ExamsForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        # Tag atribute for Form:

        # Ckeck with what form we work:
        try:
            # Edit Group Form:
            self.helper.form_action = reverse('exmas_edit',kwargs={'pk':kwargs['instance'].id})
        except:
            # Add Group Form:
            self.helper.form_action = reverse('exams_add')

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # Fields propertiies for Form:
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # Stucture of Form:
        self.helper.layout = Layout(
            'title',
            'group_name',
            'lecture',
            'datetime',
            'notes',
            # Button for Form:
            Submit('add_button', u'Зберегти', css_class='btn btn-primary'),
            Submit('cancel_button', u'Скасувати', css_class='btn btn-danger'),
        )


class ExamsCreateView(CreateView):
    model = Exams # Model for Add Exams
    template_name = 'students/exams_add.html' # Template for Add Exams
    form_class = ExamsForm # Style for add Exams Form

    # Add Button == Push and ValidationErrors == False:
    def get_success_url(self):
        #redirect to exams list with success message:
        return u"%s?status_message=Іспит %s успішно додано!" % (reverse('exams_list'), self.object)

    def post(self, request, *args, **kwargs):
        # Cancle_button == PUSH
        if request.POST.get('cancel_button'):
            # redirect to exams list with cancel message:
            return HttpResponseRedirect(u"%s?status_message=Додавання Іспиту скасовано!" % reverse('exams_list'))
        else:
            # initial Form render:
            return super(ExamsCreateView, self).post(request,*args,**kwargs)

def exams_edit(request,eid):
    ''' Exams Edit method '''
    # Method == POST:
    if request.method == 'POST':
        # Add_button == PUSH:
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
            time = request.POST.get('datetime')
            if not time:
                errors['datetime'] = u"Дата Іспиту є є обов’язковою"
            else:
                try:
                    time = datetime.strptime(time, '%Y-%m-%d %H:%M')
                except ValueError:
                    errors['datetime'] = u"Введіть коректний формат дати (Наприклад: 2017-9-25 9:30)"
                else:
                    data['datetime'] = time

            # Not errors:
            if not errors:
                # update data in Exams object:
                Exams.objects.filter(pk=eid).update(**data)
                # redirect to exams page with success mwssage:
                return HttpResponseRedirect(u'%s?status_message=Іспит %s успішно збережено!' % (reverse('exams_list'), title))
            # Yes errors:
            else:
                # redirect form with errors and previus input data:
                return render(request, 'students/exams_edit.html',{'eid': eid,
                                                                  'exams': Exams(**data),
                                                                  'groups': Group.objects.all().order_by('title'),
                                                                  'errors': errors})
        # Cancel_button == PUSH:
        elif request.POST.get('cancel_button') is not None:
            # redirect to exams list with cancel status message:
            return HttpResponseRedirect(u'%s?status_message=Редагування Іспиту скасовано!' % reverse('exams_list'))
    # Method != POST:
    else:
        # help variables for current_group, because can't auto select current group:
        # !!! Initial Form is't method POST !!!
        current_exams = Exams.objects.get(id=eid) # current Exams
        current_group = current_exams.group_name # current Group
        # Initial Exams Form:
        return render(request, 'students/exams_edit.html', {'eid': eid,
                                                           'exams': current_exams,
                                                            'groups': Group.objects.all().order_by('title'),
                                                            'current_group': current_group} )

def exams_delete(request,eid):
    ''' Exams Delete method '''
    # Form POST == YES:
    if request.method == 'POST':
        # delete_button = PUSH:
        if request.POST.get('delete_button') is not None:
            # get select group object:
            exams = Exams.objects.get(pk=eid)
            # delete select group from database:
            exams.delete()
            # redirect to groups page with success message:
            return HttpResponseRedirect(u'%s?status_message=Іспит %s успішно видалено!' % (reverse('exams_list'), exams.title))

        # cancel_button = PUSH:
        elif request.POST.get('cancel_button') is not None:
            # redirect to groups page with cancel status message:
            return HttpResponseRedirect(u"%s?status_message=Видалення Іспиту скасовано!" % reverse('exams_list'))
    else:
        # initial Form render:
        return render(request, 'students/exams_delete.html', {'exams': Exams.objects.get(pk=eid)})
