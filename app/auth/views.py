from flask import render_template,redirect,url_for,request,flash
from . import auth
from ..models import User
from .forms import RegistrationForm,LoginForm
from .. import db
from flask_login import login_user,login_required,logout_user


@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    

    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            
            login_user(user,form.remember.data)

            return redirect(request.args.get('next') or url_for('main.home'))

        flash('Invalid Username or Password')
    
    title='Drift Login'
    return render_template('auth/login.html',form=form,title=title) 

    
@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,phone_number=form.phone_number.data,password=form.password.data,role_id=2)

        user.save_user()
        flash('Thanks for registering')
        return redirect(url_for('auth.login'))

    title='New Drift Account'
    return render_template('auth/register.html',form=form,title=title)    


    
@auth.route('/create_admin/<uname>',methods=['GET','POST'])
def create_admin():
    form=RegistrationForm()
    creator=User.query.filter_by(username=uname).first()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,phone_number=form.phone_number.data,password=form.password.data,role_id=1)

        user.save_user()
        flash('Admin Created','success')
        return redirect(url_for('main.profile',uname=creator))

    title='New Drift Account'
    return render_template('auth/register_admin.html',form=form,title=title) 

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))    

