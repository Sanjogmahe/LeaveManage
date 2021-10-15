from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, request, Blueprint, before_render_template
from flaskblog.models import Post,Leaves,User
from flask_login import current_user, login_required
import logging

main = Blueprint('main', __name__)


@main.route("/")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    email = current_user.email

    leaves = Leaves.query.join(User, Leaves.user_id==User.id).filter(User.manager_byemail==email).order_by(Leaves.applied_datetime.desc()).paginate(page=page, per_page=5)
    return render_template('home.html',leaves=leaves)



@main.route("/home")
def dehome():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('welcome.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title='About')











