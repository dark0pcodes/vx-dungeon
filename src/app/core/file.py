import hashlib
import os
import re
import subprocess
import uuid

import pyimpfuzzy
import ssdeep

from app import cache
from app.common.constants import REGEX_HASH
from app.common.paths import STORAGE_PATH
from app.core.storage import Storage


class File:
    storage = Storage('files')

    def __init__(self, file_path: str):
        with open(file_path, 'rb') as f:
            self.file_buffer = f.read()
        self.pe = pyimpfuzzy.pefileEx(data=self.file_buffer)
        self.file_path = file_path

    def _analyzer_md5(self):
        """
        Compute MD5
        :return:
        """
        return hashlib.md5(self.file_buffer).hexdigest()

    def _analyzer_sha1(self):
        """
        Compute SHA1
        :return:
        """
        return hashlib.sha1(self.file_buffer).hexdigest()

    def _analyzer_sha256(self):
        """
        Compute SHA256
        :return:
        """
        return hashlib.sha256(self.file_buffer).hexdigest()

    def _analyzer_ssdeep(self):
        """
        Compute SSDEEP
        :return:
        """
        return ssdeep.hash(self.file_buffer)

    def _analyzer_imp_hash(self):
        """
        Compute ImpHash
        :return:
        """
        return self.pe.get_imphash()

    def _analyzer_imp_fuzzy(self):
        """
        Compute ImpFuzzyHash
        :return:
        """
        return pyimpfuzzy.get_impfuzzy_data(self.file_buffer)

    def _analyzer_pe_sections(self):
        """
        Compute PE sections MD5
        :return:
        """
        return [section.get_hash_md5() for section in self.pe.sections]

    def _analyzer_strings(self):
        """
        Extract ASCII and Unicode Strings
        :return:
        """
        strings = []
        for cmd in (['strings', '-e', 'l'], ['strings']):
            cmd.extend([self.file_path])
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()
            [strings.append(item) for item in stdout.decode().split('\n') if item]

        return strings

    def analysis(self):
        """
        Run all analyzers in the class
        :return:
        """
        results = {
            'file_name': self.file_path.split('/')[-1]
        }
        for analyzer in [item for item in dir(self) if '_analyzer_' in item]:
            results[analyzer[10:]] = getattr(self, analyzer)()

        return results

    @classmethod
    def register_file(cls, file_content: bytes):
        """
        Store file in disk and database
        Args:
            file_content:

        Returns:

        """
        if not cls.storage.query_one({'sha256': hashlib.sha256(file_content).hexdigest()}):
            file_path = os.path.join(STORAGE_PATH, str(uuid.uuid4()))

            with open(file_path, 'wb') as f:
                f.write(file_content)

            file_obj = cls(file_path)
            cls.storage.save_one(file_obj.analysis())
            return {'status': 'success', 'message': 'File was successfully stored'}
        return {'status': 'error', 'message': 'File already exists in repository'}

    @classmethod
    def get_file_details(cls, file_hash: str):
        """
        Given a valid hash returns the corresponding bytes
        Args:
            file_hash:

        Returns:
        """
        for key, value in REGEX_HASH.items():
            if re.match(value, file_hash):
                try:
                    data = cls.storage.query_one({key: file_hash})
                    data.pop('_id')
                    return data
                except AttributeError:
                    return {'status': 'error', 'message': 'File does not exist in repository'}
        return {'status': 'error', 'message': 'Not valid MD5/SHA1/SHA256 was submitted'}

    @classmethod
    def get_file_path(cls, file_hash: str):
        """
        Given a file hash returns the file path in disk
        Args:
            file_hash:

        Returns:

        """
        data = cls.get_file_details(file_hash)
        if 'status' not in data:
            return os.path.join(STORAGE_PATH, data['file_name'])
        return data

    @classmethod
    def advanced_search(cls, file_hash, **kwargs):
        """
        Given a file_hash returns a list of similar samples in the repo
        Returns:
        """
        task_uuid = str(uuid.uuid4())
        # TODO: Verify threshold and module in kwargs

        # Set cache and trigger async task
        cache.set(task_uuid, '{},{module},{threshold}'.format(file_hash, **kwargs), 3600)

        from app.core.tasks import advanced_search

        advanced_search.delay(task_uuid)
        return {'task_id': task_uuid}
