"""Create, Read, Update and Delete operations"""
from model import db, User, User_habit, Habit, Habit_log, Journal_log, Messages, connect_to_db

def create_user(fname, lname, email, password):
    """Create and return a new user"""
    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()
    return user

def create_habit(user, goal, name, type_of_execution, start_date, end_date):
    """Create and return a new habit"""
    user_habit = User_habit(user=user, goal=goal, name=name, type_of_execution=type_of_execution, start_date=start_date, end_date=end_date)

    db.session.add(user_habit)
    db.session.commit()

    return user_habit

# #def create_habit_log()

# def create_habit_log(user_habit, journal_log, date_of, progress):
#     habit_log = Habit_log(user_habit=user_habit, journal_log=journal_log, date_of=date_of, progress=progress) #should I add progress?

#     db.session.add(habit_log)
#     db.session.commit()



if __name__ == '__main__':
    from server import app
    connect_to_db(app)

