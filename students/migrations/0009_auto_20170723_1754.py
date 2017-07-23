# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_monthjournal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='group',
        ),
        migrations.RemoveField(
            model_name='result',
            name='name_of_exam',
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
        migrations.RemoveField(
            model_name='result',
            name='student',
        ),
        migrations.DeleteModel(
            name='Result',
        ),
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0413\u0440\u0443\u043f\u0430', blank=True, to='students.Group', null=True),
            preserve_default=True,
        ),
    ]
