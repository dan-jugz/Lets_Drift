from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__='roles'
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(12))
    users=db.relationship('User',backref='role',lazy='dynamic')


class User(UserMixin,db.Model):
    __tablename__='users'
    
    id=db.Column(db.Integer,primary_key=True)
    profile_image=db.Column(db.String(64),default='default_profile.png')
    email=db.Column(db.String(64),unique=True,index=True)
    username=db.Column(db.String(64),unique=True)
    phone_number=db.Column(db.Integer)
    password_hash=db.Column(db.String(128))
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    #tying a user i.e an admin to a drift post
    posts=db.relationship('DriftPost',backref='author',lazy='dynamic')

    #tying a user to a comment
    comments=db.relationship('Comment',backref='commenter',lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def save_user(self):
        '''
        save instance for a user
        '''
        db.session.add(self)
        db.session.commit()  
        
    @classmethod
    def check_roles(cls,user_id,role_id):
        get_role=User.query.filter_by(id=user_id).filter_by(role_id=role_id).first()
        return get_role    
    
    def __repr__(self):
        return f'User {self.username}'    



class DriftPost(db.Model):
    __tablename__='driftposts'

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    date=db.Column(db.DateTime,default=datetime.utcnow)
    drift_image=db.Column(db.String(100),default='default_image.png')
    location=db.Column(db.String(100))
    location_about=db.Column(db.Text)
    price=db.Column(db.Integer)
        
    comments_post=db.relationship('Comment',backref='post_comments',lazy='dynamic')

    def save_post(self):
        '''
        Function that saves a drift post
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls):
        '''
        Function that fetches all drift post regardless of the admin
        '''

        posts=DriftPost.query.order_by(DriftPost.date.desc()).all()
        return posts

    @classmethod
    def get_admin_posts(cls,user,page):
        '''
        Function that fetches all drift post for a single admin
        '''
        posts_user=DriftPost.query.filter_by(author=user).order_by(DriftPost.date.desc()).paginate(page=page,per_page=5) 
        return posts_user   

    def __repr__(self):
        return f'PostID:{self.id}--Date{self.date}--Title{self.title}'    


class Comment(db.Model):
    __tablename__='comments'
    
    id=db.Column(db.Integer,primary_key=True)
    comment_content=db.Column(db.Text)
    post_id=db.Column(db.Integer,db.ForeignKey('driftposts.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_comment(self):
        '''
        Function that saves a new comment
        '''
        db.session.add(self)
        db.session.commit()

    
    @classmethod
    def get_comments(cls,post_id):
        '''
        Function that fetches a specific drift post comments
        '''
        
        comments=Comment.query.filter_by(post_id=post_id).all()
        return comments




 


        



        