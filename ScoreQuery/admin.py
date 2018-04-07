# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Student, Course

# Register your models here.

class SignStudent(admin.ModelAdmin):
    list_display = ('stu_id', 'name', 'fail_num', 'average', 'total', 'credit', 'gpa', 'gpa_point', 'rank')
    search_fields = ('name',)
    list_filter = ('fail_num', 'gpa_point')

class SignCouser(admin.ModelAdmin):
    list_display = ('name', 'c_name', 'score')
    search_fields = ('name',)

admin.site.register(Student, SignStudent)
admin.site.register(Course, SignCouser)
