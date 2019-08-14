from flask import render_template,redirect,url_for,abort,flash,request
from .. import db
from . import main
from flask_login import login_required,current_user
from ..models import User,DriftPost,Comment,Role
# from .forms import UpdateProfileForm,CommentForm,PostForm
# from ..picture_handler import add_profile_pic
# from ..request import get_quotes


#views
@main.route('/')
def index():
    '''
    view root function that returns index page and its data
    '''
    # posts=BlogPost.get_posts()
    # qquote=get_quotes()
    # quote=reloadapi()
    # quote=get_quotes()
    return render_template('index.html',title='Lets Drift')

@main.route('/home')
def home():
    '''
    view root function that returns index page and its data
    '''
    # posts=BlogPost.get_posts()
    # qquote=get_quotes()
    # quote=reloadapi()
    # quote=get_quotes()
    return render_template('home.html',title='Lets Drift')


