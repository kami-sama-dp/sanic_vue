from flask import request, jsonify, g, make_response, abort
from curd.model import Machine, db, User, TestTask
from flask_restful import MethodView
from playhouse.shortcuts import model_to_dict
from fabric.api import settings, run, cd, put

from . import auth, BASE_DIR
import json
import os

zip_name = 'run.zip'


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
                local_ip = json_data['local_ip']
                port = json_data['port']
                coresize = json_data['coresize']
                mtype = json_data['mtype']
                desc = json_data['desc']
                Machine.create(ip=ip, port=port, coresize=coresize, mtype=mtype, desc=desc, local_ip=local_ip)
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
            local_ip = json_data['local_ip']
            ip = json_data['ip']
            port = json_data['port']
            coresize = json_data['coresize']
            mtype = json_data['mtype']
            desc = json_data['desc']
            Machine.update(ip=ip, port=port, coresize=coresize, mtype=mtype, desc=desc, local_ip=local_ip)\
                .where(Machine.id == id).execute()
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
            file = request.files.get('file')
            data = request.form.get('data')
            json_data = json.loads(data.encode('utf-8').decode('utf-8'))
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
            slaves_core_size = ''
            slaves_name = ''
            slave_local_ip = ''
            target = os.path.join(os.getcwd(), 'files')
            if not os.path.isdir(target):
                os.mkdir(target)
            if file is not None:
                destination = '/'.join([target, taskname + '_' + file.filename])
                file.save(destination)
            with db.atomic():
                # 先判重
                test_task = TestTask.select().where(TestTask.taskname == taskname).first()
                master_local_ip = Machine.select().where(Machine.ip == master).first().local_ip
                if test_task is None:
                    for slave_id in slaves:
                        machine = Machine.filter_by_id(id=slave_id)
                        slaves_core_size += str(machine.coresize) + ','
                        slaves_name += machine.ip + ','
                        slave_local_ip += machine.local_ip + ','
                    TestTask.create(taskname=taskname, user=username, master=master, gameserver=gameserver,
                                    slaves=slaves, autostop=autostop, runtime=runtime, testhost=testhost,
                                    usersize=usersize, userspeed=userspeed, indextimes=indextimes, desc=desc,
                                    slaves_name=slaves_name[:-1], slaves_core_size=slaves_core_size[:-1],
                                    master_local_ip=master_local_ip, slave_local_ip=slave_local_ip[:-1])
                    return "true"
                else:
                    return jsonify({'msg': '任务名称已存在', 'code': 0})
        except Exception as e:
            return jsonify({'msg': e})

    @auth.login_required
    def put(self):
        try:
            file = request.files.get('file')
            data = request.form.get('data')
            json_data = json.loads(data.encode('utf-8').decode('utf-8'))
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
            slaves_core_size = ''
            slaves_name = ''
            slave_local_ip = ''
            target = os.path.join(os.getcwd(), 'files')
            if not os.path.isdir(target):
                os.mkdir(target)
            if file is not None:
                destination = '/'.join([target, taskname + '_' + file.filename])
                file.save(destination)
            with db.atomic():
                master_local_ip = Machine.select().where(Machine.ip == master).first().local_ip
                for slave_id in slaves:
                    machine = Machine.filter_by_id(id=slave_id)
                    slaves_core_size += str(machine.coresize) + ','
                    slaves_name += machine.ip + ','
                    slave_local_ip += machine.local_ip + ','
                TestTask.update(taskname=taskname, user=username, master=master, gameserver=gameserver,
                                slaves=slaves, autostop=autostop, runtime=runtime, testhost=testhost,
                                usersize=usersize, userspeed=userspeed, indextimes=indextimes, desc=desc,
                                slaves_name=slaves_name[:-1], slaves_core_size=slaves_core_size[:-1],
                                master_local_ip=master_local_ip, slave_local_ip=slave_local_ip[:-1]).\
                    where(TestTask.taskname == taskname).execute()
                return "true"
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
                token = g.user.generate_auth_token()
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

