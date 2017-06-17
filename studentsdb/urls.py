from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG
from students.views.students import StudentCreateView, StudentUpdateView, StudentDeleteView
from students.views.contact_admin import ContactView

urlpatterns = patterns('',
    # Students urls
    url(r'^$', 'students.views.students_list', name='home'),

    # Add Student Form urls
    url(r'^students/add/$', StudentCreateView.as_view(), name='students_add'),

    # Edit Student Form urls
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name="students_edit"),

    # Delete Student urls
    url(r'^students/(?P<pk>\d+)/delete/$',StudentDeleteView.as_view(), name='students_delete'),

    # Groups urls
    url(r'^groups/$', 'students.views.groups_list', name='groups'),
    url(r'^groups/add/$', 'students.views.groups_add', name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit/$','students.views.groups_edit', name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$','students.views.groups_delete', name='groups_delete'),

    # Journal urls
    url(r'^journal/$', 'students.views.journal_list', name="journal"),

    # Exam urls
    url(r'^exams/$', 'students.views.exams_list', name="exams"),

    # Result urls
    url(r'^result/$', 'students.views.results_list', name="results"),

    # Contact Admin Form urls
    url(r'^contact-admin/$', ContactView.as_view(), name='contact_admin'),

    url(r'^admin/', include(admin.site.urls)),
)

# MEDIA urls
if DEBUG:
    # server files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT}))
