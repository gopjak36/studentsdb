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
from crispy_forms.bootstrap import PrependedText

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
            self.helper.form_action = reverse('exams_edit',kwargs={'pk':kwargs['instance'].id})
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
            PrependedText('datetime','<span class="glyphicon glyphicon-calendar"></span>', placeholder='Наприклад: 2017-9-25 9:30'),
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

class ExamsEditView(UpdateView):
    model = Exams # Model for Edit Exams
    template_name = 'students/exams_edit.html' # Template for Edit Exams
    form_class = ExamsForm # Style for Edit Exams Form

    # Add Button == Push and ValidationErrors == False:
    def get_success_url(self):
        #redirect to exams list with success message:
        return u"%s?status_message=Іспит %s успішно збережено!" % (reverse('exams_list'), self.object)

    def post(self, request, *args, **kwargs):
        # Cancle_button == PUSH
        if request.POST.get('cancel_button'):
            # redirect to exams list with cancel message:
            return HttpResponseRedirect(u"%s?status_message=Редагування скасовано!" % reverse('exams_list'))
        else:
            # initial Form render:
            return super(ExamsEditView, self).post(request,*args,**kwargs)

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
