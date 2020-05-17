import os
import pathlib

ROOT_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), '..')

TESTS_PATH = os.path.join(ROOT_PATH, 'tests')
STORAGE_PATH = os.path.join(ROOT_PATH, '..', 'storage')
