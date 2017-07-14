from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG
from students.views.students import StudentCreateView, StudentUpdateView
from students.views.journal import JournalView
from students.views.contact_admin import ContactView

urlpatterns = patterns('',
    # Students urls
    url(r'^$', 'students.views.students_list', name='home'),

    # Add Student Form urls
    url(r'^students/add/$', StudentCreateView.as_view(), name='students_add'),

    # Edit Student Form urls
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name="students_edit"),

    # Delete Student urls
    url(r'^students/(?P<id>\d+)/delete/$','students.views.students_delete', name='students_delete'),

    # Groups url:
    url(r'^groups/$', 'students.views.groups_list', name='groups'),

    # Add Group url:
    url(r'^groups/add/$', 'students.views.groups_add', name='groups_add'),

    # Edit Group url:
    url(r'^groups/(?P<gid>\d+)/edit/$','students.views.groups_edit', name='groups_edit'),

    # Delete Group url:
    url(r'^groups/(?P<gid>\d+)/delete/$','students.views.groups_delete', name='groups_delete'),

    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name="journal"),

    # Exam urls
    url(r'^exams/$', 'students.views.exams_list', name="exams"),

    # Result urls
    url(r'^result/$', 'students.views.results_list', name="results"),

    # Contact Admin Form url:
    url(r'^contact-admin/$', ContactView.as_view(), name='contact_admin'),

    # Admin Panel url:
    url(r'^admin/', include(admin.site.urls)),
)

# MEDIA urls
if DEBUG:
    # server files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT}))
