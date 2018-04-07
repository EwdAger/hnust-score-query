# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from captcha_verify import verify
from time import sleep

class spider(object):

    def login(self):
        zy = []
        """
        敏感信息已处理
        专业从上到下分别对应17-14， 从左到右对应网络，软件，计科，物联，信安
        """
        for i in range(len(zy)):

                login_url = '教务网登录API地址'
                check = "<script language=\"javascript\">window.location.href='http://kdjw.hnust.cn/kdjw/framework/main.jsp';</script>"

                while (True):
                    cookies = requests.get('验证码API地址').cookies
                    img = requests.get('验证码API地址', cookies=cookies).content
                    with open('ScoreQuery/yzm/captcha.bmp', 'wb') as f:
                        f.write(img)
                    code = verify("ScoreQuery/yzm/captcha.bmp")
                    data = {
                        'USERNAME': '权限账号',
                        'PASSWORD': '权限账号密码',
                        'RANDOMCODE': code
                    }
                    login = requests.post(login_url, cookies=cookies, data=data)
                    soup = BeautifulSoup(login.content, "lxml")
                    if str(soup.script) == check:
                        break
                data = {
                    "yx": "05",  # 学院
                    "zy": zy[i],  # 专业的16进制？
                    "pxfs": "1",  # 排序方式
                    "pmfs": "3",  # 排名方式
                    "xsfs": "1",  # 显示方式
                    "xjzt": "01",  # 学籍状态
                }

                html = requests.post('成绩查询API', data=data,
                                     cookies=cookies)
                with open('ScoreQuery/page/Score/%d.html' % i, 'w') as f:
                    f.write(html.content)
                sleep(5)

    def Score_keys_spdier(self, num):
        soup = ''
        try:
            soup = BeautifulSoup(open("ScoreQuery/page/Score/%d.html" % num), "lxml")
        except:
            self.login()
            self.Score_keys_spdier(0)
        i = 1
        keys = []
        # 获取学生成绩字典的课程名目录
        key_soup = soup.find("tr", bgcolor="#D1E4F8")
        while (True):
            try:
                key = key_soup.contents[i].text.strip()
                keys.append(key)
                i += 1
            except:
                break
        return keys



    def Score_soup(self, num, soup=None):
        if soup == None:
            try:
                soup = BeautifulSoup(open("ScoreQuery/page/Score/%d.html" % num), "lxml")
            except:
                self.login()
                self.Score_soup(0)
            try:
                value_soup = soup.find("table", id="mxh").next_element    # 只用于初始化soup时定位
            except:
                return 1
        else:
            value_soup = soup.next_sibling
        return value_soup


    def Score_spider(self, num, value_soup=None):
        values = []
        if value_soup == None:
            value_soup = self.Score_soup(num)
        j = 1
        # 获取一条学生成绩数据
        while(True):
            try:
                value = value_soup.contents[j].text
                if value.strip() == '':
                    break
                values.append(value)
                j += 1
            except:
                break
        return values, value_soup

    def Student_spdier(self, grade):
        stu_id = []
        s_name = []
        class_ = []
        j = 1
        while(True):
            try:
                soup = BeautifulSoup(open("ScoreQuery/page/Student/%s/%s.htm" % (str(grade), j)), "lxml")
            except:
                break
            i = 1
            stu_soup = soup.find("tr", id="%s" % str(i))
            while(stu_soup != None):
                temp = stu_soup.contents[5].text
                if len(temp) != 10:
                    temp = stu_soup.contents[2].text
                    stu_id.append(temp)
                    temp = stu_soup.contents[3].text
                    s_name.append(temp)
                    temp = stu_soup.contents[10].text
                    class_.append(temp)
                    i += 1
                    stu_soup = soup.find("tr", id="%s" % str(i))
                    continue
                stu_id.append(temp)
                temp = stu_soup.contents[7].text
                s_name.append(temp)
                temp = stu_soup.contents[21].text
                class_.append(temp)

                i += 1
                stu_soup = soup.find("tr", id="%s" % str(i))
            j += 1

        return stu_id, s_name, class_