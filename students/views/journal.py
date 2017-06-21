# -*- coding: utf-8 -*-

from datetime import datetime, date

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from ..models import Student
from ..util import paginate

class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):

        # get context from TemplateView class:
        context = super(JournalView,self).get_context_data(**kwargs)

        # TODO: check wheter we were given month in parament,
        #       if not - calculate current
        # NOW: give back current:
        today = datetime.today()
        month = date(today.year, today.month, 1)

        # TODO: calculate current year, next and preview month
        # NOW: give back their statically:
        context['prev_month'] = '2017-05-01'
        context['next_month'] = '2017-07-01'
        context['year'] = 2017

        # TODO: also current month and verbose of month:
        # NOW: statically:
        context['cur_month'] = '2017-06-01'
        context['month_verbose'] = u"Липень"

        # TODO: calculate list of day in month
        # NOW: statically:
        context['month_header'] = [
            {'day': 1, 'verbose': 'Пн'},
            {'day': 2, 'verbose': 'Вт'},
            {'day': 3, 'verbose': 'Ср'},
            {'day': 4, 'verbose': 'Чт'},
            {'day': 5, 'verbose': 'Пт'}]

        # extract all students and ordered by last name:
        queryset = Student.objects.order_by('last_name')

        # link for AJAX request:
        update_url = reverse('journal')

        # collect necressary data dor all students:
        students = []
        for student in queryset:

            #TODO: extract journal for student and current month

            # coolect days for student:
            days = []
            for day in range(1,31):
                days.append({
                    'day': day,
                    'present': True,
                    'date': date(2017, 6, day).strftime('%Y-%m-%d'),
                })

            # collect the rest data for student:
            students.append({
                'fullname': u"%s %s" % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        # apply pagination for students list:
        context = paginate(students, 10, self.request, context, var_name='students')

        # return update dictionary:
        return context
