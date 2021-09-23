from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class DbBinds:
    schedule = 'schedule'


app = Flask(__name__)
app.config['SQLALCHEMY_BINDS'] = {
    DbBinds.schedule: 'sqlite:///./../db/schedule.db'
}
db = SQLAlchemy(app)

from app import routes

db.create_all(bind=DbBinds.schedule)
