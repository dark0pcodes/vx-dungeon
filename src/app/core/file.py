import hashlib
import subprocess

import pyimpfuzzy
import ssdeep


class File:
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

    def analyze(self):
        results = {}
        for analyzer in [item for item in dir(self) if '_analyzer_' in item]:
            results[analyzer[10:]] = getattr(self, analyzer)()

        return results
