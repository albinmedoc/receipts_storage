from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from receipts_storage.models import User
from receipts_storage.app import bcrypt

class LoginForm(FlaskForm):
    username = StringField("Användarnamn", validators=[DataRequired("Detta fält är obligatoriskt.")])
    password = PasswordField("Lösenord", validators=[DataRequired("Detta fält är obligatoriskt.")])
    submit = SubmitField("Logga in")

    def validate_username(self, username):
        user = User.query.filter(username=username.data).first()
        if(not user):
            raise ValidationError("Användarnamnet är inte registrerad.")
    
    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if(user and not bcrypt.check_password_hash(user.password, password.data)):
            raise ValidationError("Lösenordet matchar inte användarnamnet.")


class RegisterForm(FlaskForm):
    firstname = StringField("Förnamn", validators=[DataRequired("Detta fält är obligatoriskt.")])
    lastname = StringField("Efternamn", validators=[DataRequired("Detta fält är obligatoriskt.")])
    username = StringField("Användarnamn", validators=[DataRequired("Detta fält är obligatoriskt.")])
    password = PasswordField("Lösenord", validators=[DataRequired("Detta fält är obligatoriskt.")])
    submit = SubmitField("Skapa användare")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if(user):
            raise ValidationError("Användarnamnet är upptaget.")


class EditUserForm(FlaskForm):
    firstname = StringField("Förnamn", validators=[DataRequired("Detta fält är obligatoriskt.")])
    lastname = StringField("Efternamn", validators=[DataRequired("Detta fält är obligatoriskt.")])
    username = StringField("Användarnamn", validators=[DataRequired("Detta fält är obligatoriskt.")])
    password = PasswordField("Lösenord", validators=[DataRequired("Detta fält är obligatoriskt.")])
    submit = SubmitField("Spara")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if(not user or not user.username == current_user.username):
            raise ValidationError("Användarnamnet är upptaget.")