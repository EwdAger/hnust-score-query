# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import jwc_spider
import models
from django.db import transaction
import time
import shutil
import os
from django.http import HttpResponseRedirect

now = '2018-2-1'

def init_score_data():
    for num in range(19):    # 全学院十九个专业
        spider = jwc_spider.spider()
        keys = spider.Score_keys_spdier(num)    # 获取课程名
        soup = spider.Score_soup(num)    # 初始化soup
        while(True):
            if soup != None:
                values, soup = spider.Score_spider(num, soup)
                if not values or values[0].strip() == '':
                    break
                if not models.Student.objects.filter(stu_id=values[0]).exists():
                    models.Student.objects.create(stu_id=values[0], name=values[1], rank=values[-1], gpa_point=values[-2],
                                                  gpa=values[-3], credit=values[-4], total=values[-5], average=values[-6],
                                                  fail_num=values[-7])

                with transaction.atomic():
                    i = 3
                    while(True):
                        if keys[i] == '不及格门数':  # 最后一项课程名后一定为不及格门数
                            break
                        if values[i] != '0':
                            if not models.Course.objects.filter(stu_id=values[0], c_name=keys[i]).exists():
                                models.Course.objects.create(stu_id=values[0], name=values[1], c_name=keys[i], score=values[i])
                        i += 1
                soup = spider.Score_soup(num, soup)
            else:
                break

def init_student_data():
    spider = jwc_spider.spider()
    for i in range(14, 18):
        stu_id, name, class_num = spider.Student_spdier(i)
        with transaction.atomic():
            for j in range(len(stu_id)):
                if not models.Class.objects.filter(stu_id=stu_id[j]).exists():
                    models.Class.objects.create(stu_id=stu_id[j], name=name[j], class_num=class_num[j])

def init_teachers():
    class_name = ['专业名称list']
    class_grade = ['年级list']
    class_num = ['班级list']
    jsj = ['班主任名称list']
    jsj_id = ['工号list']
    wg = []
    wg_id = []
    wl = []
    wl_id = []
    xa = []
    xa_id = []
    rj = []
    rj_id = []

    for class_ in class_name:
        i = 0
        for grade in class_grade:
            for num in class_num:
                if class_ == '计算机':
                    if grade == '14' and num == '6班':
                        break
                    models.Teacher.objects.create(tid=jsj_id[i], name=jsj[i], class_num=grade+class_+num)
                    i += 1
                if class_ == '网络':
                    if num == '4班':
                        break
                    models.Teacher.objects.create(tid=wg_id[i], name=wg[i], class_num=grade + class_ + num)
                    i += 1
                if class_ == '物联':
                    if num == '3班':
                        break
                    models.Teacher.objects.create(tid=wl_id[i], name=wl[i], class_num=grade + class_ + num)
                    i += 1
                if class_ == '信息安全':
                    if num == '4班':
                        break
                    models.Teacher.objects.create(tid=xa_id[i], name=xa[i], class_num=grade + class_ + num)
                    i += 1
                if class_ == '软件':
                    if grade == '14':
                        continue
                    if num == '3班':
                        break
                    models.Teacher.objects.create(tid=rj_id[i], name=rj[i], class_num=grade + class_ + num)
                    i += 1


# 因未知问题无法成功创建Score文件夹，该为win下测试代码。正式上线后换Linux脚本执行清空文件夹操作
def del_data():
    models.Student.objects.all().delete()
    models.Course.objects.all().delete()
    dir = "ScoreQuery/page/Score"
    if os.path.exists(dir):
        shutil.rmtree(dir, 0755)
    os.mkdir(dir)
    init_score_data()

def update_score():
    global now
    init_score_data()
    now = time.strftime('%Y-%m-%d', time.localtime(time.time()))

def update(request):
    pw = request.GET.get('pw')
    if pw.lower() == '':
        del_data()
        update_score()
        check_code = "数据更新已完成！"
    else:
        check_code = "密码错误！"
    return render(request, 'hello.html', {"check_code": check_code})

def check(request):
    return render(request, 'check.html')

def index(request):
    # init_score_data()
    # models.Course.objects.all().delete()
    # models.Student.objects.all().delete()
    return render(request, 'index.html')

