import requests
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, session)
from flask_login import current_user, login_required
from sqlalchemy import desc
import time
import secrets
from datetime import datetime , timedelta
from flaskblog import db
from flaskblog.models import Post,  User, Leaves
# Docs, Phone,RDetails
from flaskblog.leave.forms import PostForm,UploadDoc,LeaveappliedDate
from flaskblog.users.utils import save_document
import pytz
import time
#NewRequirement,AppOver,ContactMat,TestRun,CombinedForm


TZ = []
for x in pytz.common_timezones:
    y = pytz.timezone(x)
    TZ.append(y.zone)

posts = Blueprint('leave', __name__)







@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@posts.route("/leave", methods=['GET','POST'])
@login_required
def leave_summary():
    l = Leaves.query.filter(Leaves.applied_datetime < datetime.now()).all()
    # for i in l:
    #     print(i)
    form = LeaveappliedDate()
    # joiningdate = "09-01-2021"
    joiningDate= current_user.registration_time
    # d1 = datetime(2021, 1, 1)
    now = datetime.now()
    currentDate = datetime(now.year, now.month, now.day)
    Total_months = (currentDate.year - joiningDate.year) * 12 + currentDate.month - joiningDate.month
    # print(Total_months)
    Default_leaves = 2
    if Total_months > 1:
        Default_leaves = Default_leaves + (Total_months - 1) * 2
    leaves.applied_leaves=Default_leaves
    db.session.commit()
    # print(Default_leaves)
    # appliedleaves = 5
    previously_appliedleaves = Leaves.query.filter_by(user_id=current_user.id).all()
    sum_previously_appliedleaves = 0
    for i in previously_appliedleaves:
        sum_previously_appliedleaves = sum_previously_appliedleaves + i.applied_leaves
    q=User.query.filter_by(email=current_user.email).first()



    # print('Total Applied :' ,q.total_applied_leaves)
    # for i in q:
    #     print(' q for current user ',i)
    q.total_applied_leaves=sum_previously_appliedleaves
    # db.session.add(User)
    db.session.commit()
    # print("Applied Leaves,", sum_previously_appliedleaves)
    # print(previously_appliedleaves)
    if sum_previously_appliedleaves > 0:
        Default_leaves = Default_leaves - sum_previously_appliedleaves

    # print("Before Input Calculation", Default_leaves)
    allstartleaveslist=[]
    if form.validate_on_submit():
        applied_startdate = form.date.data
        allstartleaves=Leaves.query.filter_by(user_id=current_user.id).all()
        for i in allstartleaves:
            allstartleaveslist.append(i.startdate)
        if applied_startdate in allstartleaveslist :
            flash('Leave on that date exists','danger')
            return redirect(url_for('posts.leave_summary'))
        applied_startdate_datetime = datetime(int(applied_startdate.split('-')[2]), int(applied_startdate.split('-')[1]),
                                              int(applied_startdate.split('-')[0]))
        applied_enddate = form.enddate.data
        applied_enddate_datetime = datetime(int(applied_enddate.split('-')[2]), int(applied_enddate.split('-')[1]),
                                            int(applied_enddate.split('-')[0]))
        appliedleaves=0.0
        if(form.leavetype.data == "Half Day Leave"):
            appliedleaves = ((applied_enddate_datetime - applied_startdate_datetime).days+1)/2
        else:
            appliedleaves = (applied_enddate_datetime - applied_startdate_datetime).days+1

        # print('leaves applied',appliedleaves)
        if Default_leaves < appliedleaves:
            flash('Your leaves are exausted!', 'danger')
            # if appliedleaves > 0:
            #     Default_leaves = Default_leaves - appliedleaves
        else:# print("After Calculation", Default_leaves)

            pending_leaves=Default_leaves-appliedleaves

            leave = Leaves(startdate=form.date.data, enddate=form.enddate.data, author=current_user,applied_leaves=appliedleaves,leave_type=form.leavetype.data,approved='pending',pending_leaves=pending_leaves)

            # leavetype = form.leavetype.data

            db.session.add(leave)
            db.session.commit()
            flash('Your leaves has been created!', 'success')
        return redirect(url_for('leave.leave_summary'))
    leavespending=Leaves.query.filter_by(user_id=current_user.id).all()
    return render_template('leave.html',tile='LeaveSummary',form=form, y=Default_leaves,leaveall=previously_appliedleaves, leavespending=leavespending)


@posts.route("/leave/<int:leave_id>")
def leaves(leave_id):
    leave = Leaves.query.get_or_404(leave_id)
    return render_template('post.html', title="post.title", leave=leave)


@posts.route("/leave/<int:leave_id>/update", methods=['GET', 'POST'])
@login_required
def update_leave(leave_id):
    leave = Leaves.query.get_or_404(leave_id)
    # leave = Leaves.query.get
    # if post.author != current_user:
    #     abort(403)
    form = PostForm()
    # if form.validate_on_submit():
        # leave.title = form.title.data
        # post.content = form.content.data
    leave.approved = "approved"
    db.session.commit()
    flash('Leaves has been updated!', 'success')
    return redirect(url_for('posts.leaves', leave_id=leave.id))
    # elif request.method == 'GET':
    #     form.title.data = post.title
    #     form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:leave_id>/delete", methods=['POST'])
@login_required
def reject_leave(leave_id):
    leave = Leaves.query.get_or_404(leave_id)
    # if post.author != current_user:
    #     abort(403)
    leave.approved = "rejected"
    leave.applied_leaves = 0
    # db.session.delete(post)
    db.session.commit()
    flash('Leaves has been rejected!', 'success')
    return redirect(url_for('main.home'))

