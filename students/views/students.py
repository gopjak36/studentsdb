# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView, CreateView
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions

# switch on status message:
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin  # use for success message in CreateView

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

class StudentViewForm(ModelForm):
    class Meta:
        model = Student

    def __init__(self,*args,**kwargs):
        super(StudentViewForm, self).__init__(*args,**kwargs)

        self.helper = FormHelper(self)

        # set form tag attribute
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = False
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'middle_name',
            'birthday',
            'photo',
            'ticket',
            'student_group',
            'notes',
            Submit('add_button', u'Зберегти', css_class='btn btn-primary'),
            Submit('cancel_button', u'Скасувати', css_class='btn btn-link'),
        )

class StudentCreateView(SuccessMessageMixin, CreateView):
    model = Student
    template_name = 'students/students_add.html'
    form_class = StudentViewForm
    # status message of add student:
    success_message = 'Студента успішно додано!'
    success_url = '/'

    def form_valid(self,form):

        ''' Validate photo size '''
        # chek if photo data empty, if empty don't validate photo:
        if form.cleaned_data['photo']:
            # ckeck if photo size > 2 Mb:
            if form.cleaned_data['photo'].size > 2000000:
                # add error to form:
                form.add_error('photo','Фото повинно бути менше 2 МБ')
                # return error:
                return self.form_invalid(form)

        return super(StudentCreateView,self).form_valid(form)

    def post(self,request,*args,**kwargs):
        # check what user click:
        if request.POST.get('cancel_button'):
            # status message of cancel add stduent:
            messages.error(request,'Додавання студента скасовано!')
            # if push cancel button redirect to homepage:
            return HttpResponseRedirect( reverse('home') )
        else:
            # if push else button save data and get_success_url:
            return super(StudentCreateView,self).post(request,*args,**kwargs)

class StudentUpdateView(SuccessMessageMixin, UpdateView):
    model= Student
    template_name = 'students/students_edit.html'
    form_class = StudentViewForm
    success_url = '/'
    # status message of update student form:
    success_message = 'Студена успішно збережено!'


    def form_valid(self, form):

        ''' Validate leader '''
        # get groups when studnet is leader:
        groups = Group.objects.filter(leader=form.instance)
        # check if student leader in other groups:
        if len(groups) > 0 and form.cleaned_data['student_group'] != groups[0]:
            # add error to form:
            form.add_error('student_group','Студент є старостою іншої группи, а саме %s групи' % groups[0])
            # return error:
            return self.form_invalid(form)

        ''' Validate photo size '''
        # chek if photo data empty, if empty don't validate photo:
        if form.cleaned_data['photo']:
            # ckeck if photo size > 2 Mb:
            if form.cleaned_data['photo'].size > 2000000:
                # add error to form:
                form.add_error('photo','Фото повинно бути менше 2 МБ')
                # return error:
                return self.form_invalid(form)

        return super(StudentUpdateView,self).form_valid(form)

    def post(self,request,*args,**kwargs):
        if request.POST.get('cancel_button'):
            # status message of cancel edit student:
            messages.error(request,'Рудагуваня студента відмінено!')
            # redirect to home page:
            return HttpResponseRedirect( reverse('home') )
        else:
            return super(StudentUpdateView, self).post(request,*args,**kwargs)

def students_delete(request,id):
    ''' Method delete students '''

    # if click delete button:
    if request.POST.get('delete_button'):
        obj = Student.objects.get(pk=id) # get object id:
        obj.delete() # delete this object:
        # add status message of delete student:
        messages.error(request, 'Студента успішно видалено!')
        return HttpResponseRedirect(reverse('home'))# redirect to homepage:
    # if click cancel delete:
    elif request.POST.get('cancel_button'):
        # status message of cancel delete student:
        messages.error(request,'Видалення студента скасовано!')
        return HttpResponseRedirect(reverse('home'))# redirect to homtpage:
    # get information, about template and id:
    else:
        return render(request, 'students/students_config_delete.html', {'id':id})