def paiming(request):
    grade = request.GET.get('grade')
    num = request.GET.get('num')
    cls = request.GET.get('cls')

    class_dict = {"1": "网络", "2": "计算机", "3": "信息安全", "4": "软件工程", "5": "物联"}

    class_name = class_dict[num]
    if class_name == "物联" and (grade == '15' or grade == '16' or grade == '17'):
        class_name = '物联网'
    elif class_name == "软件工程" and (grade == '16' or grade == '17'):
        class_name = '软件'
    title = grade + class_name + cls + "班"
    datas = []

    if not models.Class.objects.filter(class_num=title):
        return render(request, '404.html')
    class_id = models.Class.objects.filter(class_num=title).values_list('stu_id', flat=True)
    for tid in class_id:
        if not models.Student.objects.filter(stu_id=tid):
            continue
        try:
            obj = models.Student.objects.get(stu_id=tid) # 有的同学休学或者其他原因查不到成绩。。。但是学籍还是在的。。所以得跳过
        except:
            continue
        stu_id = '/person?stu_id=' + obj.stu_id
        data = [obj.rank, obj.name, obj.gpa_point, obj.credit, stu_id]
        datas.append(data)

    datas = sorted(datas, key=lambda x: x[2], reverse=True)
    return render(request, 'paiming.html', {
        "title": title,
        "datas": datas,
        "now": now
    })

def person(request):
    stu_id = request.GET.get('stu_id')
    objs = models.Course.objects.filter(stu_id=stu_id)
    datas = []

    name = objs[0].name
    num = 0

    for obj in objs:
        flag = 0
        if '*' in obj.score:
            temp = obj.score.replace('*', '')
            if temp < '60' or temp == '不及格':
                flag = 1
                num += 1
        c_name = '/course?c_name=' + obj.c_name + '&stu_id=' + obj.stu_id
        data = [obj.c_name, obj.score, flag, c_name]
        datas.append(data)

    return render(request, 'person.html', {
        "datas": datas,
        "name": name,
        "num": num,
        "now": now
    })

def course(request):
    c_name = request.GET.get('c_name')
    stu_id = request.GET.get('stu_id')
    datas = []

    class_num = models.Class.objects.get(stu_id=stu_id).class_num
    all_stu_id = models.Class.objects.filter(class_num=class_num).values_list('stu_id', flat=True)
    for tid in all_stu_id:
        try:
            stu = models.Course.objects.get(c_name=c_name, stu_id=tid)
        except:
            continue
        flag = 0
        if '*' in stu.score:
            temp = stu.score.replace('*', '')
            if temp < '60' or temp == '不及格':
                flag = 1
        stu_num = '/person?stu_id=' + stu.stu_id
        data = [stu.name, stu.score, flag, stu_num]
        datas.append(data)

    return render(request, 'course.html', {
        "datas": datas,
        "c_name": c_name,
        "now": now
    })

def search(request): # 该部分未完成
    name = request.GET.get('name')
    class_num = request.GET.get('class_num')
    stu_name = models.Class.objects.filter(class_num=class_num).values_list('name', flat=True)
    if name in stu_name:
        try:
            stu_id = models.Class.objects.get(name=name).stu_id
        except:
            pass
        return HttpResponseRedirect('person?stu_id=' + stu_id)
    else:
        msg = "查询的学生不存在"
        return render(request, 'index.html', {"msg": msg})

