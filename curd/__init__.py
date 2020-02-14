from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from flask_httpauth import HTTPBasicAuth
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)
api = Api(app)
CORS(app)
app.config.from_object(Config)
auth = HTTPBasicAuth()

from . import controller
api.add_resource(controller.all_machine, '/api/machine/')
api.add_resource(controller.admin_register, '/api/login/')
api.add_resource(controller.test_task_action, '/api/test_task/')
api.add_resource(controller.run_task, '/api/runTask/')
