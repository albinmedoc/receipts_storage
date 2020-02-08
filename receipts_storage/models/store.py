from receipts_storage.app import db

class Store(db.Model):
    __tablename__ = "store"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    receipts = db.relationship("Receipt", back_populates="store")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
    