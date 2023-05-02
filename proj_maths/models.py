# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Terms(models.Model):
    name = models.TextField()
    definition = models.TextField()
    termauthor = models.TextField(blank=True, null=True)
    list = models.TextField(blank=True, null=True)
    pos = models.TextField()

    class Meta:
        managed = False
        db_table = 'terms'


class VerbsForms(models.Model):
    verb = models.TextField()
    ich = models.TextField(blank=True, null=True)
    du = models.TextField(blank=True, null=True)
    fid = models.OneToOneField(Terms, models.DO_NOTHING, db_column='fid', primary_key=True, blank=True, null=False)
    er = models.TextField(blank=True, null=True)
    ihr = models.TextField(blank=True, null=True)
    wir = models.TextField(blank=True, null=True)
    sie = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verbs_forms'
