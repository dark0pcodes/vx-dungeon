import unittest

from app.core.file import File


class TestFile(unittest.TestCase):
    def setUp(self):
        self.obj = File(b'Lorem ipsum dolor sit amet,')

    def test_md5(self):
        self.assertEqual(self.obj._md5(), '059e5714948c77a56a5376310e9dc0c9')

    def test_sha1(self):
        self.assertEqual(self.obj._sha1(), '004faf620a8a553376e17f8543bd41d46bc6020c')

    def test_sha256(self):
        self.assertEqual(self.obj._sha256(), '7a1fdb8b8cbba4430197c2611b39326a63505e8b8c4af717ec0d86683943761c')


if __name__ == '__main__':
    unittest.main()
