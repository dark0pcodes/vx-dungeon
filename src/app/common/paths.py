import os
import pathlib

ROOT_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), '..')

TESTS_PATH = os.path.join(ROOT_PATH, '..', 'tests')
CONFIG_PATH = os.path.join(ROOT_PATH, '..', '..', 'config')
STORAGE_PATH = os.path.join(ROOT_PATH, '..', '..', 'storage')
