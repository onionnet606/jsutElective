# 江理工选课脚本
本脚本通过微信公众号的接口进行提交，模拟人工提交。

> 接口竟然连鉴权都没有，可以随意退课、选课、查课。

> 请不要用于非法用途，否则后果自负。

## API

### 说明

以下API链接均以学号：`8888888888`，选课号：`(2019-2020-2)-X000587-2014500040-1`，作为例子。

以下返回结果均包含在一个`course()`内，例如：
```json
course({"status":0,"msg":"不在选课时间","data":null})
```

返回的结果一般直接是数据集，若有返回提示信息我所遇到的是遵循以下格式的：
```json
{
  "status":0,
  "msg":"不在选课时间",
  "data":null,
}
```


### 查询已选课程
> http://xuanke.qian-xue.com/course/GetSelectedCourse?callback=course&xh=8888888888&_=1569047672354

| 参数 | 说明  |
| ---- | ---- |
|  xh | 学号，需要查询的学号 |
|  &_ | 时间戳，猜测用于防止浏览器缓存     |

### 选课
> http://xuanke.qian-xue.com/course/XuanKe?callback=course&xh=8888888888&xkkh={course_ID}&jcyd=0&_=1569066468165

| 参数 | 说明  |
| ---- | ---- |
|  xh | 学号，需要查询的学号 |
|  xkkh | 选课课号 |
|  jcyd | 教材预定 |
|  &_ | 时间戳，猜测用于防止浏览器缓存 |

### 查询所有课程列表

> http://xuanke.qian-xue.com/course/getcourse?callback=course&_=1569037511460

| 参数 | 说明                           |
| ---- | ------------------------------ |
| &_   | 时间戳，猜测用于防止浏览器缓存 |

### 退课

> http://xuanke.qian-xue.com/course/TuiXuan?callback=course&xh=8888888888&xkkh={course_ID}&_=1569066478528

| 参数 | 说明                           |
| ---- | ------------------------------ |
| xh   | 学号，需要查询的学号           |
| xkkh | 选课课号                       |
| &_   | 时间戳，猜测用于防止浏览器缓存 |




## 选课号获取方法

1. 进入教务系统，选课列表（一般提前一天会公布）
2. 开启浏览器`开发者工具(F12)`，选择你想查看的课程名称，定位其元素
3. 查看元素的`onclick`值，里面的`xkkh`就是了

![image-20200408222825539](C:\Users\onion\AppData\Roaming\Typora\typora-user-images\image-20200408222825539.png)