from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = "abc"

from app import views
from app import models
from app import dict
from app import service