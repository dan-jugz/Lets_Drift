from flask import render_template,redirect,url_for,abort,flash,request
from .. import db
from . import main
from flask_login import login_required,current_user
from ..models import User,DriftPost,Comment,Role
from .forms import UpdateProfileForm
from ..image_upload import add_profile_pic
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


@main.route('/user/<uname>')
def profile(uname):
    '''
    view function to see a single user profile
    '''
    user=User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template('profile/user_profile.html',user=user)   

    
@main.route('/user/<uname>/profile_update',methods=['GET','POST'])
@login_required
def profile_update(uname):
    '''
    view function to updtae a user profile
    '''
    user=User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    
    print(user)    

    
    form=UpdateProfileForm()

    if form.validate_on_submit():
        
        if form.picture.data:
            pic=add_profile_pic(form.picture.data,user.username)
            current_user.profile_image=pic
        user.username=form.username.data
        user.email=form.email.data

        db.session.add(user) 
        db.session.commit() 

        return redirect(url_for('main.profile',uname=user.username)) 

    elif request.method=='GET':
        #user is not submitting anything
        #set form field to the current users details
        form.username.data=current_user.username
        form.email.data=current_user.email
    
    #fetch the current profile image from the static folder and inject to the template    
    profile_image=url_for('static',filename='profile_pics/'+user.profile_image)  
    return render_template('profile/update_profile.html',form=form,profile_image=profile_image)  