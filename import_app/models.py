# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Categories(models.Model):
    parentid = models.IntegerField(db_column='parentID')  # Field name made lowercase.
    title = models.CharField(max_length=200)
    titlefull = models.CharField(db_column='titleFull', max_length=1000)  # Field name made lowercase.
    operation = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'categories'


class Elements(models.Model):
    categoryid = models.IntegerField(db_column='categoryID')  # Field name made lowercase.
    sum = models.FloatField()
    created = models.DateField()

    class Meta:
        managed = False
        db_table = 'elements'


class ElementsHashtags(models.Model):
    elements_id = models.IntegerField()
    hashtags_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'elements_hashtags'
        unique_together = (('elements_id', 'hashtags_id'),)


class Hashtags(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'hashtags'


class Users(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=40)
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=70)
    created_at = models.DateTimeField()
    active = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'users'
