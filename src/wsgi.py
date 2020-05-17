from subprocess import Popen

from flask import Flask
from waitress import serve

from api.endpoint.file import FileView

app = Flask(__name__)

# Register Views
FileView.register(app)


if __name__ == '__main__':
    celery = Popen(['celery', '-A', 'app', 'worker', '--concurrency=2'])
    serve(app, host='0.0.0.0', port=8080)