def charts(request):
    grade = request.GET.get('grade')     # 接入微信后直接获取班主任所在班级
    num = request.GET.get('num')
    cls = request.GET.get('cls')

    class_dict = {"1": "网络", "2": "计算机", "3": "信息安全", "4": "软件工程", "5": "物联"}

    class_name = class_dict[num]
    if class_name == "物联" and (grade == '15' or grade == '16' or grade == '17'):
        class_name = '物联网'
    elif class_name == "软件工程" and (grade == '16' or grade == '17'):
        class_name = '软件'
    self_cls = grade + class_name + cls + "班"

    if not models.Class.objects.filter(class_num=self_cls):
        return render(request, '404.html')

    # 获取本专业所有班级名与该班级所有学生学号
    all_cls = []
    all_cls_stuid = []
    for i in range(1, 10):
        cls_temp = grade + class_name + str(i) + "班"
        if not models.Class.objects.filter(class_num=cls_temp):
            break
        temp_stu_id = models.Class.objects.filter(class_num=cls_temp).values_list('stu_id', flat=True)  # 获取一个班所有学生学号的list
        all_cls_stuid.append(temp_stu_id)
        all_cls.append(cls_temp)

    # 获取各班挂科人数、年排前十人数、平均学分绩点分布
    all_fail_num = []
    all_rank_ten = []
    # 列表不能进行连等初始化操作！！！
    all_gpa_list1 = []
    all_gpa_list2 = []
    all_gpa_list3 = []
    all_gpa_list4 = []
    all_gpa_list5 = []
    for temp in all_cls_stuid:
        fail_count = rank_count = gpa_count1 = gpa_count2 = gpa_count3 = gpa_count4 = gpa_count5 = 0
        for stu in temp:
            try:
                stu_obj = models.Student.objects.get(stu_id=stu)
            except:
                continue
            fail = int(stu_obj.fail_num)
            rank = int(stu_obj.rank)
            gpa = float(stu_obj.gpa_point)
            if rank <= 10:
                rank_count += 1
            if fail != 0:
                fail_count += 1

            if gpa <= 1.5:
                gpa_count1 += 1
            elif gpa <= 2.0:
                gpa_count2 += 1
            elif gpa <= 2.5:
                gpa_count3 += 1
            elif gpa <= 3.0:
                gpa_count4 += 1
            elif gpa <= 4.0:
                gpa_count5 += 1

        all_fail_num.append(fail_count)
        all_rank_ten.append(rank_count)
        all_gpa_list1.append(gpa_count1)
        all_gpa_list2.append(gpa_count2)
        all_gpa_list3.append(gpa_count3)
        all_gpa_list4.append(gpa_count4)
        all_gpa_list5.append(gpa_count5)

    self_stu_id = models.Class.objects.filter(class_num=self_cls).values_list('stu_id', flat=True)

    all_name = []
    fail_num = []
    great_num = []

    c_names = []
    for stu_id in self_stu_id:
        count = 0
        try:
            stu = models.Student.objects.get(stu_id=stu_id)    # 有的同学休学或者其他原因查不到成绩。。。但是学籍还是在的。。所以得跳过
        except:
            continue
        name = stu.name
        fail = stu.fail_num
        scores = models.Course.objects.filter(stu_id=stu_id).values_list('score', flat=True)
        for score in scores:
            try:
                score = float(score)
                if score >= 90:
                    count += 1
            except:
                if score == '优':
                    count += 1
        all_name.append(name)
        fail_num.append(fail)
        great_num.append(count)
        """
        c_names = models.Course.objects.filter(stu_id=stu_id).values_list('c_name', flat=True)
        for c_name in c_names:
            count1 = count2 = count3 = count4 = count5 = 0
            score = models.Course.objects.get(stu_id=stu_id, c_name=c_name).score
            if score < '60' or score == '不及格':
                count1 += 1
            elif score < '70' or score == '及格':
                count2 += 1
            elif score < '80' or score == '中':
                count3 += 1
            elif score < '90' or score == '良':
                count4 += 1
            elif score >= '90' or score == '优':
                count5 += 1
        
        list1.append(count1)
        list2.append(count2)
        list3.append(count3)
        list4.append(count4)
        list5.append(count5)
        """

    fail_num_add = []
    for i in fail_num:
        if i != '0':
            i = '-' + i
        fail_num_add.append(i)


    return render(request, 'charts.html', {
        'all_cls': all_cls,
        'all_fail_num': all_fail_num,
        'all_rank_ten': all_rank_ten,

        'all_gpa_list1': all_gpa_list1,
        'all_gpa_list2': all_gpa_list2,
        'all_gpa_list3': all_gpa_list3,
        'all_gpa_list4': all_gpa_list4,
        'all_gpa_list5': all_gpa_list5,

        'all_name': all_name,
        'fail_num': fail_num_add,
        'great_num': great_num,
    })