from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from rotas.views import rotas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/rotas.db'
db = SQLAlchemy(app)


app.register_blueprint(rotas)

db.create_all()
