"""Models for 2do 2gether"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    email = db.Column(db.String(40) unique = True)
    password = db.Column(db.String(8)) #how do you make the requirement alphanumeric

    def __repr__(self):
        return f'<User fname={self.fname} lname={self.lname} email={self.email}>'

class User_habit(db.Model):
    """A user's habit description and other details"""

    __tablename__ = 'user_habit'

    user_habit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)      #turned yellow when I just had id
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.habit_id'))
    accountability_partner_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) 
    goal = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    name = db.Column(db.String)
    type_of_execution = db.Column(db.String)
    start_date = db.Column(db.Datetime)
    end_date = db.Column(db.Datetime)

    user = db.relationship('User', backref='user_habit')
    habit = db.relationship('Habit' backref='user_habit')


    def __repr__(self):
        return f'<User_habit user_id={self.user_id} name={self.name} goal={self.goal} start_date={self.start_date} end_date={self.end_date}

class Habit(db.Model):
    """the Habit list"""

    __tablename__ = 'habit'

    habit_id = db.Column(db.Interger, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f'<Habit habit_id={self.habit_id} name={self.name}>'

class Habit_log(db.Model):
    "A daily habit-log for user"

    __tablename__ = 'habit-log'

    

