from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,DateField,IntegerField

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


class DriftForm(FlaskForm):
    '''
    Class to create a drif trip post
    '''

    location=StringField('Drift Location',validators=[DataRequired()])
    location_about=TextAreaField('About Drift',validators=[DataRequired()])
    date=DateField('When',validators=[DataRequired()])
    price=IntegerField('Price',validators=[DataRequired()])
    drift_image=FileField('Upload Drift Image',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField('Submit Drift')


