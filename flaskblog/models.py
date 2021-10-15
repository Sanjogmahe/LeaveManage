from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    registration_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    manager_byemail = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    leaves = db.relationship('Leaves', backref='author', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    testcaseid=db.Column(db.String(20), unique=True)
    total_applied_leaves = db.Column(db.Integer, default=0)
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}','{self.registration_time}','{self.manager_byemail}','{self.posts}','{self.roles}','{self.testcaseid}','{self.total_applied_leaves}')"


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='roles')

    def __repr__(self):
        return f"Role('{self.name}','{self.id}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Leaves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    startdate = db.Column(db.String(10), nullable=False)
    applied_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    enddate = db.Column(db.String(10), nullable=False)
    applied_leaves = db.Column(db.Integer, nullable=False)
    leave_type = db.Column(db.String(100), nullable=False)
    approved = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pending_leaves=db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Leaves('{self.startdate}', '{self.applied_datetime}','{self.enddate}','{self.applied_leaves}','{self.leave_type}','{self.approved}','{self.pending_leaves}')"





