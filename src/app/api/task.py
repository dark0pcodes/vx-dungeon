import json

from app import cache
from app.api import web
from app.core.render import Render


@web.route('/api/v1/task/<task_uuid>', methods=['GET'])
def results(task_uuid):
    """
    Given a task_uuid returns the corresponding analysis results
    Args:
        task_uuid:

    Returns:
    """
    try:
        return Render.response(json.loads(cache.get(task_uuid).decode()))
    except AttributeError:
        return Render.error('Invalid task_uuid was submitted')
    except ValueError:
        return Render.error('Task is not ready')
