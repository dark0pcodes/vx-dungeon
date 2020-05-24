from celery import Celery
from celery import signals
from pymemcache.client.base import Client

from app.core.storage import MongoCtrl
from app.core.utils import load_config

# Memcached
memcached_cfg = load_config()['MEMCACHED']
cache = Client((memcached_cfg["HOST"], memcached_cfg["PORT"]))

# Celery config
mongo_cfg = load_config()['MONGO']
task_queue = Celery('tasks', broker=f'mongodb://{mongo_cfg["USERNAME"]}:{mongo_cfg["PASSWORD"]}@{mongo_cfg["HOST"]}:'
                                    f'{mongo_cfg["PORT"]}/{mongo_cfg["DATABASE"]}')
task_queue.autodiscover_tasks(['app.core'])


def init_database(**kwargs):
    MongoCtrl().connect()


signals.worker_process_init.connect(init_database)
