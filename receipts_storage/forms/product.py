import json
from wtforms.form import Form as NoCsrfForm
from wtforms import StringField, HiddenField, MultipleFileField
from wtforms.validators import DataRequired, ValidationError

class ProductForm(NoCsrfForm):
    name = StringField("Namn", validators=[DataRequired("Detta fält är obligatoriskt.")])
    price = StringField("Pris", validators=[DataRequired("Detta fält är obligatoriskt.")])
    tags = HiddenField("Taggar")
    images = MultipleFileField("Bilder", render_kw={"accept": "image/*"})

    def validate_tags(self, tags):
        if(tags.data != ""):
            try:
                json.loads(tags.data)
            except ValueError:
                raise ValidationError("Kunde inte läsa av taggar.")