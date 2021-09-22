from flask import Flask

app = Flask(__name__)
session_storage = {}

from app import routes