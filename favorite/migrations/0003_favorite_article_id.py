# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2022-05-18 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favorite', '0002_remove_favorite_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='article_id',
            field=models.CharField(default='nono', max_length=20, verbose_name='文章號'),
        ),
    ]