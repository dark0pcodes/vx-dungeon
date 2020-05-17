import hashlib


class File:
    def __init__(self, file_buffer: bytes):
        self.file_buffer = file_buffer

    def _md5(self):
        """
        Compute MD5

        :return:
        """
        return hashlib.md5(self.file_buffer).hexdigest()

    def _sha1(self):
        """
        Compute SHA1
        :return:
        """
        return hashlib.sha1(self.file_buffer).hexdigest()

    def _sha256(self):
        """
        Compute SHA256

        :return:
        """
        return hashlib.sha256(self.file_buffer).hexdigest()
