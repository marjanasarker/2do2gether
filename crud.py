"""Create, Read, Update and Delete operations"""
from model import db, User, User_habit, Habit, Habit_log, Journal_log, Messages, connect_to_db
from sqlalchemy.sql import func, cast
import sqlalchemy

def create_user(fname, lname, email, password):
    """Create and return a new user"""
    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()
    
    return user

def create_user_habit(user_id, goal, name, type_of_execution, start_date, end_date):
    """Create and return a new habit set up"""
    user_habit = User_habit(user_id=user_id, goal=goal, name=name, 
                           type_of_execution=type_of_execution, 
                           start_date=start_date, end_date=end_date)

    db.session.add(user_habit)
    db.session.commit()

    return user_habit

def create_habit(habit_id, name):
    """Create and return the user's habits for the month"""
    habit = Habit(habit_id=habit_id, name=name)

    db.session.add(habit)
    db.session.commit()

def create_habit_log(user_habit_id, journal_log, date_of, log_in_time, progress):
    """Create and return a new log for habit completion"""
    habit_log = Habit_log(user_habit_id=user_habit_id, journal_log=journal_log, 
                           date_of=date_of, log_in_time=log_in_time, progress=progress) #should I add progress?

    db.session.add(habit_log)
    db.session.commit()

    return habit_log

def create_journal_log(journal_entry):
    """Create and return a new journal entry"""

    journal_log = Journal_log(journal_entry=journal_entry)

    db.session.add(journal_log)
    db.session.commit()

    return journal_log

def create_messages(user_habit_id, sender_id, receiver_id, message_date, message):
    """Create and return a new message"""

    messages = Messages(user_habit_id=user_habit_id, sender_id=sender_id, 
                       receiver_id=receiver_id, message_date=message_date,
                       message=message)

    db.session.add(messages)
    db.session.commit()

    return messages

def get_user_by_email(email):
    """Returns user with email"""

    return User.query.filter(User.email == email).first()

def get_habits_by_user(user_id):
    """Return habits by user"""

    return User_habit.query.filter_by(user_id=user_id).all() 

def get_number_of_habits(user_id):
    """Returns number of habits user set up"""

    return User_habit.query.filter_by(user_id=user_id).count()

def get_user_habit_progress_sum(user_habit_id):
    """Return progress metric for user based on logged hours vs. user goal"""
    
    sum_logins= db.session.query(func.sum(cast(Habit_log.log_in_time, sqlalchemy.Float)).filter(Habit_log.user_habit_id == user_habit_id)).scalar()
    return sum_logins

def get_user_habit_log(user_habit_id):
    "Return habit_log for user's particular habit"

    return Habit_log.query.filter(Habit_log.user_habit_id == user_habit_id).all()

def get_user_habit_goal(user_habit_id):
    "Return user habit details"

    habit_details= User_habit.query.filter(User_habit.user_habit_id==user_habit_id).one()
    habit_goal = habit_details.goal
    #habit_goal = habit_details.query.filter(User_habit.goal).all()
    return habit_goal

def get_user_habit_name(user_habit_id):
    "Return user habit name"
    habit_details= User_habit.query.filter(User_habit.user_habit_id==user_habit_id).one()
    habit_name = habit_details.name
    return habit_name

if __name__ == '__main__':
    from server import app
    connect_to_db(app)