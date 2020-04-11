import requests                     # 网页访问
import json
import re
import time
import os
import random
import platform

import prettytable as pt

# 监控列表
monitorList = {
    # 智慧树
    '(2019-2020-2)-X000603-9000000255-1': '大学生创业概论与实践',
    # 尔雅
	# '(2019-2020-2)-X000620-9000000044-1': '艺术哲学：美是如何诞生的',
    # 尔雅
    # '(2019-2020-2)-X000427-9000000044-1': '美学原理',
    # 尔雅
    # '(2019-2020-2)-X000611-9000000044-1': '艺术鉴赏',
    # 智慧树
    '(2019-2020-2)-X000615-9000000255-1': '美学与人生',
    # 中博财商
    # '(2019-2020-2)-X000607-9000000318-1': '财商教育案例分享',
}

# 需要操作学生ID
student_ID = '2018144137'

# 刷新时间
refreshTime_UP = 3
refreshTime_DOWN = 1

# 单个重复尝试次数
repeatTimes = 2

# ServerChan token
SERVERCHAN = r'SCU55917T9ef597b4983f7e463b88fb69ffae48635d369d95561fd'
# WXF
# SERVERCHAN = r'SCU62071T34ad4620284f6ede9dc90c5f066ef60d5d8853e4a8860'

class getCourse:
    '''
    抢课类，可以获取课程列表、获取已选课程、抢课、退课
    '''
    def __init__(self,student_ID,monitorList):
        # 甚至不需要Token验证
        self.token_code = ''
        # Header 浏览器头部
        self.header = {
            "User-Agent"   : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1226.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
            "Referer"      : "http://wzs.qian-xue.com/SelectCourse/Index/?code={}&state=".format(self.token_code)
        }
        # 监控列表
        self.monitorList = monitorList

        # 学生ID
        self.student_ID=student_ID

    def _getWebContent(self,url):
        '''获取网页信息并解析为List'''
        url = url
        try:
            response = requests.get(url,headers=self.header)
            res = response.content.decode()
            pattern = re.compile('course\((.*)\)')
            s = pattern.findall(res)
        except:
            print('获取网页源文件出错')
            return []
        if (len(s) <= 0):
            return []
        s = s[0]
        try:
            List = json.loads(s)
        except:
            if res != "course(])":
                '''
                明确该返回结果是由于空集导致的
                '''
                print('未知数据结构 :' + res)
            return []
        return List

    def getcourse(self):
        '''获取可选课程列表'''
        url = r'http://xuanke.qian-xue.com/course/getcourse?callback=course&_=1569037511460'

        courseList = self._getWebContent(url)
        List_ = []

        for course in courseList:
            new = {
                '学年'  :   course['XN'],
                '学期'  :   course['XQ'],
                '课程代码': course['KCDM'],
                '课程名称': course['KCMC'],
                '课程类型': course['KCXZ'],
                '课程归属': course['KCGS'],
                '学分'  :   course['XF'],
                '上课时间': course['SKSJ'],
                '上课地点': course['SKDD'],
                '总人数'  : course['RS'],
                '教师姓名': course['JSXM'],
                '选课课号': course['XKKH'],
                '选课年级': course['XZDX'],
                '选课专业': course['MXDX'],
                '备注'    : course['BZ'],
                '已选人数': course['YXRS']
            }
            List_.append(new)
        return List_

    def getSelectedCourse(self,student_ID=None):
        '''获取已选课程'''
        if(student_ID==None):
            student_ID = self.student_ID

        url = r'http://xuanke.qian-xue.com/course/GetSelectedCourse?callback=course&xh={}&_=1569047672354'.format(student_ID)

        selectedCourse = self._getWebContent(url)
        List_ = []
        for course in selectedCourse:
            new = {
                '选课课号'  :   course['XKKH'],
                '课程名称'  :   course['KCMC'],
                '学分'      :   course['XF'],
                '上课地点'  :   course['SKDD'],
                '教师姓名'  :   course['JSXM'],
                '上课时间'  :   course['SKSJ'],
                '备注'      :   course['BZ'],
                '教材预定'  :   course['JCYD']
            }
            List_.append(new)
        return List_

    def selectCourse(self,course_ID,course_name=None):
        '''选课'''
        url = r'http://xuanke.qian-xue.com/course/XuanKe?callback=course&xh={student_ID}&xkkh={course_ID}&jcyd=1&_=1569066468165'.format(student_ID=self.student_ID,course_ID=course_ID)

        result = self._getWebContent(url)
        print("{} | 选课结果：{}".format(course_name if course_name != None else course_ID,result['msg']))

        return result

    def withdrawCourse(self,course_ID):
        '''退课接口'''
        url = r'http://xuanke.qian-xue.com/course/TuiXuan?callback=course&xh={student_ID}&xkkh={course_ID}&_=1569066478528'.format(student_ID=self.student_ID,course_ID=course_ID)

        # result = self._getWebContent(url)
        return []

    def isAlreadyChoose(self,course_ID=None):
        '''判断选好的课是否在列表内，couser_ID如果提供，则判断course_ID是否已选'''
        # 获取已选课程
        selectedList = self.getSelectedCourse()

        for select in selectedList:
            if(course_ID!=None):
                # 指定课号
                if(select['选课课号'] == course_ID):
                    return True
            elif(select['选课课号'] in self.monitorList):
                # 返回成功
                return True
        # 无匹配项
        return False

    def haveCourse(self,course_ID):
        '''可选列表内是否有这节课'''
        for course in course_Class.getcourse():
            if(course['选课课号'] == course_ID):
                return True
        return False

    def wantCourse(self,course_ID):
        '''判断该课程是否在监控列表呢'''
        return course_ID in self.monitorList


