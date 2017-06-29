# -*- coding: utf-8 -*-

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from ..models import Student, MonthJournal
from ..util import paginate

from django.http import JsonResponse

class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):

        # get context from TemplateView class:
        context = super(JournalView,self).get_context_data(**kwargs)

        # chek if we need to display some specific month:
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'],'%Y-%m-%d').date()
        else:
            # otherwise just displaying current month data:
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # calculate current year, next and previus month detail for month navigayion element in template:
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        # variable for students pagination:
        context['cur_month'] = month.strftime('%Y-%m-%d')

        # variable dor template to generate journal table header elements:
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{
            'day': d,
            'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
            for d in range(1, number_of_days+1)]

        # extract all students and ordered by last name:
        queryset = Student.objects.order_by('last_name')

        # url to update student presence, for form post:
        update_url = reverse('journal')

        # collect necressary data for all students:
        students = []
        for student in queryset:

            # try to get journal object by month selected and current student:
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None

            # coolect days for current student:
            days = []
            for day in range(1,number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day%d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                })

            # collect the rest data for student:
            students.append({
                'fullname': u"%s %s" % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        # apply pagination for students list:
        context = paginate(students, 5, self.request, context, var_name='students')

        # return update dictionary:
        return context

    def post(self, request, *args, **kwargs):
        return JsonResponse({'key':'value'})
