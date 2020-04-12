<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
	<title>JSUT - 选课助手</title>
	<link rel="stylesheet" href="dist/layui/css/layui.css">
</head>
<body style="background-color: #eaeaea">
<a href="https://github.com/onionnet606/jsutElective" class="github-corner" aria-label="View source on GitHub"><svg width="80" height="80" viewBox="0 0 250 250" style="fill:#151513; color:#fff; z-index: 99998; position: absolute; top: 0; border: 0; right: 0;" aria-hidden="true"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path></svg></a><style>.github-corner:hover .octo-arm{animation:octocat-wave 560ms ease-in-out}@keyframes octocat-wave{0%,100%{transform:rotate(0)}20%,60%{transform:rotate(-25deg)}40%,80%{transform:rotate(10deg)}}@media (max-width:500px){.github-corner:hover .octo-arm{animation:none}.github-corner .octo-arm{animation:octocat-wave 560ms ease-in-out}}</style>


<!-- 导航条 -->
<ul class="layui-nav">
	<li class="layui-nav-item" style="font-size: 16px;">JSUT Elective</li>
</ul>


<!-- 你的HTML代码 -->
<div class="layui-container" style="margin-top: 20px;">
	<div class="layui-row layui-col-space15">
		<div class="layui-col-md12">
			<div class="layui-card">
				<div class="layui-card-header">当前配置</div>
				<div class="layui-card-body">
					<table id="configList" lay-filter="configList"></table>
					<button class="layui-btn" id="saveConfig" data-type="save_config">保存配置</button>
				</div>
			</div>
		</div>
		<div class="layui-col-md12">
			<div class="layui-tab layui-tab-card">
				<ul class="layui-tab-title">
					<li class="layui-this">当前可选课程</li>
					<li>已选课信息</li>
					<li>待抢课信息</li>
					<li>批量查询</li>
				</ul>
				<div class="layui-tab-content" >
					<div class="layui-tab-item layui-show">
						搜索关键字：
						<div class="layui-inline">
							<input class="layui-input" id="CourseList_keyword" autocomplete="off" >
						</div>
						<button class="layui-btn" data-type="search_course">搜索</button>
						<button class="layui-btn" data-type="search_course_cancel" style="display: none;">取消搜索</button>
						<!-- 可选课程 -->
						<table id="CourseList" lay-filter="CourseList"></table>
					</div>
					<div class="layui-tab-item">
						<div id="selectedCourse_search">
							查询学号：
							<div class="layui-inline">
								<input class="layui-input" id="selectedCourse_keyword" autocomplete="off" >
							</div>
							<button class="layui-btn" data-type="search_student">搜索</button>
						</div>
						<!-- 已选课程 -->
						<table id="selectedCourse" lay-filter="selectedCourse"></table>
					</div>
					<div class="layui-tab-item">
						<!-- 待抢课 -->
						<table id="wantCourse" lay-filter="wantCourse"></table>
						
						<button class="layui-btn" data-type="saveWantCourse">保存待抢课列表到文件</button>
					</div>
					<div class="layui-tab-item">
						学号范围查询：
						<div class="layui-inline">
							<div class="layui-input-inline" style="width: 120px;">
								<input type="text" id="sid" value="2018144101" autocomplete="off" class="layui-input">
							</div>
							<div class="layui-input-inline" style="width: 120px;">
								<input type="text" id="eid" value="2018144103" autocomplete="off" class="layui-input">
							</div>
						</div>
						<button class="layui-btn" data-type="search_students">搜索</button>
						<!-- 已选课程 -->
						<table id="searchTable" lay-filter="searchTable"></table>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

<script type="text/html" id="CourseListBar">
	<a class="layui-btn layui-btn-normal layui-btn-xs" lay-event="add">添到待选</a>
</script>

<script type="text/html" id="wantCourseBar">
	<a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="del">删除</a>
</script>





