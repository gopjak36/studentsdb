# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_auto_20170731_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mark', models.CharField(max_length=2, null=True, verbose_name='\u041e\u0446\u0456\u043d\u043a\u0430', choices=[(5, b'A'), (4, b'B'), (3, b'C'), (2, b'D'), (1, b'E')])),
                ('exams_name', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u041d\u0430\u0437\u0432\u0430 \u0406\u0441\u043f\u0438\u0442\u0443', to='students.Exams', null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Student', null=True)),
            ],
            options={
                'verbose_name': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442',
                'verbose_name_plural': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0438',
            },
            bases=(models.Model,),
        ),
    ]
