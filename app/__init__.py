from flask import Flask

app = Flask(__name__)

from app.routes import routes
from app.routes import admin_routes