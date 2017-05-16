# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 15:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20170420_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='courses.Course', verbose_name='Curso'),
        ),
    ]
