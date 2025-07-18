# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.TextField(unique=True)
    full_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    owner = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    due_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task'


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey(Task, models.DO_NOTHING, blank=True, null=True)
    author = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'
