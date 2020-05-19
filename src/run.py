from subprocess import Popen

from flask import Flask
from waitress import serve

from app.api.file import FileView
from app.core.storage import MongoCtrl
from app.core.utils import create_storage

app = Flask(__name__)

# Register Views
FileView.register(app)


if __name__ == '__main__':
    celery = Popen(['celery', '-A', 'app', 'worker', '--concurrency=2'])
    create_storage()
    MongoCtrl().connect()

    serve(app, host='0.0.0.0', port=8080)
