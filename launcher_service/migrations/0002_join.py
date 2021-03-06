# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-02-19 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('launcher_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('group', models.CharField(max_length=20)),
                ('share_id', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
