import os
from secrets import token_hex
from flask import current_app
from PIL import Image as _Image
from receipts_storage.app import db

class Image(db.Model):
    __tablename__ = "image"
    id = db.Column(db.Integer(), primary_key=True)
    filename = db.Column(db.String())

    def __init__(self, image, *args, **kwargs):
        img = _Image.open(image)

        location = os.path.join(current_app.root_path, current_app.config["UPLOAD_IMG_PATH"])

        # Creating the directories if needed
        if(not os.path.exists(location)):
            os.makedirs(location)

        # Generate unique filename
        filename = token_hex(8) + ".png"
        while(os.path.isfile(os.path.join(location, filename))):
            filename = secrets.token_hex(8) + ".png"
        
        # Save the image
        img.save(os.path.join(location, filename))
        self.filename = filename
        super().__init__(*args, **kwargs)
    
    def to_json(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "path": self.path
        }

    @property
    def path(self):
        return os.path.join(current_app.root_path, current_app.config["UPLOAD_IMG_PATH"], self.filename)
        