import os

from flask import request, send_file
from werkzeug.exceptions import BadRequestKeyError

from app.api import web
from app.common.constants import MODULES
from app.common.paths import STORAGE_PATH
from app.core.file import File
from app.core.render import Render


@web.route('/api/v1/file/submit', methods=['POST'])
def submit():
    """
    Store sample in Repo
    :return:
    """
    if 'file' not in request.files:
        return Render.error('No file was submitted')

    file_content = request.files['file']
    if file_content == b'':
        return Render.error('Empty file was submitted')

    file_content = file_content.stream.read()
    data = File.query_one(file_content=file_content)
    if data:
        return Render.response(data)
    return Render.response(File.register_file(file_content))


@web.route('/api/v1/file/<file_hash>/download', methods=['GET'])
def download(file_hash):
    """
    Download sample by hash
    :return:
    """
    type_hash = File.check_hash(file_hash)
    if type_hash:
        data = File.query_one({type_hash: file_hash})

        if data:
            return send_file(os.path.join(STORAGE_PATH, data['file_name']))
        return Render.error('File does not exist in repository')
    return Render.error('Invalid MD5/SHA1/SHA256 was submitted')


@web.route('/api/v1/file/<file_hash>/details', methods=['GET'])
def details(file_hash):
    """
    Get sample details by hash
    :return:
    """
    type_hash = File.check_hash(file_hash)
    if type_hash:
        data = File.query_one({type_hash: file_hash})

        if data:
            return Render.response(data)
        return Render.error('File does not exist in repository')
    return Render.error('Invalid MD5/SHA1/SHA256 was submitted')


@web.route('/api/v1/file/<file_hash>/related/<module>', methods=['GET'])
def related(file_hash, module):
    """
    Get similar files to a given sample
    :return:
    """
    type_hash = File.check_hash(file_hash)
    if type_hash:
        data = File.query_one({type_hash: file_hash})

        if data:
            if module == 'imp_hash':
                return Render.response(File.get_related_imp_hash(data))
            if module not in MODULES:
                return Render.error('Invalid module was submitted')
            try:
                threshold = float(request.args['threshold'])
                if threshold > 1.0 or threshold < 0.0:
                    raise ValueError
                return Render.response(File.get_related(data['_id'], module, threshold))
            except (BadRequestKeyError, ValueError):
                return Render.error('Invalid or no threshold was submitted')
        return Render.error('File does not exist in repository')
    return Render.error('Invalid MD5/SHA1/SHA256 was submitted')
