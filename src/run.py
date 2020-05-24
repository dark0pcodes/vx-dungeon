from subprocess import Popen

from waitress import serve

from app.api import web
from app.core.storage import MongoCtrl
from app.core.utils import create_storage

if __name__ == '__main__':
    celery = Popen(['celery', '-A', 'app', 'worker', '--concurrency=2'])
    create_storage()
    MongoCtrl().connect()

    serve(web, host='0.0.0.0', port=8080)
