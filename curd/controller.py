from flask import Blueprint, request, jsonify
from curd.model import Machine, db
from flask_restful import Resource
from playhouse.shortcuts import dict_to_model,model_to_dict
import json

class all_machine(Resource):
    # 获取服务器列表接口
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
            Machine.update(ip=ip, port=port, coresize=coresize, mtype=mtype, desc=desc).where(Machine.id==id).execute()
            return 'true'
        except Exception as e:
            return jsonify({'msg': e})

    # 删除
    def delete(self):
        try:
            data = request.get_json()
            id = data['id']
            Machine.delete().where(Machine.id==id).execute()
            return 'true'
        except Exception as e:
            return jsonify({'msg': e})

