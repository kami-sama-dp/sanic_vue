import login from '../views/login'
import manage from '../views/manage'
import dataAnalysis from '../views/dataAnalysis'
import serverMachine from '../views/serverMachine'
import testReport from '../views/testReport'
import testTask from '../views/testTask'
import home from '../views/home'


export default[
	{
		path: '/login',
		component: login
	},
	{
		path:'/manage',
		component: manage,
		children:[
			{
				path:'/dataAnalysis',
				component:dataAnalysis
			},
			{
				path:'/serverMachine',
				component:serverMachine
			},
			{
				path:'/testReport',
				component:testReport
			},
			{
				path:'/testTask',
				component:testTask
			},
			{
				path:'/home',
				component:home
			}
		]
	},
	{
		path:'/',
		redirect:'/login'
	}
]