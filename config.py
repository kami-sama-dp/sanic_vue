import os

class Config:
    SECRET_KEY = 'jklklsadhfjkhwbii9/sdf\sdf'
    CSRF_ENABLED = True
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # CELERY_BROKER_URL = 'redis://localhost:6379/1'

    # 配置mq
    RABBITMQ_HOSTS = "127.0.0.1"

    RABBITMQ_PORT = 5672

    RABBITMQ_VHOST = '/'

    RABBITMQ_USER = 'guest'

    RABBITMQ_PWD = 'guest'

    CELERY_BROKER_URL = 'amqp://%s:%s@%s:%d/%s' % (RABBITMQ_USER, RABBITMQ_PWD, RABBITMQ_HOSTS, RABBITMQ_PORT, RABBITMQ_VHOST)

    @staticmethod
    def init_app(app):
        pass