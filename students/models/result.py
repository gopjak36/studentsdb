# -*- coding: utf-8 -*-
from django.db import models

class Result(models.Model):
    ''' Result Model '''

    class Meta(object):
        verbose_name = u"Результат"
        verbose_name_plural = u"Результати"

    name_of_exam = models.ForeignKey('Exam',
        verbose_name=u"Назва Іспиту",
        blank=True,
        null=True)

    student = models.ForeignKey('Student',
        verbose_name=u"Студент",
        blank=True,
        null=True)

    point = models.IntegerField(
        verbose_name=u"Оцінка",
        blank=True,
        null=True)

    def __unicode__(self):
        return u"%s - %s %s - %s" % (self.name_of_exam, self.student.first_name, self.student.last_name, self.point)