<script src="dist/layui/layui.all.js"></script>
<script>


    layui.use(['layer', 'form', 'element', 'table'], function(){
        var layer = layui.layer
            ,form = layui.form
            ,table = layui.table
            ,$ = layui.$
	        ,element = layui.element;

        table.render({
            elem: '#CourseList'
            ,url: 'http://127.0.0.1:5002/CourseList'
            ,toolbar: true
            ,defaultToolbar: ['filter', 'exports', 'print', {
                title: '刷新'
                ,layEvent: 'LAYTABLE_RELOAD'
                ,icon: 'layui-icon-refresh'
            }]
            ,loading: true
            ,cols: [[ //表头
                {field: '课程名称', title: '课程名称', width: 250, sort: true, fixed: 'left'}
                ,{field: '选课课号', title: '选课课号', hide:true}
                ,{field: '学分', title: '学分', width: 80, sort: true}
                ,{field: '上课时间', title: '上课时间'}
                ,{field: '上课地点', title: '上课地点', width: 130}
                ,{field: '教师姓名', title: '教师姓名', width: 100}
                ,{field: '已选人数', title: '已选人数', width: 90}
                ,{field: '总人数', title: '总人数', width: 80}
                ,{field: '备注', title: '备注', hide: true}
                ,{fixed: 'right', width:100,title: '操作', align:'center', toolbar: '#CourseListBar'}
            ]]
        });

        // 可选课程列表
        table.on('toolbar(CourseList)', function(obj){
            switch(obj.event){
                // 刷新
                default:
                case 'LAYTABLE_RELOAD':
                    table.reload('CourseList');
                    break;
            }
        });

        table.on('tool(CourseList)', function(obj){
            var data = obj.data;
            switch(obj.event) {
                case 'choose':
                    // 选课
                    break;
                case 'add':
                    // 添加选课
	                active['addCourse'].call(this,data);
                    break;
            }
        });

        table.render({
            elem: '#selectedCourse_search'
            ,url: 'http://127.0.0.1:5002/selectedCourse'
            ,page: false
            ,cols: [[ //表头
                {field: '课程名称', title: '课程名称', sort: true, fixed: 'left'}
                ,{field: '选课课号', title: '选课课号'}
                ,{field: '学分', title: '学分', width: 80, sort: true}
                ,{field: '上课时间', title: '上课时间'}
                ,{field: '上课地点', title: '上课地点', width: 130}
                ,{field: '教师姓名', title: '教师姓名', width: 100}
                ,{field: '教材预定', title: '教材预定', width: 90, templet: function(d){
                        return d['教材预定'] == 1 ? '已预定' : '未预定';
                    }}
                ,{field: '备注', title: '备注'}
            ]]
        });

        table.render({
            elem: '#searchTable'
            ,data: []
            ,page: false
            ,toolbar: true
	        ,limit: 999
            ,defaultToolbar: ['filter', 'exports', 'print']
            ,cols: [[ //表头
                {field: '学号', title: '学号', sort: true, fixed: 'left'}
                ,{field: '课程名称', title: '课程名称', sort: true}
                ,{field: '选课课号', title: '选课课号'}
                ,{field: '学分', title: '学分', width: 80, sort: true}
                ,{field: '上课时间', title: '上课时间'}
                ,{field: '上课地点', title: '上课地点', width: 130}
                ,{field: '教师姓名', title: '教师姓名', width: 100}
                ,{field: '教材预定', title: '教材预定', width: 90, templet: function(d){
                        return d['教材预定'] == 1 ? '已预定' : '未预定';
                    }}
                ,{field: '备注', title: '备注'}
            ]]
        });
	    
        table.render({
            elem: '#configList'
            ,url: 'http://127.0.0.1:5002/getConfig'
	        ,page: false
	        ,limit: 999
            ,cols: [[ //表头
                {field: '配置名', title: '配置名'}
                ,{field: '值', title: '值', edit:true}
            ]]
        });
	    
        table.render({
            elem: '#wantCourse'
            ,url: 'http://127.0.0.1:5002/getMonitorList'
	        ,page: false
	        ,limit: 999
            ,cols: [[ //表头
                {field: '选课课号', title: '选课课号', sort: true, fixed: 'left'}
                ,{field: '课程名称', title: '课程名称'}
                ,{field: '学分', title: '学分', width: 80, sort: true}
                ,{field: '备注', title: '备注'}
                ,{fixed: 'right', width:80,title: '操作', align:'center', toolbar: '#wantCourseBar'}
            ]]
        });
        
        table.on('tool(wantCourse)', function(obj){
            var data = obj.data;
            switch(obj.event) {
                case 'del':
                    // 删除
	                obj.del();
                    break;
            }
        });

        active = {
            
            saveWantCourse: function() {
                var tableData = table.cache['wantCourse'];
                var fileContent = {};
                $.each(tableData, function (k, v) {
                    if (v.length !== 0){
                        // obj删除长度不变
	                    fileContent[v['选课课号']] = v['课程名称']
                    }
                })
	            console.log(fileContent);
	            $.ajax({
                    url: 'http://127.0.0.1:5002/saveFile',
                    data: {
                        data: JSON.stringify(fileContent)
                    },
                    dataType:'json',
                    contentType: "application/json;charset=utf-8",
                    success: function (data) {
                        layer.msg(data.msg)
                    }
                })
	            
            },
            search_course_cancel: function() {
                $('#CourseList_keyword').val("");
                $("[data-type='search_course']").show();
                $("[data-type='search_course_cancel']").hide();
                table.reload('CourseList', {
                    where: null
                }, 'data');
                
            },
            search_course: function() {
                var CourseList_keyword = $('#CourseList_keyword');
                table.reload('CourseList', {
                    where: {
                        keyword: CourseList_keyword.val()
                    }
                }, 'data');
                $("[data-type='search_course_cancel']").show();
            
            },
            search_student: function(){
                var selectedCourse_keyword = $('#selectedCourse_keyword');
                table.reload('selectedCourse_search', {
                    where: {
                        stuid: selectedCourse_keyword.val()
                    }
                }, 'data');
            },

            search_students: function () {
                var sid = $('#sid').val();
                var eid = $('#eid').val();
                var tableData = table.cache['searchTable'];
                if (sid > eid){
                    return;
                }
                var t = 1;
                for (let i = sid; i <= eid; i++) {
                    setTimeout(function (){
                        $.ajax({
	                        url: 'http://127.0.0.1:5002/selectedCourse',
	                        data: {
	                            stuid: i
	                        },
	                        dataType:'json',
	                        success: function (data) {
	                            result = data.data;
	                            $.each(result, function (k, v) {
	                                tableData.push({
	                                    学号: i,
	                                    课程名称: v['课程名称'],
	                                    选课课号: v['选课课号'],
	                                    学分: v['学分'],
	                                    上课时间: v['上课时间'],
	                                    上课地点: v['上课地点'],
	                                    教师姓名: v['教师姓名'],
	                                    教材预定: v['教材预定'],
	                                    备注: v['备注'],
	
	                                });
	                            })
	                            table.reload("searchTable",{
	                                data: tableData
	                            });
	                        }
	                    })
                    }, t*1000);
                    console.log(t);
                    t++;
                }
            },
	        
	        addCourse: function (courseInfo) {
                var tableDatas = table.cache['wantCourse'];
                tableDatas.push({
	                选课课号: courseInfo['选课课号'],
	                课程名称: courseInfo['课程名称'],
	                学分: courseInfo['学分'],
	                备注: courseInfo['备注']
                })
		        table.reload('wantCourse',{
		            data: tableDatas,
			        url: ""
		        })
		        console.log(table.cache['wantCourse'])
		        layer.msg("添加成功：" + courseInfo['课程名称']);
		        
            },
	        
	        save_config: function () {
                var tableDatas = table.cache['configList'];
                var postData = {};
                $.each(tableDatas, function (k,v) {
                    postData[v['配置名']] = v['值']
                })
		        $.ajax({
			        url: 'http://127.0.0.1:5002/updateConfig',
                    data: {
                        data: JSON.stringify(postData)
                    },
                    dataType:'json',
                    contentType: "application/json;charset=utf-8",
                    success: function (data) {
                        layer.msg(data.msg)
                    }
                })
		        console.log(postData);
            }
            
        };

        $('.layui-tab-item .layui-btn').on('click', function(){
            var type = $(this).data('type');
            active[type] ? active[type].call(this) : '';
        });
        
        $('#saveConfig').on('click', function () {
            var type = $(this).data('type');
            active[type] ? active[type].call(this) : '';
        })



    });
</script>
</body>
</html>