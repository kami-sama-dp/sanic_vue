from flask import request, jsonify, g, make_response, abort
from curd.model import Machine, db, User, TestTask
from flask_restful import MethodView
from playhouse.shortcuts import model_to_dict
from . import auth
import json


class all_machine(MethodView):
    # 获取服务器列表接口
    @auth.login_required
    def get(self):
        try:
            ip, page_size = request.args.get('ip'), request.args.get('pageSize')
            cur_page = request.args.get('curPage', 1, type=int)
            qs = Machine.filter(ip=ip, cur_page=cur_page, page_size=page_size)
            result = [model_to_dict(row) for row in qs.result.iterator()]
            return jsonify({
                'result': result,
                'total': Machine.counts(),
                "cur_page": cur_page
            })
        except Exception as e:
            return jsonify({'msg': e})

    # 新增
    @auth.login_required
    def post(self):
        try:
            data = request.get_data()
            json_data = json.loads(data.decode('utf-8'))
            with db.atomic():
                ip = json_data['ip']
                port = json_data['port']
                coresize = json_data['coresize']
                mtype = json_data['mtype']
                desc = json_data['desc']
                Machine.create(ip=ip, port=port, coresize=coresize, mtype=mtype, desc=desc)
            return 'true'
        except Exception as e:
            return jsonify({'msg': e})

    # 修改
    @auth.login_required
    def put(self):
        try:
            data = request.get_data()
            json_data = json.loads(data.decode('utf-8'))
            id = json_data['id']
            ip = json_data['ip']
            port = json_data['port']
            coresize = json_data['coresize']
            mtype = json_data['mtype']
            desc = json_data['desc']
            Machine.update(ip=ip, port=port, coresize=coresize, mtype=mtype, desc=desc).where(Machine.id == id).execute()
            return 'true'
        except Exception as e:
            return jsonify({'msg': e})

    # 删除
    @auth.login_required
    def delete(self):
        try:
            data = request.get_json()
            id = data['id']
            Machine.delete().where(Machine.id == id).execute()
            return 'true'
        except Exception as e:
            return jsonify({'msg': e})


class test_task_action(MethodView):
    # 测试任务相关接口
    @auth.login_required
    def get(self):
        try:
            task_name, page_size = request.args.get('task_name'), request.args.get('pageSize')
            cur_page = request.args.get('curPage', 1, type=int)
            qs = TestTask.filter(taskname=task_name, cur_page=cur_page, page_size=page_size)
            _result = [model_to_dict(row) for row in qs.result.iterator()]
            return jsonify({
                'result': _result,
                'total': TestTask.counts(),
                "cur_page": cur_page
            })
        except Exception as e:
            return jsonify({'msg': e})

    @auth.login_required
    def post(self):
        try:
            data = request.get_data()
            json_data = json.loads(data.decode('utf-8'))
            print(json_data)
            username = json_data['username']
            taskname = json_data['taskname']
            master = json_data['master']
            slaves = json_data['slaves']
            gameserver = json_data['gameserver']
            autostop = json_data['autostop']
            runtime = json_data['runtime']
            testhost = json_data['testhost']
            usersize = json_data['usersize']
            userspeed = json_data['userspeed']
            indextimes = json_data['indextimes']
            desc = json_data['desc']
            slaves_core_size = 0
            slaves_name = ''
            with db.atomic():
                # 先判重
                test_task = TestTask.select().where(TestTask.taskname == taskname).first()
                if test_task is None:
                    for slave_id in slaves:
                        machine = Machine.filter_by_id(id=slave_id)
                        slaves_core_size += machine.coresize
                        slaves_name += machine.ip + ','
                    TestTask.create(taskname=taskname, user=username, master=master, gameserver=gameserver,
                                    slaves=slaves, autostop=autostop, runtime=runtime, testhost=testhost,
                                    usersize=usersize, userspeed=userspeed, indextimes=indextimes, desc=desc,
                                    slaves_name=slaves_name[:-1], slaves_core_size=slaves_core_size)
                    return 'true'
                else:
                    return jsonify({'msg': '任务名称已存在', 'code': 0})
        except Exception as e:
            return jsonify({'msg': e})

    @auth.login_required
    def put(self):
        try:
            data = request.get_data()
            json_data = json.loads(data.decode('utf-8'))
            print(json_data)
            return 'put'
        except Exception as e:
            return jsonify({'msg': e})

    @auth.login_required
    def delete(self):
        try:
            data = request.get_json()
            id = data['id']
            TestTask.delete().where(TestTask.id == id).execute()
            return 'true'
        except Exception as e:
            return jsonify({'msg': e})










# 登录接口, 查不到则直接注册
class admin_register(MethodView):
    @auth.login_required
    def post(self):
        try:
            if hasattr(g, 'user'):
                print("密码验证通过--------")
                token = g.user.generate_auth_token()
                print('token:   ', token)
                return jsonify({'token': token.decode('ascii')})
            else:
                return make_response(jsonify({'error': '密码错误!'}), 401)
        except Exception as e:
            return jsonify({'msg': e})


@auth.verify_password
def verify_password(username_or_token, client_password):
    if request.path == "/api/login/":
        json_data = json.loads(request.get_data().decode('utf-8'))
        user_name = json_data['username']
        pwd = json_data['password']
        user = User.select().where(User.user_name == user_name).first()
        if user is not None and not user.verify_password(pwd):
            abort(403)
        elif user is None:
            password = User().hash_password(pwd)
            user = User.create(user_name=user_name, password=password)
    else:
        user = User.verify_auth_token(username_or_token)
        if not user:
            abort(401)
    g.user = user
    return True

