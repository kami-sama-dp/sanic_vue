from peewee import *
from playhouse import pool

db = pool.PooledMySQLDatabase(host='127.0.0.1',port=3306, user='root', database='test',password='123456')


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def filter(cls, ip=None, task_name=None, report_name=None, cur_page=1, page_size=20):
        if not ip and  not task_name and not  report_name:
            cls.qs = cls.select()
        elif  ip:
            cls.qs = cls.select().where(cls.ip.contains(ip))
        elif  task_name:
            cls.qs = cls.select().where(cls.task_name.contains(task_name))
        elif  report_name:
            cls.qs = cls.select().where(cls.report_name.contains(report_name))
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

db.create_tables([Machine])