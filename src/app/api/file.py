from flask import request, jsonify, send_file
from flask_classy import FlaskView, route

from app.core.file import File


class FileView(FlaskView):
    @route('submit', methods=['POST'])
    def submit(self):
        """
        Store sample in Repo
        :return:
        """
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file was submitted'})
        file_content = request.files['file']
        if file_content == '':
            return jsonify({'status': 'error', 'message': 'Empty file was submitted'})
        return jsonify(File.register_file(file_content.stream.read()))

    def download(self, file_hash):
        """
        Download sample by hash
        :return:
        """
        data = File.get_file_path(file_hash)

        if isinstance(data, dict):
            return jsonify(data)
        return send_file(data)

    def details(self, file_hash):
        """
        Get sample details by hash
        :return:
        """
        return jsonify(File.get_file_details(file_hash))

    def advanced_search(self, file_hash):
        """
        Get similar files to a given sample
        :return:
        """
        return jsonify(File.advanced_search(file_hash, **request.args))
