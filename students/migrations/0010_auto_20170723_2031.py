# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_auto_20170723_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='\u041d\u0430\u0437\u0432\u0430 \u0406\u0441\u043f\u0438\u0442\u0443')),
                ('lecture', models.CharField(max_length=256, verbose_name='\u0412\u0438\u043a\u043b\u0430\u0434\u0430\u0447')),
                ('datetime', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0442\u0430 \u0427\u0430\u0441')),
                ('notes', models.TextField(verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0456 \u043d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True)),
                ('group_name', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0413\u0440\u0443\u043f\u0430 \u0434\u043b\u044f \u0406\u0441\u043f\u0438\u0442\u0443', to='students.Group', null=True)),
            ],
            options={
                'verbose_name': '\u0406\u0441\u043f\u0438\u0442',
                'verbose_name_plural': '\u0406\u0441\u043f\u0438\u0442\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='journal',
            name='student',
        ),
        migrations.DeleteModel(
            name='Journal',
        ),
    ]
