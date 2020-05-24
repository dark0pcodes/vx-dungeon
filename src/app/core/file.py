import hashlib
import json
import os
import re
import subprocess
import uuid
from time import sleep

import pyimpfuzzy
import ssdeep

from app import cache
from app.common.constants import REGEX_HASH
from app.common.paths import STORAGE_PATH
from app.core.storage import Storage


# TODO: Implement MIN_HASHES
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

    @staticmethod
    def jaccard_index(list_a: list, list_b: list):
        """
        Compute the Jaccard index over two lists
        Args:
            list_a:
            list_b:

        Returns:
        """
        a, b = set(list_a), set(list_b)
        return len(a.intersection(b)) / len(a.union(b))

    @classmethod
    def check_hash(cls, file_hash: str):
        """
        Check if a file hash is valid
        Args:
            file_hash:

        Returns:
        """
        for key, value in REGEX_HASH.items():
            if re.match(value, file_hash):
                return key

    @classmethod
    def query_one(cls, query: dict = None, file_content: bytes = None):
        """

        Args:
            query:
            file_content:

        Returns:
        """
        if file_content:
            return cls.storage.query_one({'sha256': hashlib.sha256(file_content).hexdigest()})
        return cls.storage.query_one(query)

    @classmethod
    def register_file(cls, file_content: bytes):
        """
        Store file in disk and database
        Args:
            file_content:

        Returns:

        """
        file_path = os.path.join(STORAGE_PATH, str(uuid.uuid4()))

        with open(file_path, 'wb') as f:
            f.write(file_content)

        file_obj = cls(file_path)
        return cls.storage.query_one({'_id': cls.storage.save_one(file_obj.analysis()).inserted_id})

    @classmethod
    def get_related_imp_hash(cls, file_data):
        """
        Return all files matching the imp_hash
        Args:
            file_data:

        Returns:
        """
        return list(cls.storage.query({'imp_hash': file_data['imp_hash'], '_id': {'$ne': file_data['_id']}}))

    @classmethod
    def get_related(cls, file_id, module, threshold):
        """
        Given a file_id returns a list of similar samples in the repo
        Returns:
        """
        task_uuid = str(uuid.uuid4())

        # Set cache and trigger async task
        cache.set(task_uuid, f'{file_id},{module},{threshold}', 3600)

        from app.core.tasks import get_related

        # Launch Async task
        get_related.delay(task_uuid)

        for i in range(0, 10):
            cached_data = cache.get(task_uuid).decode()
            try:
                return json.loads(cached_data)
            except ValueError:
                sleep(0.1)
        return {'task_id': task_uuid}
