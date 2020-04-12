import random
import requests
import json
import time
import os

class Utils:
    def __init__(self,option):
        self.option = option
        self.refresh_time_down  = int(option['refresh_time_down'])
        self.refresh_time_up    = int(option['refresh_time_up'])
        self.SERVERCHAN    = option['serverchan'] if option['serverchan'] != "" else None
        self.student_id    = option['student_id']
        self.repeatTimes   = int(option['repeatTimes'])
        self.nameReplace = {
            'refresh_time_down' : '最小刷新时间',
            'refresh_time_up'   : '最大刷新时间',
            'serverchan'        : 'Server酱推送SCKEY',
            'student_id'        : '学号',
            'repeatTimes'       : '重复次数',
        }
        self.rev_nameReplace = {
            '最小刷新时间': 'refresh_time_down',
            '最大刷新时间': 'refresh_time_up',
            'Server酱推送SCKEY': 'serverchan',
            '学号': 'student_id',
            '重复次数': 'repeatTimes',
        }

    def getConfigList(self):
        res = []
        for k,v in self.nameReplace.items():
            res.append({
                '配置名'   : v,
                '值'       : self.option[k]
            })
        return res

    def updateConfigList(self,configList):
        updateList = {}
        for k,v in configList.items():
            updateList[self.rev_nameReplace[k]] = v
        with open(os.path.dirname(__file__) + "/../json/config.json", 'w', encoding='utf-8') as file_obj:
            file_obj.write(json.dumps(updateList, indent=2, ensure_ascii=False))
        self.refreshConfig()

    def saveFile(self,courseList):
        with open(os.path.dirname(__file__) + '/../json/base.json', 'w', encoding='utf-8') as file_obj:
            file_obj.write(json.dumps(courseList, indent=2, ensure_ascii=False))


    def random_time(self):
        return random.randint(self.refresh_time_down, self.refresh_time_up)

    def get_file_data(self,path):
        # must be a text file
        with open(path, 'r', encoding='utf8') as f:
            content = f.read()
        return content

    def send_to_wechat(self,courseName):
        if self.SERVERCHAN == None:
            return

        url = 'https://sc.ftqq.com/{}.send'.format(self.SERVERCHAN)
        # 标题内容替换
        title = courseName + '课程选课成功！'
        # 替换内容
        content = courseName + '选课成功！ | 学号：' + self.student_id + ' |  时间：' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                      time.localtime())

        try:
            # 网页参数提交
            data = "?text=" + title + "&desp=" + content
            req = requests.get(url + data)
            # 取回提交结果并作判断
            send_req = json.loads(req.content.decode())
        except:
            print('微信推送失败！')
        if send_req['errmsg'] != 'success':
            print('推送失败！')
        else:
            print("推送成功！")

    def loadSubscribeList(self):
        # base.json 是使用筛选课程功能自动获取的
        base_list = json.loads(self.get_file_data(os.path.dirname(__file__)  + "/../json/base.json"))

        # additon.json 是手工填写的
        addition_list = json.loads(self.get_file_data(os.path.dirname(__file__)  + "/../json/addition.json"))

        base_list.update(addition_list)
        return base_list

    def refreshConfig(self):
        try:
            with open(os.path.dirname(__file__) + "/../json/config.json", 'r', encoding='utf8') as f:
                content = f.read()
        except:
            exit()

        self.__init__(json.loads(content))


try:
    with open(os.path.dirname(__file__)  + "/../json/config.json", 'r', encoding='utf8') as f:
        content = f.read()
except:
    exit()

util = Utils(json.loads(content))