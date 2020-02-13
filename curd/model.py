from peewee import *
from playhouse import pool
from passlib.apps import custom_app_context
from playhouse.fields import ManyToManyField

from curd import app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


db = pool.PooledMySQLDatabase(host='127.0.0.1', port=3306, user='root', database='test')


@app.before_request
def conn():
    print('connect Database')
    if db.is_closed():
        db.connect()


@app.teardown_request
def close(e):
    print('close Database')
    if not db.is_closed():
        db.close()


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def filter(cls, ip=None, taskname=None, report_name=None, cur_page=1, page_size=20):
        if ip:
            cls.qs = cls.select().where(cls.ip.contains(ip))
        elif taskname:
            cls.qs = cls.select().where(cls.taskname.contains(taskname))
        elif report_name:
            cls.qs = cls.select().where(cls.report_name.contains(report_name))
        else:
            cls.qs = cls.select()
        cls.result = cls.qs.order_by(cls.id).paginate(cur_page, int(page_size))
        return cls

    @classmethod
    def counts(cls):
        return cls.qs.count()

    # 通过主键id查询(结果值唯一)
    @classmethod
    def filter_by_id(cls, id):
        return cls.select().where(cls.id == id).first()


class Machine(BaseModel):
    ip = CharField()
    port = IntegerField()
    user = CharField(default='')
    coresize = IntegerField()
    mtype = BooleanField(default=False)
    desc = TextField(default='')

    class Meta:
        table_name = "machine"


class TestTask(BaseModel):
    taskname = CharField(verbose_name="任务名称", default="", max_length=100, unique=True)
    user = CharField(verbose_name="创建人")
    #testfile = FileField(verbose_name="上传任务文件", upload_to=user_directory_path)
    master = CharField(verbose_name="控制器", default='')
    slaves = CharField(default='')
    gameserver = TextField(verbose_name='被测服务器配置信息', default="未提供服务器配置信息")
    autostop = BooleanField(verbose_name="自动停止", default=False, help_text="脚本必须支持自动停止功能，此优先级高于运行时长")
    runtime = CharField(verbose_name="运行时长", default="", max_length=30, help_text="例子(300s, 20m, 3h, 1h30m)", null=True)
    testhost = CharField(verbose_name="目标主机", max_length=200, null=True)
    slaves_name = CharField(default='')
    slaves_core_size = IntegerField(default=0)

    # def clientsize(self):
    #     result = 0
    #     for slave in self.slaves.get_queryset():
    #         result += slave.coresize
    #     return result
    #
    # def getslavename(self):
    #     tmp = ""
    #     for slave in self.slaves.get_queryset():
    #         tmp += slave.ip + ','
    #     return tmp

    usersize = IntegerField(verbose_name="并发用户数", default=10)
    userspeed = IntegerField(verbose_name="每秒启动用户数", default=10)
    indextimes = CharField(verbose_name="超时指标", max_length=20, default="10,20,30")
    desc = TextField(verbose_name="备注")

    class Meta:
        table_name = 'testtask'



class User(BaseModel):
    user_name = CharField(unique=True)
    password = CharField()

    def hash_password(self, password):
        self.password = custom_app_context.hash(password)
        return self.password

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    def generate_auth_token(self, expiration=7200):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'name': str(User.user_name)})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        return data

    class Meta:
        table_name = 'user'


db.create_tables([Machine, User, TestTask], safe=True)

