import pyimpfuzzy
import ssdeep
from bson import ObjectId

from app import task_queue, cache
from app.core.file import File
from app.core.render import Render


@task_queue.task
def get_related(task_uuid):
    """
    Given a task uuid returns a list of similar samples in the repo
    Args:
        task_uuid:

    Returns:
    """
    lookup_functions = {
        'imp_fuzzy': pyimpfuzzy.hash_compare,
        'ssdeep': ssdeep.compare,
        'pe_sections': File.jaccard_index,
        'strings': File.jaccard_index
    }

    try:
        file_id, module, threshold = cache.get(task_uuid).decode().split(',')
        file_data = File.storage.query_one({'_id': ObjectId(file_id)})

        related = []
        for sample in File.storage.query({'_id': {'$ne': file_data['_id']}}):
            score = float(lookup_functions[module](file_data[module], sample[module]))
            if score > float(threshold):
                related.append({'score': score, 'file': sample})

        cache.set(task_uuid, Render.dumps(related), 3600)
    except (AttributeError, ValueError):
        pass
