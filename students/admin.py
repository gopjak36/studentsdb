# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Student, Group, Journal, Exam, Result
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

class StudentAdmin(admin.ModelAdmin):

    form = StudentFormAdmin
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']



    def view_on_site(self,obj):
        return reverse('students_edit', kwargs={'pk': obj.id})

# Register Student model:
admin.site.register(Student, StudentAdmin)
admin.site.register(Group)
admin.site.register(Journal)
admin.site.register(Exam)
admin.site.register(Result)
