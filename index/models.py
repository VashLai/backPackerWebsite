# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Backpacker(models.Model):
    name = models.CharField(max_length=20)
    category = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    articlenum = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    reports = models.CharField(max_length=20, blank=True, null=True)
    b_time = models.DateTimeField(blank=True, null=True)
    c_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return 'Title:' + self.title + '____ArticleNum:' + str(self.articlenum)

    class Meta:
        managed = False
        db_table = 'backpacker'
