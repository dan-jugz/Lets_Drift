from flask import render_template,redirect,url_for,abort,flash,request
from .. import db
from . import main
from flask_login import login_required,current_user
from ..models import User,DriftPost,Comment,Role,CustomDrift
from .forms import UpdateProfileForm,DriftForm,CommentForm,CustomDriftForm
from ..image_upload import add_profile_pic,add_drift_image



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

@main.route('/home',methods=['GET','POST'])
def home():
    '''
    view root function that returns index page and its data
    '''

    form=CustomDriftForm()
    drifts=DriftPost.get_posts()

    if form.validate_on_submit():

        customdrift=CustomDrift(group=form.group.data,specifics=form.specifics.data,date=form.date.data,food=form.food.data,user_id=current_user.id)  
        flash('Custom Drift Created Successfully &#128515' ,'success')
        customdrift.save_drift()
        
  
 
    return render_template('home.html',title='Lets Drift',drifts=drifts,form=form)
    

@main.route('/user/<uname>')
def profile(uname):
    '''
    view function to see a single user profile
    '''
    #cyccle thru the custom drifts using pages..i.e if there are more than 5 posts we dont display all in tha single page
    page=request.args.get('page',1,type=int)

    user=User.query.filter_by(username=uname).first()
    customdrifts=CustomDrift.get_custom_drifts(page)

    if user is None:
        abort(404)

    return render_template('profile/user_profile.html',user=user,customdrifts=customdrifts)   

    
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

@main.route('/drift/<int:drift_id>',methods=['GET','POST'])
def single_driftpost(drift_id):
    '''
    View function to view one drift post
    '''
    drift_post=DriftPost.query.get_or_404(drift_id)
    comments=Comment.get_comments(drift_id)

    form=CommentForm()

    if form.validate_on_submit():
        comment_content=form.comment_content.data
        new_comment=Comment(comment_content=comment_content,post_id=drift_id,user_id=current_user.id)

        new_comment.save_comment()
        return redirect(url_for('main.single_driftpost',drift_id=drift_post.id))



    return render_template('driftpost.html',title=drift_post.location,drift_post=drift_post,comments=comments,form=form)


@main.route('/post/<int:drift_id>/update',methods=['GET','POST'])
@login_required
def update_drift(drift_id):
    '''
    View function to update a drift
    '''
    drift_post=DriftPost.query.get_or_404(drift_id)

    if drift_post.author !=current_user:
        #if the viewer is not the owner of the post
        #dont allow
        abort(403)
    
    form=DriftForm()
    if form.validate_on_submit():

        if form.drift_image.data:
            pic=add_drift_image(form.drift_image.data,form.location.data)
            drift_img=pic
            drift_post.drift_image=drift_img

        drift_post.location=form.location.data
        drift_post.price=form.price.data
        drift_post.date=form.date.data
        drift_post.location_about=form.location_about.data
            
        db.session.commit()

        flash('Drift Updated','success')
        return redirect(url_for('main.single_driftpost',drift_id=drift_post.id))

    elif request.method=='GET':

        #fill the form with the post details if user has not editted 
        form.location.data=drift_post.location
        form.price.data=drift_post.price
        form.date.data=drift_post.date
        form.location_about.data=drift_post.location_about
   

    return render_template('admin/create_drift.html',title="Update Drift",form=form)     


@main.route('/post/<int:drift_id>/delete',methods=['GET','POST'])
@login_required
def delete_drift(drift_id):
    '''
    View function to delete a drift post
    '''
    drift_post=DriftPost.query.get_or_404(drift_id)
        
    db.session.delete(drift_post)
    db.session.commit()
    flash('Drift Post Deleted Successfully &#128686; &#02713;','success')
    
    return redirect(url_for('main.home'))


@main.route('/drift/comment/new/<int:drift_id>',methods=['GET','POST'])
@login_required
def comment(drift_id):
    '''
    View function that returns a form to create a comment 
    ''' 
    drift_post=DriftPost.query.filter_by(id=drift_id).first()
    form=CommentForm()

    if form.validate_on_submit():
        comment_content=form.comment_content.data
        new_comment=Comment(comment_content=comment_content,post_id=drift_id,user_id=current_user.id)

        new_comment.save_comment()
        return redirect(url_for('main.single_driftpost',drift_id=drift_post.id))

    title=f'New {drift_post.location}Comment'

    return render_template('comment.html',title=title,form=form)   


@main.route('/<int:drift_id>/comment/<int:comment_id>/delete',methods=['GET','POST'])
@login_required
def delete_comment(drift_id,comment_id):
    '''
    View function to delete a comment
    '''
    comment=Comment.query.filter_by(id=comment_id).first()
    drift_post=DriftPost.query.get_or_404(drift_id)
    if drift_post.author != current_user:
        abort(403)
        
    db.session.delete(comment)
    db.session.commit()
    
    return redirect(url_for('main.single_driftpost',drift_id=drift_id))      

@main.route('/about')
def about():
    '''
    view root function that returns about page and its data
    '''
    return render_template('about_us.html',title='Lets Drift')

@main.route('/<uname>/<int:custom_drift_id>/delete',methods=['GET','POST'])
@login_required
def delete_custom_drift(uname,custom_drift_id):
    '''
    View function to delete a custom drift
    '''
    custom_drift=CustomDrift.query.get_or_404(custom_drift_id)
        
    custom_drift.delete_custom_drift(custom_drift_id)

    flash('Custom Drift Deleted Successfully','success')
    
    return redirect(url_for('main.profile',uname=uname))



 