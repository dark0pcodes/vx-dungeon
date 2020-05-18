from app import app, cache
from app.core.file import File


@app.task
def advanced_search(uuid):
    """

    Args:
        uuid:

    Returns:

    """
    file_hash, module, threshold = cache.get(uuid).decode().split(',')
    file_data = File.get_file_details(file_hash)
    print(file_data)

    # TODO: Add search functions for each module
    if module == 'imp_hash':
        list(File.storage.query({'imp_hash': file_data['imp_hash']}))
