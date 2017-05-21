# -*- coding: utf-8 -*-
from django.db import models

class Exam(models.Model):
    ''' Exam model '''

    class Meta(object):
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"

    name = models.CharField(
            verbose_name=u"Назва",
            blank=False,
            null=False,
            max_length=255)

    group = models.ForeignKey("Group",
            verbose_name=u"Група",
            blank=False,
            null=False
            )

    lecturer = models.CharField(
            verbose_name=u"Викладач",
            blank=False,
            null=False,
            max_length=255
            )

    time = models.DateTimeField(
            verbose_name=u"Час",
            blank=False,
            null=False,
            max_length=255
            )

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.group.title)
