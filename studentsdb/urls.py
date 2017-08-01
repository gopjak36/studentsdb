from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG
from students.views.students import StudentCreateView, StudentUpdateView
from students.views.groups import GroupCreateView, GroupEditView, GroupDeleteView
from students.views.journal import JournalView
from students.views.contact_admin import ContactView
from students.views.exams import ExamsCreateView, ExamsEditView, ExamsDeleteView

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
    url(r'^groups/add/$', GroupCreateView.as_view() , name='groups_add'),

    # Edit Group url:
    url(r'^groups/(?P<pk>\d+)/edit/$',GroupEditView.as_view(), name='groups_edit'),

    # Delete Group url:
    url(r'^groups/(?P<pk>\d+)/delete/$',GroupDeleteView.as_view(), name='groups_delete'),

    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name="journal"),

    # Exams urls
    url(r'^exams/$', 'students.views.exams_list', name="exams_list"),

    # Add Exams urls
    url(r'^exams/add/$', ExamsCreateView.as_view() , name="exams_add"),

    # Edit Exams urls
    url(r'^exams/(?P<pk>\d+)/edit/$', ExamsEditView.as_view() , name="exams_edit"),

    # Delete Exams urls
    url(r'^exams/(?P<pk>\d+)/delete/$', ExamsDeleteView.as_view() , name="exams_delete"),

    # Contact Admin Form url:
    url(r'^contact-admin/$', ContactView.as_view(), name='contact_admin'),

    # Results urls
    url(r'^results/$', 'students.views.results_list', name="results_list"),

    # Result urls
    url(r'^result/(?P<eid>\d+)/$', 'students.views.results_result', name="results_result"),

    # Result View urls
    url(r'^result/(?P<eid>\d+)/(?P<sid>\d+)/view/$', 'students.views.result_view', name="result_view"),

    # Admin Panel url:
    url(r'^admin/', include(admin.site.urls)),
)

# MEDIA urls
if DEBUG:
    # server files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT}))
