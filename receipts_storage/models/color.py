from receipts_storage.app import db

class Color(db.Model):
    __tablename__ = "color"
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(6), unique=True)

    def to_json(self):
        return {
            "id": self.id,
            "value": self.value
        }