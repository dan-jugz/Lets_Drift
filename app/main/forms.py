from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,IntegerField,SelectField
from wtforms.fields.html5 import DateField

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
    picture=FileField('Update Profile Pic',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField('Update')


class DriftForm(FlaskForm):
    '''
    Class to create a drif trip post
    '''

    location=StringField('Drift Location',validators=[DataRequired()])
    location_about=TextAreaField('About Drift',validators=[DataRequired()])
    date=DateField('When',format='%Y-%m-%d')
    price=IntegerField('Price',validators=[DataRequired()])
    drift_image=FileField('Upload Drift Image',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField('Submit Drift')



class CommentForm(FlaskForm):
    '''
    class to create a comment form
    '''
    comment_content=TextAreaField('Leave A Comment',validators=[DataRequired()])
    submit=SubmitField('Submit')


class CustomDriftForm(FlaskForm):
    '''
    Class to create a custom drift form 
    '''
    group=SelectField('Solo or Group',choices=[('',''),('solo','Solo'),('group','Group')])
    specifics=TextAreaField('What you wish to experience',validators=[DataRequired()])
    date=DateField('Day you wish to travel',format='%Y-%m-%d')
    food=SelectField('Should we provide food?',choices=[('Yes','Yes'),('No','No')])
    submit=SubmitField('Submit Custom Drift')    

