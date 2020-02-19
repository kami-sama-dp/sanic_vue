import os

class Config:
    SECRET_KEY = 'jklklsadhfjkhwbii9/sdf\sdf'
    CSRF_ENABLED = True
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'

    @staticmethod
    def init_app(app):
        pass