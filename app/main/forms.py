from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField

#for the picture upload
from flask_wtf.file import FileField,FileAllowed

from wtforms import ValidationError
from wtforms.validators import DataRequired,Email
from ..models import User


class UpdateProfileForm(FlaskForm):
    '''
    class to create a form to update user details
    '''
    email=StringField('Email',validators=[DataRequired(),Email()])
    username=StringField('Username',validators=[DataRequired()])
    picture=FileField('Update Profile Pic',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')