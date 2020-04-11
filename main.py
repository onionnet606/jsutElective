from lib.Utils import util
import time
from lib.JSUTCourse import JSUTCourse

def main():
    # 新建类
    if util.student_id is None:
        exit()

    student_id = util.student_id

    courseList = util.loadSubscribeList()

    jsut_course = JSUTCourse(student_id, courseList)

    while 1:
        table_fields = ['课程名称', '选课课号', '学分', '教师姓名', '备注', '已选人数']
        s_table_fields = ['课程名称', '上课地点', '上课时间', '教师姓名', '选课课号', '学分', '备注']

        print('刷新时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '学号：', student_id)
        # 遍历可选课程
        all_course = jsut_course.get_all_courses_full()
        # if len(all_course) <= 0:
        #     print('无课程可选...')
        #     time.sleep(random.randint(refresh_time_up, refresh_time_down))
        #     continue
        jsut_course.show_courses(table_fields, all_course)
        while 1:
            monitor_list = jsut_course.monitor_list
            for course_id in jsut_course.monitor_list:
                if not jsut_course.already_choose(course_id):
                    # send_to_wechat("正在处理课程：" + course['课程名称'])
                    # 没有选上想要的课
                    # 二话不说，先选为敬
                    tryTimes = 0
                    while tryTimes < util.repeatTimes:
                        # 立即选课
                        print(monitor_list[course_id] + ' | 正在选课...')
                        jsut_course.select_course(course_id, monitor_list[course_id])
                        tryTimes += 1
                        time.sleep(util.random_time())
                    if jsut_course.already_choose(course_id):
                        print(monitor_list[course_id] + ' | 抢课成功...')
                        util.send_to_wechat(monitor_list[course_id])

                        print("当前选课情况: ")
                        selected_courses = jsut_course.get_selected_courses_full()
                        jsut_course.show_courses(s_table_fields, selected_courses)

                        break
                    else:
                        print(monitor_list[course_id] + ' | 抢课失败...')
                else:
                    print(monitor_list[course_id] + ' | 已经抢到自动忽略...')

            time.sleep(util.random_time())

if __name__ == '__main__':
    main()


