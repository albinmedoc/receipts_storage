from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

app = Flask(__name__)
db = SQLAlchemy()
login = LoginManager()
bcrypt = Bcrypt()

def create_app(config=Config, create_db=False):
    app.config.from_object(config)

    db.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)


    from receipts_storage.routes import bp_receipt, bp_main

    app.register_blueprint(bp_receipt)
    app.register_blueprint(bp_main)

    if(create_db):
        with app.test_request_context():
            from receipts_storage.models import Color, Image, Product, Receipt, Store, Tag
            db.create_all()

    return app