def sendMsg(courseName):
    url = 'https://sc.ftqq.com/{}.send'.format(SERVERCHAN)
	# 标题内容替换
    title = courseName + '课程可选了！'
	# 替换内容
    content = courseName + '目前可以选了！| 学号' + student_ID + ' | 时间' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	
	# 网页参数提交
    data = "?text=" + title + "&desp=" + content
    req = requests.get(url + data)
    # 取回提交结果并作判断
    try:
        send_req = json.loads(req.content.decode())
    except:
        print('微信推送失败！')
    if send_req['errmsg'] != 'success':
        print('推送失败！')

def clearScreen():
    sys = platform.system()
    if sys == "Windows":
        os.system('cls')
    elif sys == "Linux":
        os.system('clear')
        pass


# 新建类
course_Class = getCourse(student_ID,monitorList)

# table_fields = ['学号', '课程名称', '学分']
# tb = pt.PrettyTable(table_fields)
# tb.padding_width = 1  # One space between column edges and contents (default)
#
#
# os.system('cls')
#
# for id in range(2018144101,2018144141):
#     course = course_Class.getSelectedCourse(id)
#     if len(course) <= 0:
#         tb.add_row([id, "Null", 0])
#     else:
#         course = course[0]
#         tb.add_row([id, course['课程名称'], course['学分']])
#     os.system('cls')
#     print(tb)
#     time.sleep(1)
# input()



while(1):
    # 遍历可选课程
    allCourse = course_Class.getcourse()
    if len(allCourse) <= 0:
        print('无课程可选...')
        time.sleep(random.randint(refreshTime_DOWN,refreshTime_UP))
        continue

    table_fields = ['课程名称', '学分', '教师姓名', '已选人数', '总人数']
    tb = pt.PrettyTable(table_fields)

    tb.padding_width = 1  # One space between column edges and contents (default)

    for course in allCourse:
        row_ = []
        for field in table_fields:
            row_.append(course[field])
        tb.add_row(row_)

    clearScreen()
    print('刷新时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '学号：', student_ID)
    print(tb)
    for course in allCourse:
        tryTimes = 0
        if(course_Class.wantCourse(course['选课课号'])):
            if(course_Class.isAlreadyChoose() == False):
                print("正在处理课程：" + course['课程名称'])
                # 没有选上想要的课
                # 二话不说，先选为敬
                tryTimes += 1
                course_Class.selectCourse(course['选课课号'], course['课程名称'])
                while(course_Class.isAlreadyChoose(course['选课课号']) != True and course_Class.haveCourse(course['选课课号']) == True and tryTimes <= repeatTimes):
                    # 立即选课
                    print(course['课程名称'] + ' | 正在选课...')
                    course_Class.selectCourse(course['选课课号'], course['课程名称'])
                    tryTimes += 1
                    time.sleep(1)
                if(course_Class.isAlreadyChoose(course['选课课号'])==True):
                    print(course['课程名称'] + ' | 抢课成功...')
                    sendMsg("抢课成功！" + course['课程名称'])
                else:
                    print(course['课程名称'] + ' | 抢课失败...')
            else:
                print(course['课程名称'] + ' | 已经抢到自动忽略...')
    t = random.randint(refreshTime_DOWN,refreshTime_UP)
    print("结束轮询，延时:",t)
    time.sleep(t)
