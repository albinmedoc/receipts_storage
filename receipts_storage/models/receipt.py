from datetime import date
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from receipts_storage.app import db
from ..models import Product, Color

receipt_tags = db.Table("receipt_tags",
    db.Column("receipt_id", db.Integer(), db.ForeignKey("receipt.id", ondelete="CASCADE"), primary_key=True),
    db.Column("tag_id", db.Integer(), db.ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True)
)

receipt_images = db.Table("receipt_images",
    db.Column("receipt_id", db.Integer(), db.ForeignKey("receipt.id", ondelete="CASCADE"), primary_key=True),
    db.Column("image_id", db.Integer(), db.ForeignKey("image.id", ondelete="CASCADE"), primary_key=True)
)

class Receipt(db.Model):
    __tablename__ = "receipt"
    id = db.Column(db.Integer(), primary_key=True)
    receipt_number = db.Column(db.String())
    date = db.Column(db.Date())
    payed = db.Column(db.Date())
    store_id = db.Column(db.Integer(), db.ForeignKey("store.id"))
    store = db.relationship("Store", back_populates="receipts")
    color_id = db.Column(db.Integer(), db.ForeignKey("color.id"))
    color = db.relationship("Color")
    tags = db.relationship("Tag", secondary=receipt_tags, lazy="subquery")
    images = db.relationship("Image", secondary=receipt_images, lazy="subquery")
    products = db.relationship("Product", back_populates="receipt")

    def __init__(self, *args, **kwargs):
        self.color = Color.query.order_by(func.random()).first()
        super().__init__(*args, **kwargs)

    @hybrid_property
    def sum(self):
        return sum([product.price for product in self.products])
    
    @sum.expression
    def sum(cls):
        return select([func.sum(Product.price)]).where(Product.receipt_id == cls.id).as_scalar()

    def to_json(self):
        return {
            "id": self.id,
            "receipt_number": self.receipt_number,
            "date": self.date,
            "payed": self.payed,
            "store": self.store.to_json(),
            "color": self.color.to_json(),
            "tags": [tag.to_json() for tag in self.tags],
            "images": [image.to_json() for image in self.images]
        }
    