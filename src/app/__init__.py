from celery import Celery

from app.common.utils import load_config

# Celery config
mongo_cfg = load_config('base')['MONGO']
app = Celery('tasks', broker=f'mongodb://{mongo_cfg["USERNAME"]}:{mongo_cfg["PASSWORD"]}@{mongo_cfg["HOST"]}:'
                             f'{mongo_cfg["PORT"]}/{mongo_cfg["DATABASE"]}')
app.autodiscover_tasks(['app.core'])
