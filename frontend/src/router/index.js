import login from '../views/login'
import manage from '../views/manage'
import dataAnalysis from '../views/dataAnalysis'
import serverMachine from '../views/serverMachine'
import testReport from '../views/testReport'
import testTask from '../views/testTask'
import home from '../views/home'
import addTask from '../views/addTask.vue'
import editTask from '../views/editTask.vue'
import reportDetail from '../views/reportDetail.vue'

export default [
	{
		path: '/login',
		component: login
	},
	{
		path: '/manage',
		component: manage,
		children: [
			{
				path: '/dataAnalysis',
				component: dataAnalysis,
				meta:{
					title:['数据分析'],
					requireAuth: true
				}
			},
			{
				path: '/serverMachine',
				component: serverMachine,
				meta:{
					title:['服务器列表'],
					requireAuth: true
				}
			},
			{
				path: '/testReport',
				component: testReport,
				meta:{
					title:['测试报告'],
					requireAuth: true
				}
			},
			{
				path: '/testTask',
				component: testTask,
				meta:{
					title:['测试任务'],
					requireAuth: true
				}
			},
			{
				path: '/home',
				component: home,
				meta: []
			},
			{
				path:'/addTask',
				component:addTask,
				meta:{
					title:['添加测试任务'],
					requireAuth: true
				}
			},
			{
				name:'editTask',
				path:'/editTask',
				component:editTask,
				meta:{
					title:['编辑测试任务'],
					requireAuth: true
				}
			},
			{
				name:'reportDetail',
				path:'/reportDetail',
				component:reportDetail,
				meta:{
					title:['报告详情页'],
					requireAuth: true
				}
			},
		]
	},
	{
		path: '/',
		redirect: '/login'
	}
]
