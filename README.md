# flask_vue
最好在chrome下打开，safari 有些样式初次加载有问题


    使用celery实现分布式异步任务处理

    celery worker -A curd.celery -l info  -f celery.log 

    启动celery worker 更改celery配置需要重启celery
  
 消息队列存放在rabbitmq或者redis(broker中间件)
 
 结果存在redis(backend)
 
   启动前端(Vue)： 
   
    需要安装node 和yarn 
    cd frontend
    yarn run serve 
   
  启动后端(flask)
  
    nohup python3  run.py >/dev/null 2>&1 &
    
  启动redis
  
    nohup redis-server > web6.log 2>&1 < /dev/null&
   
 实现的模块：
 
    1. 登录注册(带token，过期验证) 使用的peewee(orm)
    2. CRUD服务器资源列表、测试任务列表
    3. 展示测试报告(locust)
    4. 上传文件到远程服务器, fabric远程操作linux命令,