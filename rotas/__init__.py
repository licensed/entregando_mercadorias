from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/rotas.db'
db = SQLAlchemy(app)

from rotas.views import rotas

app.register_blueprint(rotas)

db.create_all()
