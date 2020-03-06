# 压测平台(locust为核心) V1.0
 前端Vue， 后端flask
 
最好在chrome下打开，safari 有些样式初次加载有问题

技术栈：Vue + Vuex + ElementUI + flask + peewee + HTTPBasicAuth + celery + fabric (前后端分离MVVM模式)

目前前端处理跨域问题, 后期可优化成后端处理

pymonitor.py 可以监控python脚本的实时变化, 简单模拟一个服务端热更新功能


##  实现的模块：
 
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
    
  启动redis(不启动 报告界面无法获取数据)
  
    nohup redis-server > web6.log 2>&1 < /dev/null&
   
 安装rabbitmq:(可以不使用, 用redis代替)
 
     brew install rabbitmq
     cd  /usr/local/Cellar/rabbitmq/3.8.2 （安装目录）
  
 安装RabiitMQ的可视化监控插件
 
    sudo sbin/rabbitmq-plugins enable rabbitmq_management

 配置rabbitmq环境变量

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

## Linux下的配置：

  使用supervisord
  
    pip install supervisor
    在根目录下添加配置:
    echo_supervisord_conf> supervisord.conf 
    [program:celeryd]
    command=celery worker -A curd.celery -l info  -f celery.log   --concurrency=15
    ;stdout_logfile=/var/log/celery/celeryd.log
    ;stderr_logfile=/var/log/celery/celeryd.log
    autostart=true
    autorestart=true
    startsecs=10

    启动
    supervisord
    重启
    supervisorctl reload
    
   在linux上部署flask生产环境
       
     pip install gunicorn
     vim gunicorn.sh
     nohup gunicorn -w 4 -b 0.0.0.0:8888 run:app > gunicorn.log 2>&1 & 
     sh gunicorn.sh 
     -w 4是指预定义的工作进程数为4，
     -b 127.0.0.1:4000指绑定地址和端口
     
   部署Vue(nginx)
        
     在linux上打包得到dist
     /usr/local/nginx/conf
     在nginx.conf 第一行修改 user root;(解决403问题)
     sudo ./nginx -s stop(reload)停止nginx(重新加载conf)
     ps axu | grep nginx
     nginx -t 查看具体使用那个conf  -c + 路径(具体哪个conf)
     
     
   Linux下mysql中文乱码:
    
     locate my.cnf
     ps aux|grep mysql|grep 'my.cnf'(查看是否使用了指定目录的my.cnf)
     mysql --help|grep 'my.cnf'(查看mysql默认读取my.cnf的目录, 顺序排前的优先。)
     [mysqld]
     character-set-server=utf8
     [client]
     default-character-set=utf8
     [mysql]
     default-character-set=utf8
     show full columns from machine; 查询表的字符编码
     sudo  service mysqld restart  (重启mysql)
     show variables like 'character%';    查看数据库的编码格式
     
     show create database test; 查看数据库字符编码
     alter database test default character set utf8 collate utf8_general_ci;
     更改数据库字符编码
     
     alter table `表名` convert to character set utf8;
       一次性修改表中所有字段的字符集语句
   
   在linux上用gunicorn部署flask
   
     touch  gunicorn.sh
     nohup gunicorn -w 1 -b 0.0.0.0:8888 run:app > gunicorn.log 2>&1 &