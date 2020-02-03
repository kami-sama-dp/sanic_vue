from peewee import *
from playhouse import pool
from passlib.apps import custom_app_context
from curd import app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


db = pool.PooledMySQLDatabase(host='127.0.0.1',port=3306, user='root', database='test',password='123456')


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
    def filter(cls, ip=None, task_name=None, report_name=None, cur_page=1, page_size=20):
        if ip:
            cls.qs = cls.select().where(cls.ip.contains(ip))
        elif task_name:
            cls.qs = cls.select().where(cls.task_name.contains(task_name))
        elif report_name:
            cls.qs = cls.select().where(cls.report_name.contains(report_name))
        else:
            cls.qs = cls.select()
        cls.result = cls.qs.order_by(cls.id).paginate(cur_page, int(page_size))
        return cls

    @classmethod
    def counts(cls):
        return cls.qs.count()


class Machine(BaseModel):
    ip = CharField()
    port = IntegerField()
    user = CharField(default='')
    coresize = IntegerField()
    mtype = BooleanField(default=False)
    desc = TextField(default='')

    class Meta:
        table_name = "machine"


class User(BaseModel):
    user_name = CharField(unique=True)
    password = CharField()

    def hash_password(self, password):
        self.password = custom_app_context.hash(password)
        return self.password

    def verify_password(self,password):
        return custom_app_context.verify(password, self.password)

    def generate_auth_token(self,expiration=7200):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'name': str(User.user_name)})

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



db.create_tables([Machine, User], safe=True)

