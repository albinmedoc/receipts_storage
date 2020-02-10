from receipts_storage.app import db

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f"Role('{self.id}', '{self.name}')"