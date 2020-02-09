from sqlalchemy import func
from receipts_storage.app import db
from .color import Color

product_tags = db.Table("product_tags",
    db.Column("product_id", db.Integer(), db.ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    db.Column("tag_id", db.Integer(), db.ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True)
)

product_images = db.Table("product_images",
    db.Column("product_id", db.Integer(), db.ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    db.Column("image_id", db.Integer(), db.ForeignKey("image.id", ondelete="CASCADE"), primary_key=True)
)

class Product(db.Model):
    __tablename__ = "product"
    __searchable__ = ["name"]

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float())
    returned = db.Column(db.Boolean(), default=False)
    receipt_id = db.Column(db.Integer(), db.ForeignKey("receipt.id"), nullable=False)
    receipt = db.relationship("Receipt", back_populates="products")
    color_id = db.Column(db.Integer(), db.ForeignKey("color.id"))
    color = db.relationship("Color")
    tags = db.relationship("Tag", secondary=product_tags, lazy="subquery")
    images = db.relationship("Image", secondary=product_images, lazy="subquery")

    def __init__(self, *args, **kwargs):
        self.color = Color.query.order_by(func.random()).first()
        super().__init__(*args, **kwargs)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "returned": self.returned,
            "color": self.color.to_json(),
            "tags": [tag.to_json() for tag in self.tags],
            "images": [image.to_json() for image in self.images]
        }