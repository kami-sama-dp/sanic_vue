import login from '../views/login'
import manage from '../views/manage'
import dataAnalysis from '../views/dataAnalysis'
import serverMachine from '../views/serverMachine'
import testReport from '../views/testReport'
import testTask from '../views/testTask'
import home from '../views/home'


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
			}
		]
	},
	{
		path: '/',
		redirect: '/login'
	}
]
