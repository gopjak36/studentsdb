# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_journal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430')),
                ('lecturer', models.CharField(max_length=255, verbose_name='\u0412\u0438\u043a\u043b\u0430\u0434\u0430\u0447')),
                ('time', models.DateTimeField(max_length=255, verbose_name='\u0427\u0430\u0441')),
                ('group', models.ForeignKey(verbose_name='\u0413\u0440\u0443\u043f\u0430', to='students.Group')),
            ],
            options={
                'verbose_name': '\u0406\u0441\u043f\u0438\u0442',
                'verbose_name_plural': '\u0406\u0441\u043f\u0438\u0442\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='journal',
            options={'verbose_name': '\u0416\u0443\u0440\u043d\u0430\u043b', 'verbose_name_plural': '\u0416\u0443\u0440\u043d\u0430\u043b'},
        ),
        migrations.AlterField(
            model_name='journal',
            name='student',
            field=models.OneToOneField(verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Student'),
            preserve_default=True,
        ),
    ]
