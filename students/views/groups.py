# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic.edit import CreateView
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

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

class GroupForm(ModelForm):

    class Meta:
        model = Group

    def __init__(self,*args,**kwargs):
        super(GroupForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        # Tag atribute for Form:

        # Ckeck with what form we work:
        try:
            # Edit Group Form:
            self.helper.form_action = reverse('groups_edit',kwargs={'pk':kwargs['instance'].id})
        except:
            # Add Group Form:
            self.helper.form_action = reverse('groups_add')

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # Fields propertiies for Form:
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # Stucture of Form:
        self.helper.layout = Layout(
            'title',
            'leader',
            'notes',
            # Button for Form:
            Submit('add_button', u'Зберегти', css_class='btn btn-primary'),
            Submit('cancel_button', u'Скасувати', css_class='btn btn-danger'),
        )


class GroupCreateView(CreateView):
    model = Group # Model for add Group
    template_name = 'students/groups_add.html' # Template for Form
    form_class = GroupForm # style of form

    # Add_button == PUSH and not ValidationErrors:
    def get_success_url(self):
        # redirect to groups page with success message:
        return u"%s?status_message=Групу %s успішно додано!" % (reverse('groups'), self.object)

    def form_valid(self, form):
        # User Input group data == FALSE:
        if form.cleaned_data['leader'] is not None:
            # Leader have group == FALSE:
            if form.cleaned_data['leader'].student_group is None:
                # Add Error message:
                form.add_error('leader','Студент не може бути старостою, бо не належить до жодної групи')
                # Return Invalid Form:
                return self.form_invalid(form)
            # Leader is in other group == TRUE:
            elif form.cleaned_data['leader'].student_group.title != form.cleaned_data['title']:
                # Add Error message:
                form.add_error('leader','Студент не може бути старостою, бо не належить до даної групи')
                # Return Invalid Form:
                return self.form_invalid(form)
        # initial Form:
        return super(GroupCreateView,self).form_valid(form)

    def post(self, request, *args, **kwargs):
        # Cancle_button == PUSH
        if request.POST.get('cancel_button'):
            # redirect to groups page with cancel message:
            return HttpResponseRedirect(u"%s?status_message=Додавання скасовано!" % reverse('groups'))
        else:
            # initial Form render:
            return super(GroupCreateView, self).post(request,*args,**kwargs)

class GroupEditView(UpdateView):
    model = Group # model for edit Group
    template_name = 'students/groups_edit.html' # template for Form
    form_class = GroupForm # style of form

    # Add_button == PUSH:
    def get_success_url(self):
        # redirect to groups page with succes message:
        return u"%s?status_message=Групу %s успішно збережено!" % (reverse('groups'), self.object.title)

    def form_valid(self, form):
        # User Input group data == FALSE:
        if form.cleaned_data['leader'] is not None:
            # Leader have group == FALSE:
            if form.cleaned_data['leader'].student_group is None:
                # Add Error message:
                form.add_error('leader','Студент не може бути старостою, бо не належить до жодної групи')
                # Return Invalid Form:
                return self.form_invalid(form)
            # Leader is in other group == TRUE:
            elif form.cleaned_data['leader'].student_group.title != form.cleaned_data['title']:
                # Add Error message:
                form.add_error('leader','Студент не може бути старостою, бо не належить до даної групи')
                # Return Invalid Form:
                return self.form_invalid(form)
        # initial Form:
        return super(GroupEditView,self).form_valid(form)

    def post(self,request,*args,**kwargs):
        # cancel_button == PUSH:
        if request.POST.get('cancel_button'):
            # redirect to groups page with cancel message:
            return HttpResponseRedirect(u"%s?status_message=Редагування скасовано!" % reverse('groups'))
        else:
            # initial Form render:
            return super(GroupEditView, self).post(request,*args,**kwargs)


class GroupDeleteView(DeleteView):
    model = Group # model for delete Group
    template_name = 'students/groups_config_delete.html' # template for Form

    # delete_button = PUSH:
    def get_success_url(self):
        # redirect to groups page with success message:
        return u'%s?status_message=Групу %s успішно видалено!' % (reverse('groups'), self.object)

    def post(self,request,*args,**kwargs):
        # cancel_button = PUSH:
        if request.POST.get('cancel_button'):
            # redirect to groups page with cancel status message:
            return HttpResponseRedirect(u"%s?status_message=Видалення групи скасовано!" % reverse('groups'))
        else:
            return super(GroupDeleteView, self).post(request,*args,**kwargs)
