# flask_vue
最好在chrome下打开，safari 有些样式初次加载有问题

技术栈：Vue + Vuex + ElementUI + flask + peewee + HTTPBasicAuth + celery + fabric (前后端分离MVVM模式)

目前前端处理跨域问题, 后期可优化成后端处理

pymonitor.py 可以监控python脚本的实时变化, 简单模拟一个服务端热更新功能


  实现的模块：
 
    1. 登录注册(带token，过期验证) 使用的peewee(orm)
    2. CRUD服务器资源列表、测试任务列表
    3. 展示测试报告(locust)
    4. 上传文件到远程服务器, fabric远程操作linux命令,
    
  使用celery实现分布式异步任务处理

    celery worker -A curd.celery -l info  -f celery.log 

    启动celery worker 更改celery配置需要重启celery
  
 消息队列存放在rabbitmq或者redis(broker中间件)
 
 任务状态的结果存在redis(backend), 前端根据这个状态更新相应的任务状态
 
   启动前端(Vue)： 
   
    需要安装node 和yarn 
    cd frontend
    yarn run serve 
   
  启动后端(flask)
  
    nohup python3  run.py >/dev/null 2>&1 &
    
  启动redis
  
    nohup redis-server > web6.log 2>&1 < /dev/null&
   
 安装rabbitmq:(可以不使用, 用redis代替)
 
     brew install rabbitmq
     cd  /usr/local/Cellar/rabbitmq/3.8.2 （安装目录）
  
 安装RabiitMQ的可视化监控插件
 
    sudo sbin/rabbitmq-plugins enable rabbitmq_management

配置环境变量

    vi ~/.bash_profile
    export RABBIT_HOME= /usr/local/Cellar/rabbitmq/3.8.2
    export PATH=$PATH:$RABBIT_HOME/sbin
    source ~/.bash_profile


后台启动rabbitMQ

    后台启动
    rabbitmq-server -detached  
    查看状态
    rabbitmqctl status 
    访问可视化监控插件的界面
    浏览器内输入 http://localhost:15672,
    默认的用户名密码都是guest,登录后可以在Admin那一列菜单内添加自己的用户
    rabbitmqctl stop 关闭
  
  监控  flower
    
    pip install flower
    启动flower
    celery flower --address=127.0.0.1 --port=5555
    可通过浏览器查看
    http://127.0.0.1:5555



    
