import prettytable as pt
import re
import time
import json
import requests  # 网页访问

class JSUTCourse:
    """
    抢课类，可以获取课程列表、获取已选课程、抢课
    """

    def __init__(self, _student_id, monitor_list):
        # 甚至不需要Token验证
        self.token_code = ''
        # Header 浏览器头部
        self.http_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1226.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
            "Referer": "http://wzs.qian-xue.com/SelectCourse/Index/?code={}&state=".format(self.token_code)
        }
        # 监控列表
        self.monitor_list = monitor_list

        # 学生ID
        self.student_id = _student_id

    def show_courses(self, table_fields, course_list=None):
        if course_list is None:
            course_list = self.get_all_courses_full()

        tb = pt.PrettyTable(table_fields)

        tb.padding_width = 1  # One space between column edges and contents (default)

        for course in course_list:
            row_ = []
            for field in table_fields:
                row_.append(course[field])
            tb.add_row(row_)

        print(tb)

    def screen_courses(self, keyword, credit=None, course_list=None):
        if course_list is None:
            course_list = self.get_all_courses_full()
        new_course_list = []
        for course in course_list:
            if keyword in course["备注"] or keyword in course['课程名称'] or keyword in course['教师姓名']:
                if credit is not None:
                    if float(credit) == float(course['学分']):
                        new_course_list.append(course)
                else:
                    new_course_list.append(course)
        return new_course_list

    def __get_web_content(self, url):
        """获取网页信息并解析为List"""
        url = url + '&_=' + str(int(time.time() * 1000))  # add timestamp
        try:
            response = requests.get(url, headers=self.http_header)
            res = response.content.decode()
            pattern = re.compile('course\((.*)\)')
            s = pattern.findall(res)
        except:
            print('获取网页源文件出错')
            return []
        if len(s) <= 0:
            return []
        s = s[0]
        try:
            _json = json.loads(s)
        except:
            if res != "course(])":
                '''
                明确该返回结果是由于空集导致的
                '''
                print('未知数据结构 :' + res)
            return []
        return _json

    def get_all_courses_full(self):
        """获取可选课程的完整信息"""
        url = r'http://xuanke.qian-xue.com/course/getcourse?callback=course'

        raw_course_list = self.__get_web_content(url)
        course_list = []

        for course in raw_course_list:
            new = {
                '学年': course['XN'],
                '学期': course['XQ'],
                '课程代码': course['KCDM'],
                '课程名称': course['KCMC'],
                '课程类型': course['KCXZ'],
                '课程归属': course['KCGS'],
                '学分': course['XF'],
                '上课时间': course['SKSJ'],
                '上课地点': course['SKDD'],
                '总人数': course['RS'],
                '教师姓名': course['JSXM'],
                '选课课号': course['XKKH'],
                '选课年级': course['XZDX'],
                '选课专业': course['MXDX'],
                '备注': course['BZ'],
                '已选人数': course['YXRS']
            }
            course_list.append(new)
        return course_list

    def get_all_courses(self):
        """获取可选课程的 XKKH 和 KCMC"""
        url = r'http://xuanke.qian-xue.com/course/getcourse?callback=course'

        raw_course_list = self.__get_web_content(url)
        course_list = {}

        for course in raw_course_list:
            course_list['XKKH'] = course['KCMC']
        return course_list

    def get_selected_courses_full(self, student_id=None):
        """获取已选课程"""
        if student_id is None:
            student_id = self.student_id

        url = r'http://xuanke.qian-xue.com/course/GetSelectedCourse?callback=course&xh={}'.format(student_id)

        raw_selected_course = self.__get_web_content(url)
        selected_courses = []
        for course in raw_selected_course:
            new = {
                '选课课号': course['XKKH'],
                '课程名称': course['KCMC'],
                '学分': course['XF'],
                '上课地点': course['SKDD'],
                '教师姓名': course['JSXM'],
                '上课时间': course['SKSJ'],
                '备注': course['BZ'],
                '教材预定': course['JCYD']
            }
            selected_courses.append(new)
        return selected_courses

    def get_selected_courses(self, student_id=None):
        """获取已选课程"""
        if student_id is None:
            student_id = self.student_id

        url = r'http://xuanke.qian-xue.com/course/GetSelectedCourse?callback=course&xh={}'.format(student_id)

        raw_selected_course = self.__get_web_content(url)
        selected_courses = {}
        for course in raw_selected_course:
            selected_courses['XKKH'] = course['KCMC']
        return selected_courses

    def select_course(self, course_id, course_name=None):
        """选课"""
        url = r'http://xuanke.qian-xue.com/course/XuanKe?callback=course&xh={student_ID}&xkkh={course_ID}&jcyd=1'.format(
            student_ID=self.student_id, course_ID=course_id)
        try:
            result = self.__get_web_content(url)
            print("{} | 选课结果：{}".format(course_name if course_name is not None else course_id, result['msg']))
        except:
            print("{} | 选课失败，请检查选课课号是否正确".format(course_name if course_name is not None else course_id))

        return result

    def already_choose(self, course_id=None):
        '''判断选好的课是否在列表内，couser_ID如果提供，则判断course_ID是否已选'''
        # 获取已选课程
        selected_list = self.get_selected_courses_full()

        for select in selected_list:
            if course_id is not None:
                # 指定课号
                if select['选课课号'] == course_id:
                    return True
            elif select['选课课号'] in self.monitor_list:
                # 返回成功
                return True
        # 无匹配项
        return False

    def have_course(self, course_id):
        """可选列表内是否有这节课"""
        if course_id in self.get_all_courses():
            return True
        return False

    def want_course(self, course_id):
        """判断该课程是否在监控列表呢"""
        return course_id in self.monitor_list