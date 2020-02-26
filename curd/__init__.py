# -*- coding: UTF-8 -*-
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from celery import Celery
from flask_httpauth import HTTPBasicAuth
import os

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
# 时区
celery.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
celery.conf.enable_utc = True

auth = HTTPBasicAuth()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 创建Flask App的工厂函数
def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(Config)
  return app


# 创建celery的工厂函数
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    # celery.conf.update(app.config)


    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    # 将app_context 包含在celery.Task中，这样让其他的Flask扩展也能正常使用
    celery.Task = ContextTask
    return celery


app = create_app('default')
api = Api(app)

CORS(app, resources=r'/*')

from . import controller

api.add_resource(controller.all_machine, '/api/machine/')
api.add_resource(controller.admin_register, '/api/login/')
api.add_resource(controller.test_task_action, '/api/test_task/')
api.add_resource(controller.run_task, '/api/runTask/')
api.add_resource(controller.all_report, '/api/reportList/')
api.add_resource(controller.report_detil, '/api/report_detail/')



