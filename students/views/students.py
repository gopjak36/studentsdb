# -*- coding: utf-8 -*-
from django.shortcuts import render
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
        self.helper.help_text_inline = True
        self.helper.html5_required = True
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

class StudentCreateView(CreateView):
    model = Student
    template_name = 'students/students_add.html'
    form_class = StudentViewForm

    def get_success_url(self):
        return reverse('home')

    def post(self,request,*args,**kwargs):
        # check what user click:
        if request.POST.get('cancel_button'):
            # if push cancel button redirect to homepage:
            return HttpResponseRedirect( reverse('home') )
        else:
            # if push else button save data and get_success_url:
            return super(StudentCreateView,self).post(request,*args,**kwargs)

class StudentUpdateView(UpdateView):
    model= Student
    template_name = 'students/students_edit.html'
    form_class = StudentViewForm

    def get_success_url(self):
        return reverse('home')

    # TODO: Fix bag with valid photo    
    '''
    def form_valid(self, form):
        # check photo size in stduent edit form:
        if form.cleaned_data['photo'].size > 2000000:
            # message with error:
            form.add_error('photo', 'Фото повинно бути менше 2 МБ' )
            return self.form_invalid(form)
        return super(StudentUpdateView, self).form_valid(form)
        '''
    def post(self,request,*args,**kwargs):
        if request.POST.get('cancel_button'):
            # status message of cancel edit student:
            messages.error(request,'Рудагуваня студента відмінено!')
            # redirect to home page:
            return HttpResponseRedirect( reverse('home') )
        else:
            # statuc message for sabe edit student, move from get_succes_url to this place:
            messages.error(request ,'Студена успішно збережено!')
            return super(StudentUpdateView, self).post(request,*args,**kwargs)

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_config_delete.html'

    def get_success_url(self):
        return reverse('home')

    # create this section for status message:
    def post(self, request, *args, **kwargs):
        # check if push to delete button:
        if request.POST.get('delete_button'):
            # status message of delete student:
            messages.error(request, 'Студента успішно видалено!')
            # return HttpResponce object:
            return super(StudentDeleteView, self).post(request,*args,**kwargs)
'''
# Method for add Student:

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
                if not ((photo.content_type == 'image/jpeg') or (photo.content_type == 'image/png')):
                    errors['photo'] = u"Оберіть фото файл"
                else:
                    if not (photo.size < 2000000):
                        errors['photo'] = u"Фото повинно бути менше 2 МБ"
                    else:
                        data['photo'] = photo

            # Validate form fo errors
            if not errors:
                # create student object
                student = Student(**data)

                # save student to database
                student.save()

                # status message of add student with first and last name:
                messages.error(request,"Студента %s %s успішно додано!" % (str(student.first_name),str(student.last_name)))

                # redirect user to student list
                return HttpResponseRedirect( reverse('home') )

            else:
                # render form with errors and previus user input
                return render(request, 'students/students_add.html',
                       {'groups': Group.objects.all().order_by('title'),
                        'errors': errors })

        # Form cancel burron clicked?
        elif request.POST.get('cancel_button') is not None:
            # status message of cancel add student:
            messages.error(request, 'Додавання студента скасовано!')
            # redirect to home page
            return HttpResponseRedirect( reverse('home') )
    else:
        # inital form render
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})

'''
