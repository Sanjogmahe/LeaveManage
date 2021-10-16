from flask_login import current_user

from flaskblog import create_app#flaskbolg is initilse ,which get loded and interpreted
from datetime import datetime, timedelta
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flaskblog.models import Leaves, User
from flaskblog import db


app = create_app()#storing all the function of create _app ,it containes all the info like bluepront and all the srtucture of the web app
# currDat=datetime.now()+timedelta(seconds=30)

# nowtime=datetime.now()
# nextyr=int(nowtime.year)+1
nextyrdate = datetime(int((datetime.now()).year)+1, 1, 1)
def print_date_time():
    with app.app_context():# when we have to use the db or any anyothe function  outside the view
        # date_1 =
        # print("date1",date_1)
        # date_2 = datetime.now()
        # date_format_str = '%d/%m/%Y %H:%M:%S.%f'
        start = datetime.now() - timedelta(hours=24) # datetime.strptime(date_1, date_format_str)

        # currDat = datetime.now
        # print("print :",x)

        # yearend=datetime.now() - timedelta(year=1)
        # end = date_2
        # Get interval between two timstamps as timedelta object
        # diff = end - start#00/00/000 24:00:00
        # print(diff)
        # Get interval between two timstamps in hours
        # diff_in_hours = diff.total_seconds() / 3600
        # print('Difference between two datetimes in hours:')
        # print(diff_in_hours)

        #print(c)
        l = Leaves.query.filter(Leaves.applied_datetime<=start,Leaves.approved.in_(['No','pending'])).all()#got the date greater then 24 hours
        for i in l:
            print('old :',i)
            i.approved='approved'
            db.session.commit()
        else :
            print("No Pending approval")




def leave_conv_money():
    with app.app_context():
        user=User.query.all()
        leave=Leaves.query.all()
        for i in user:
            print('username:',i.username,'applied leaves:',i.total_applied_leaves)
        # for j in leave:
        #     pendleave=j.pending_leaves
        #     userid=j.id
        c=Leaves.query.group_by(id).all()
        for i in c:
            print('tries:'+i)
            # print("pending leaves are "+ str(pendleave))
            # if pendleave==0:
            #     j.pending_leaves=1



        user_withmoreLeaves=User.query.filter(User.total_applied_leaves>=1).all()
        user_withmoreLeaves=User.query.filter(User.total_applied_leaves>=1).all()
        for usr in user_withmoreLeaves:
            print('userwithmoreleaves:',usr.total_applied_leaves)

scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval" ,hours=2)

scheduler.add_job(func=leave_conv_money, trigger="interval",next_run_time=nextyrdate,hours=8766)# manage the hours pending
# scheduler.add_job(func=leave_conv_money, trigger="interval",minutes=1)# manage the hours pending
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

print(__name__)

if __name__ == '__main__':# on app.py call app.run is called# main file
    # import test
    app.run(host='0.0.0.0', port=5000, debug=True)


