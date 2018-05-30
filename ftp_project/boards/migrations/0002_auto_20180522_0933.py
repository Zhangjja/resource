# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-22 09:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=300)),
                ('password', models.CharField(max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='path',
            name='url',
            field=models.CharField(max_length=300),
        ),
    ]
