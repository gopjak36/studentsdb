# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0010_auto_20170723_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exams',
            name='notes',
            field=models.TextField(null=True, verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0456 \u043d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True),
            preserve_default=True,
        ),
    ]
