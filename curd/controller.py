from flask import Blueprint, request, jsonify
from curd.model import Machine, db
from playhouse.shortcuts import dict_to_model,model_to_dict
import json

bp = Blueprint('bp_curd',__name__,url_prefix='/api/')

@bp.route('get_machine')
def get_machine():
    try:
        ip, page_size = request.args.get('ip'), request.args.get('pageSize')
        cur_page = request.args.get('curPage', 1, type=int)
        qs = Machine.filter(ip=ip, cur_page=cur_page, page_size=page_size)
        result = [model_to_dict(row) for row in qs.result.iterator()]
        return jsonify({
            'result': result,
            'total':Machine.counts()
        })
    except Exception as e:
        return jsonify({
            'msg':e
        })



@bp.route('add_machine', methods=['POST'])
def add_machine():
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        json_data = json.loads(data.decode('utf-8'))
        print(json_data)
        with db.atomic():
            ip = json_data['ip']
            port = json_data['port']
            coresize = json_data['coresize']
            mtype = json_data['mtype']
            print(mtype)
            print(type(mtype))

            desc = json_data['desc']
            a = Machine(ip=ip, port=port, coresize=coresize, mtype=mtype, desc=desc)
            b = a.save()
        return 'true'
