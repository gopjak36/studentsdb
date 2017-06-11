from django.contrib import admin
from .models import Student, Group, Journal, Exam, Result
from django.core.urlresolvers import reverse

class StudentAdmin(admin.ModelAdmin):
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
