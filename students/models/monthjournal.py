# -*- coding: utf-8 -*-

from django.db import models

class MonthJournal(models.Model):
    ''' Student Monthly Journal '''

    class Meta:
        verbose_name = u'Місячний Журнал'
        verbose_name_plural = u'Місячні Журнали'

    student = models.ForeignKey('Student',
        verbose_name=u'Студент',
        blank=False,
        unique_for_month='date')

    # we only need year and month, so always set day to first day of the month:
    date = models.DateField(
        verbose_name=u'Дата',
        blank=False)

    def __unicode__(self):
        return u"%s: %d %d" % (self.student.last_name, self.date.month, self.date.year)

# list of days, each says whether student was present or not:
for num in range(1, 32):
    MonthJournal.add_to_class('present_day'+str(num), models.BooleanField(default=False))
