# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultsRegister',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('view', models.BooleanField(default=False)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Exams', null=True)),
            ],
            options={
                'verbose_name': '\u0420\u0435\u0454\u0441\u0442\u0440\u0430\u0446\u0456\u044f \u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0443',
                'verbose_name_plural': '\u0420\u0435\u0454\u0441\u0442\u0440\u0430\u0446\u0456\u044f \u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0456\u0432',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='result',
            name='mark',
            field=models.IntegerField(max_length=2, null=True, verbose_name='\u041e\u0446\u0456\u043d\u043a\u0430', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40)]),
            preserve_default=True,
        ),
    ]
