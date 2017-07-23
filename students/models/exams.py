# -*- coding: utf-8 -*-
from django.db import models

class Exams(models.Model):
    ''' Exams Model '''

    class Meta(object):
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"


    title = models.CharField(
                max_length=256,
                blank=False,
                verbose_name=u"Назва Іспиту")

    group_name = models.ForeignKey('Group',
                blank=False,
                null=True,
                on_delete=models.SET_NULL,
                verbose_name=u"Група для Іспиту")

    lecture = models.CharField(
                max_length=256,
                blank=False,
                verbose_name=u"Викладач")

    datetime = models.DateTimeField(
                blank=False,
                verbose_name=u"Дата та Час")

    notes = models.TextField(
                blank=True,
                verbose_name=u"Додаткові нотатки")


    def __unicode__(self):
        return u"%s (%s) %s" % (self.title, self.group_name, self.datetime)
