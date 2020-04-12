

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