class run_task(MethodView):
    # 执行任务前先把zip包传到相应的slaves和master上, 并解压
    @auth.login_required
    async def post(self):
        try:
            data = request.get_data()
            json_data = json.loads(data)
            task_name = json_data['task_name']
            master_ip = json_data['master']
            slaves_name = json_data['slaves_name']
            file_name = json_data['task_name'] + '_' + zip_name
            master_local_ip = json_data['master_local_ip']
            usersize = json_data['usersize']
            userspeed = json_data['userspeed']
            autostop = json_data['autostop']
            runtime = json_data['runtime']
            slaves_core_size = json_data['slaves_core_size']
            testhost = json_data['testhost']
            slave_num = 0  # 用来计算一共slave有多少核心
            print(json_data)
            # 任务设置了目标主机时，使用新的目标主机进行测试
            if testhost != "" and testhost is not None:
                adhost = " -H " + testhost
            else:
                adhost = ""
            # 如果设置了自动停止，不加入 -t参数，
            if autostop == '是':
                runtimestring = ""
            else:
                if runtime != "" and runtime is not None:
                    runtimestring = " -t " + runtime + " "
                else:
                    # runtime 为空时添加默认300s
                    runtimestring = " -t 300s "
            # 上传文件到slaves
            for index, slave_ip in enumerate(slaves_name):
                slave_num += int(slaves_core_size[index])
                clean(task_name=task_name, host_string=slave_ip, user="root")
                fab_unzip(task_name=task_name, filename=file_name, host_string=slave_ip, user='root')
                for i in range(int(slaves_core_size[index])):
                    # 客户端服务器启动时放入后台执行，因为控制器服务器结束时，客户端会自动结束
                    slavecommand = "nohup locust --slave " + adhost \
                                   + " --no-reset-stats --logfile /home/dengpu/locustlogs/locust" \
                                   + str(i) + ".log --master-host  " + str(master_local_ip) \
                                   + " --master-port 6607 -f /home/dengpu/locustfile/" + task_name + '/'\
                                   + file_name[-7:-4] + ".py >& /dev/null < /dev/null &"
               #     print(slavecommand)
                    fabrun(slavecommand, slave_ip, user='root')

            # 上传文件到master上
            clean(task_name=task_name, host_string=master_ip, user='root')
            fab_unzip(task_name=task_name, filename=file_name, host_string=master_ip, user='root')

            master_command = "locust --master --no-web  --no-reset-stats --expect-slaves  " + str(slave_num) + \
                             " --logfile /home/dengpu/locustlogs/locust.log --only-summary --master-bind-host " + \
                             str(master_local_ip) + " --master-bind-port 6607 --csv /home/dengpu/locustresult/" +\
                             task_name + '/' + " -c " + \
                             str(usersize) + " -r " + str(userspeed) + runtimestring +\
                             " -f /home/dengpu/locustfile/" + task_name + '/' + file_name[-7:-4] +\
                             ".py >& /dev/null < /dev/null"
            print(master_command)
            fabrun(master_command, master_ip, user='root')
            return "true"
        except Exception as e:
            return jsonify({'msg': e})


# 上传文件至远程服务器
# 需要加锁、 防止2个用户上传同一个任务
def fab_unzip(task_name, filename, host_string, user):
    with settings(host_string=host_string, user=user):
        run('mkdir -p  /home/dengpu/locustfile/' + task_name)
        run('mkdir -p  /home/dengpu/locustlogs/' + task_name)
        run('mkdir -p  /home/dengpu/locustresult/' + task_name)
        put(local_path=BASE_DIR + '/files/' + filename, remote_path='/home/dengpu/locustfile/' + task_name + '/')
        with cd('/home/dengpu/locustfile/' + task_name):
            run('unzip ' + filename)
            run('rm -rf ' + filename)


#  删除对应测试任务的文件夹
def clean(task_name, host_string, user):
    with settings(host_string=host_string, user=user):
        run("rm -rf  /home/dengpu/locustfile/" + task_name)
        run("rm -rf  /home/dengpu/locustlogs/" + task_name)
        run("rm -rf  /home/dengpu/locustresult/" + task_name)


def fabrun(command, host_string, user):
    with settings(host_string=host_string, user=user):
        # 设置pty=False，避免因为Fabric退出导致进程的退出
        run(command, quiet=True, pty=False)


