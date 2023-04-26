from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class loginForm(FlaskForm):
    email=StringField(label='Email')
    motdepasse=PasswordField(label='Mot de passe')
    
