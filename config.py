import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SECRET_KEY = "KEBABRULLE"

    UPLOAD_IMG_PATH = "static/img/receipt_img"

    #Database
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False