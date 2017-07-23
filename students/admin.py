# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Student, Group, MonthJournal, Exams
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        ''' Chek if student leader in any group '''

        # get group where current student in a leader:
        groups = Group.objects.filter(leader=self.instance)

        # Check if student leader in other groups
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u"Студент є старостою іншої группи", code="invalid")

        return self.cleaned_data['student_group']

    def clean_photo(self):
        ''' Check student upload files  '''

        # ckeck if user upload new file:
        if self.cleaned_data['photo']:
            try:
                # get content file of upload photo:
                photo = self.cleaned_data['photo'].content_type.split('/')[1]
                # raise error if file not png or jpge format:
                if not(photo == 'png' or photo == 'jpeg'):
                    raise ValidationError('Це не фото файл')
                # raise error if file size is more then 2 Мb:
                elif self.cleaned_data['photo'].size > 200000:
                    raise ValidationError('Фото більше 2 Мб')
            # if photo yet selected:
            except AttributeError:
                return self.cleaned_data['photo']
        # if photo not selected:
        else:
             return self.cleaned_data['photo']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']

    form = StudentFormAdmin

    def view_on_site(self,obj):
        return reverse('students_edit', kwargs={'pk': obj.id})

class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        ''' Check if student in correct student group '''
        try:
            # chek if leader form is empty:
            if not self.cleaned_data['leader']:
                return self.cleaned_data['leader']
            try:
                # chek if student is in other groups:
                if self.cleaned_data['leader'].student_group.title != self.cleaned_data['title']:
                    raise ValidationError('Студент не може бути старостою, бо належить до іншої групи')
                # update info about student:
                else:
                    return self.cleaned_data['leader']
            except KeyError:
                # check if user don't input title:
                raise ValidationError('Напишіть назву групи')
        # check if student is not in any group:
        except AttributeError:
            raise ValidationError('Студент не належить до груп, додайте студунта в групу')

class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_display_link = ['title']
    ordering = ['title']
    list_filter = ['title']
    list_per_page = 10
    search_fields = ['title', 'notes']

    form = GroupFormAdmin

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'gid': obj.id})

# Register Student model:
admin.site.register(Student, StudentAdmin)
# Register Group model:
admin.site.register(Group, GroupAdmin)
# Register MonthJournal model:
admin.site.register(MonthJournal)
# Register Exams model:
admin.site.register(Exams)
