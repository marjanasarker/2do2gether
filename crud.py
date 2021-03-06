"""Create, Read, Update and Delete operations"""
from model import db, User, User_habit, Habit, Habit_log, Journal_log, Messages, connect_to_db
from sqlalchemy.sql import func, cast
from datetime import datetime, date
import sqlalchemy

def create_user(fname, lname, email, password):
    """Create and return a new user"""
    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()
    
    return user

def create_user_habit(user_id, habit_id, goal, name, type_of_execution, start_date, end_date):
    """Create and return a new habit set up"""
    user_habit = User_habit(user_id=user_id, habit_id=habit_id, goal=goal, name=name, 
                           type_of_execution=type_of_execution, 
                           start_date=start_date, end_date=end_date)

    db.session.add(user_habit)
    db.session.commit()

    return user_habit

def create_habit(name):
    """Create and return the user's habits for the month"""
    habit = Habit(name=name)

    db.session.add(habit)
    db.session.commit()

def create_habit_log(user_habit_id, journal_id, date_of, log_in_time):
    """Create and return a new log for habit completion"""
    habit_log = Habit_log(user_habit_id=user_habit_id, journal_id=journal_id, 
                           date_of=date_of, log_in_time=log_in_time) #should I add progress?

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

def get_user_by_id(user_id):
    """Returns user's name with user id"""

    user_details = User.query.filter(User.user_id == user_id).first()
    return user_details.fname

def get_habits():
    """Returns all habits from database in a list"""

    habits_in_db = db.session.query(Habit.name).all()
    habits_in_list = [habit for (habit,) in habits_in_db]
    return habits_in_list

def get_type_goal(user_habit_id):

    user_habit_details = User_habit.query.filter_by(user_habit_id=user_habit_id).first()
    return user_habit_details.type_of_execution

def get_habit_id(habit_name):
    """Returns habit id by taking habit_name as argument"""

    user_habit = Habit.query.filter(Habit.name == habit_name).first()
    return user_habit.habit_id

def get_user_name_same_habit(habit_name):
    """Returns list of user full name with same habits"""

    same_habit_user = User_habit.query.filter_by(name=habit_name).all()
    same_habit_users_id = []
    
    same_habit_users_name_email = []
    for users in same_habit_user:
        if users.accountability_partner_id == None:
            same_habit_users_id.append(users.user_id)

    
    for user in same_habit_users_id:
        user_details = User.query.filter_by(user_id=user).one()
        fname=user_details.fname
        email = user_details.email
        name_email = (fname, email)
        same_habit_users_name_email.append(name_email)
        
            
    return(same_habit_users_name_email)

def get_user_habit_id_habitname_userid(habit_name, user_id):
    """Returns user_habit_id with habit_name and user_id"""

    same_habit_user = User_habit.query.filter_by(name=habit_name).all()
    
    for user in same_habit_user:
        if user.user_id == user_id:
            return user.user_habit_id 

         
def get_sender_id(user_habit_id):
    """Return receiver id using user_habit_id from the messages table"""

    one_message = Messages.query.filter_by(user_habit_id=user_habit_id).first()
    return one_message.sender_id

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
    """Return habit_log for user's particular habit"""

    return Habit_log.query.filter(Habit_log.user_habit_id == user_habit_id).all()

def get_user_journal_entries(journal_id):
    """Return journal entries using journal id"""

    journal_log =  Journal_log.query.filter_by(journal_id=journal_id).one()
    return journal_log.journal_entry

def get_journal_entries_by_user_habit(user_habit_id):
    """Return journal entries based on journal ids from user's habit log"""

    habit_log = get_user_habit_log(user_habit_id)
    journal_ids = []
    journal_entries=[]
    for user in habit_log:
        journal_ids.append(user.journal_id)
    for ids in journal_ids:
        journal_entries.append(get_user_journal_entries(ids))

    return journal_entries

def get_user_habit_log_dates(user_habit_id):
    """Return dates of habit_log"""

    list_habit_log = Habit_log.query.filter(Habit_log.user_habit_id == user_habit_id).all()
    date_of_habit_log = []
    for log in list_habit_log:
        date = log.date_of.strftime('%Y-%m-%d')
        date_of_habit_log.append(date)
    return date_of_habit_log

def get_user_habit_goal(user_habit_id):
    """Return user habit details"""

    habit_details= User_habit.query.filter(User_habit.user_habit_id==user_habit_id).one()
    habit_goal = habit_details.goal
    return habit_goal

def get_user_habit_end_date(user_habit_id):
    """Return when the 30 days for habit ends"""
    
    habit_details = User_habit.query.filter(User_habit.user_habit_id==user_habit_id).one()
    end_date = habit_details.end_date
    return end_date


def get_user_habit_name(user_habit_id):
    """Return user habit name"""

    habit_details= User_habit.query.filter(User_habit.user_habit_id==user_habit_id).one()
    habit_name = habit_details.name
    return habit_name

def get_messages_user_habit(user_habit_id):
    """Return messages by user_habit_id"""

    message_details= Messages.query.filter_by(user_habit_id=user_habit_id).all()
    date_message=[]
    
    for user in message_details:
        date = user.message_date.strftime('%Y-%m-%d')
        message = user.message
        receiver_name = get_user_by_id(user.receiver_id)
        date_and_message = (date, message, receiver_name)
        date_message.append(date_and_message)
    return date_message  

def add_accountability_partner_id(user_habit_id, accountability_partner_id):
    """Upadates user_habit_id with accountability_partner_id once partner selected for habit"""

    user_habits = User_habit.query.filter_by(user_habit_id=user_habit_id).first()
    user_habits.accountability_partner_id = accountability_partner_id


def get_user_habit_ids_habit_name(user_habit_name):
    """Storing the user_habit_ids for a particular habit in a list"""

    user_habit_ids = User_habit.query.filter_by(name=user_habit_name).all()
    user_habit_id = []
    for user in user_habit_ids:
        user_habit_id.append(user.user_habit_id)
        
    return user_habit_id

def check_if_selected_accountability_partner(user_habit_name, user_id):
    """Return the user id that chose a person as their accountability partner"""
    check_users = get_user_habit_ids_habit_name(user_habit_name)
    
    for user_habit_id in check_users:
        habit_details = User_habit.query.filter_by(user_habit_id=user_habit_id).first()
        if habit_details.accountability_partner_id==user_id:

            return habit_details.user_id

  
        

if __name__ == '__main__':
    from server import app
    connect_to_db(app)