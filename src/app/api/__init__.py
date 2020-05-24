from flask import Flask

web = Flask(__name__)

from app.api.file import *
from app.api.task import *
