from flask import Flask

from web.api.file import FileView

app = Flask(__name__)

# Register Views
FileView.register(app)
