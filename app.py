import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from models import db
from urls import register_routes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + os.environ.get('POSTGRES_USER')+':' + os.environ.get('POSTGRES_PASSWORD')+'@' + os.environ.get('POSTGRES_HOST')+':' + os.environ.get('POSTGRES_PORT')+'/' + os.environ.get('POSTGRES_DB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key'


app_context = app.app_context()
app_context.push()

migrate = Migrate(app, db)
db.init_app(app)

cors = CORS(app)

register_routes(app)
