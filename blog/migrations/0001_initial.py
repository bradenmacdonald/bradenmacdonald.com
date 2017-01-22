# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('body', models.TextField(help_text='Leave a blank line to split the summary from the rest')),
                ('posted', models.DateTimeField(db_index=True, null=True, verbose_name='Date posted')),
            ],
            options={
                'ordering': ('-posted',),
            },
        ),
    ]