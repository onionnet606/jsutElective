from flask import *
from lib.JSUTCourse import JSUTCourse
from lib.Utils import util
import json
from flask_cors import *

app = Flask(__name__,static_folder='templates/dist')
CORS(app, supports_credentials=True)
# 拟合
@app.route('/CourseList',methods=["GET"])
def getCourseList():
    stu = JSUTCourse(util.student_id, [])
    keyword = request.args.get('keyword',default=None)

    if keyword != None:
        result = stu.screen_courses(keyword)
    else:
        result = stu.get_all_courses_full()

    return json.dumps({
        'data' : result,
        'code' : 0,
        'count': len(result),
    })

# 获取已选课程
@app.route('/selectedCourse',methods=["GET"])
def getSelectedCourse():
    stuID = request.args.get("stuid",default=util.student_id)
    stu = JSUTCourse(stuID, [])
    course = stu.get_selected_courses_full()
    return json.dumps({
        'data' : course,
        'code' : 0,
        'count': len(course),
    })

# 保存文件
@app.route('/saveFile',methods=["GET"])
def savefile():

    data = request.values.get('data')
    data = json.loads(data)
    util.saveFile(data)

    return json.dumps({
        'data': None,
        'code': 0,
        'msg': "修改成功，请运行脚本即可",
    })

@app.route('/getMonitorList', methods=['GET'])
def getMonitorList():
    # base.json 是使用筛选课程功能自动获取的
    base_list = util.loadSubscribeList()
    res = []
    for k,v in base_list.items():
        res.append({
            '选课课号': k,
            '课程名称': v,
            '学分': '文件导入，未知',
            '备注': '文件导入，未知'
        })
    return json.dumps({
        'data': res,
        'code': 0,
        'count': len(res),
    })

@app.route('/')
def index():
    return render_template('home.tpl')

@app.route('/getConfig')
def getConfig():
    return json.dumps({
        'data': util.getConfigList(),
        'code': 0,
        'count': len(util.getConfigList()),
    })

@app.route('/updateConfig')
def updateConfig():
    data = request.values.get('data')
    data = json.loads(data)

    util.updateConfigList(data)

    return json.dumps({
        'data': None,
        'code': 0,
        'msg': "修改成功，请运行脚本即可",
    })


if __name__ == '__main__':
    # Web
    app.run(host="127.0.0.1", port=5002, debug=True)
    # main()