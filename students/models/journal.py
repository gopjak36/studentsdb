# -*- coding: utf-8 -*-
from django.db import models

class Journal(models.Model):

    class Meta(object):
        verbose_name=u"Журнал"
        verbose_name_plural=u"Журнал"

    student = models.OneToOneField('Student',
            verbose_name=u"Студент",
            blank=False,
            null=False)

    def __unicode__(self):
            return u"%s %s" % (self.student.first_name, self.student.last_name)
