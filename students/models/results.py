# -*- coding: utf-8 -*-

from django.db import models

class Result(models.Model):
    ''' Result of Exams '''

    class Meta(object):
        verbose_name = u"Результат"
        verbose_name_plural = u"Результати"

    exams_name = models.ForeignKey('Exams',
                    blank=False,
                    null=True,
                    on_delete=models.SET_NULL,
                    verbose_name=u"Назва Іспиту")

    student = models.ForeignKey('Student',
                    blank=False,
                    null=True,
                    on_delete=models.SET_NULL,
                    verbose_name=u"Студент")

    ''' Generation Avaliable Marks for Result of Exam '''
    MARKS = zip( range(1,41), range(1,41) )

    mark = models.IntegerField(
                    max_length=2,
                    choices=MARKS,
                    blank=False,
                    null=True,
                    verbose_name=u"Оцінка")

    def __unicode__(self):
        return u"%s (%s) - %s" % (self.student, self.exams_name, self.mark)
