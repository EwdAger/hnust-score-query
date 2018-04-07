# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.

class Student(models.Model):
    stu_id = models.CharField(max_length=200, verbose_name='学号')
    name = models.CharField(max_length=200, verbose_name='姓名')
    fail_num = models.CharField(max_length=200, verbose_name='不及格门数')
    average = models.CharField(max_length=200, verbose_name='平均分')
    total = models.CharField(max_length=200, verbose_name='总分')
    credit = models.CharField(max_length=200, verbose_name='所得学分')
    gpa = models.CharField(max_length=200, verbose_name='平均学分绩')
    gpa_point = models.CharField(max_length=200, verbose_name='平均学分绩点')
    rank = models.CharField(max_length=200, verbose_name='排名')

    class Meta:
        verbose_name = '总成绩'
        verbose_name_plural = '总成绩'

    def __unicode__(self):
        return self.name

class Course(models.Model):
    stu_id = models.CharField(max_length=200, verbose_name='学号')
    name = models.CharField(max_length=200, verbose_name='姓名')
    c_name = models.CharField(max_length=200, verbose_name='课程名')
    score = models.CharField(max_length=200, verbose_name='得分')

    class Meta:
        verbose_name = '个人成绩'
        verbose_name_plural = '个人成绩'

    def __unicode__(self):
        return self.name

class Class(models.Model):
    stu_id = models.CharField(max_length=200, verbose_name='学号')
    name = models.CharField(max_length=200, verbose_name='姓名')
    class_num = models.CharField(max_length=200, verbose_name='班级')

    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'

    def __unicode__(self):
        return self.class_num

class Teacher(models.Model):
    tid = models.CharField(max_length=200, verbose_name='工号')
    name = models.CharField(max_length=200, verbose_name='姓名')
    class_num = models.CharField(max_length=200, verbose_name='班级')

    class Meta:
        verbose_name = '班主任信息'
        verbose_name_plural = '班主任信息'

    def __unicode__(self):
        return self.name