from receipts_storage.app import db

class Tag(db.Model):
    __tablename__ = "tag"
    __searchable__ = ["name"]

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }