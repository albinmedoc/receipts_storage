import json
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, HiddenField, FieldList, FormField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired
from .fields import DatalistField
from .product import ProductForm
from ..models import Store


class ReceiptForm(FlaskForm):
    store = DatalistField("Butik", validators=[DataRequired("Detta fält är obligatoriskt.")])
    receipt_number = StringField("Kvittonummer", validators=[DataRequired("Detta fält är obligatoriskt.")])
    date = DateField("Datum", default=date.today, validators=[DataRequired("Detta fält är obligatoriskt.")])
    tags = HiddenField("Taggar")
    images = MultipleFileField("Bilder", render_kw={"accept": "image/*"})
    products = FieldList(FormField(ProductForm), min_entries=1)
    submit = SubmitField("Lägg till")

    def __init__(self):
        super(ReceiptForm, self).__init__()
        self.store.datalist = [s.name for s in Store.query.all()]

    def validate_date(self, field):
        if(field.data > date.today()):
            raise ValidationError("Kan inte vara i framtiden.")
    
    def validate_tags(self, tags):
        if(tags.data != ""):
            try:
                json.loads(tags.data)
            except ValueError:
                raise ValidationError("Kunde inte läsa av taggar.")