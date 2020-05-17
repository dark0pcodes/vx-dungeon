from flask import jsonify
from flask_classy import FlaskView

from app.core.tasks import test


class FileView(FlaskView):
    def get(self):
        test.delay()
        return jsonify({'status': 'OK'})
