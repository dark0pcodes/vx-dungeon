import os
import unittest

from app.common.paths import TESTS_PATH
from app.core.file import File


class TestFile(unittest.TestCase):
    def setUp(self):
        self.obj = File(os.path.join(
            TESTS_PATH, 'data', '736330aaa3a4683d3cc866153510763351a60062a236d22b12f4fe0f10853582')
        )
        self.results = {
            'md5': '9052d06c6ac53471f8496263f8fef2eb',
            'sha1': '73016558c8353509b15cd757063816369e9abfa7',
            'sha256': '736330aaa3a4683d3cc866153510763351a60062a236d22b12f4fe0f10853582',
            'ssdeep': '24576:HnYO/xJrstd2u3Slcfo259gy6Ym4ZrpdSdwwDtrm83zh:dbst4u3vA2PgTqpdSdvDtrm+zh',
            'imp_hash': 'd803cf4cabab38ad6ac8123e3c7a53dd',
            'imp_fuzzy': '96:oO0b11txj63OxfUv6u75tKN2Sm68eXTCdjAwhmypAhiO4uR83un:oO411txj63OxfUv6u7vJY2djO',
            'pe_sections': [
                'c2a8f0f2df948e32017da4e4741c0758',
                '65b60216c5ccca9452dd0d1fd0a343d0',
                'b4b7ec6b6bf4dfe41972c4b09d569565',
                '3df28295fcf4f22f0619dbb667c6103e',
                'c32633f1600732d51cd8162f12316160',
                'd2ae732e2833befe28cdebfac0e23e2e',
                '3f538e9cee3f455a7e53b8e3a5256d0d'
            ],
            'strings': 13810
        }

    def test_analyzers(self):
        for key, value in self.results.items():
            result = getattr(self.obj, f'_analyzer_{key}')()
            if key == 'strings':
                result = len(result)

            self.assertEqual(result, value)


if __name__ == '__main__':
    unittest.main()
