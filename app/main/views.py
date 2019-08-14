from flask import render_template,redirect,url_for,abort,flash,request
from .. import db
from . import main
from flask_login import login_required,current_user
from ..models import User,DriftPost,Comment,Role
from .forms import UpdateProfileForm,DriftForm
from ..image_upload import add_profile_pic,add_drift_image
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
    drifts=DriftPost.get_posts()
   
    return render_template('home.html',title='Lets Drift',drifts=drifts)


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



@main.route('/create_drift',methods=['GET','POST'])
@login_required
def create_drift():
    '''
    View Function to create a drift
    '''
    form=DriftForm()
    if form.validate_on_submit():

        if form.drift_image.data:
            pic=add_drift_image(form.drift_image.data,form.location.data)
            drift_img=pic
            drift=DriftPost(location=form.location.data,date=form.date.data,location_about=form.location.data,price=form.price.data,drift_image=drift_img,user_id=current_user.id)  
            
            drift.save_post()

        return redirect(url_for('main.home'))
     
    return render_template('admin/create_drift.html',form=form)   

@main.route('/drift/<int:drift_id>')
def single_driftpost(drift_id):
    '''
    View function to view one drift post
    '''
    drift_post=DriftPost.query.get_or_404(drift_id)
    # comments=Comment.get_comments(blog_post_id)
    return render_template('driftpost.html',title=drift_post.title,drift_post=drift_post)

 