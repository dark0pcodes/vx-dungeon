import json

from bson import ObjectId


class Render(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

    @classmethod
    def error(cls, message):
        return json.dumps({'status': 'error', 'message': message})

    @classmethod
    def response(cls, data):
        return json.dumps({'status': 'success', 'data': data}, cls=Render)

    @classmethod
    def dumps(cls, data):
        return json.dumps(data, cls=Render)
