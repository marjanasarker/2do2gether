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

    user_habit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)      
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
    """A daily habit-log for user"""

    __tablename__ = 'habit-log'

    habit_log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_habit_id = db.Column(db.Integer, db.ForeignKey('user_habit.user_habit_id'))
    journal_id = db.Column(db.Integer, db.ForeignKey('journal_log.journal_id'))
    date_of = db.Column(db.Datetime)
    progress = db.Column(db.Numeric)

    user_habit = db.relationship('User_habit', backref='habit_log')
    journal_log = db.relationship('Journal_log', backref='habit_log')

    def __repr__(self):
        return f'<Habit_log habit_log_id={self.habit_log_id} date_of={self.date_of} progress={self.progress}>

class Journal_log(db.Model):
    """Journal entries"""

    __tablename__ = 'journal-entries'

    journal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    journal_entry = db.Column(db.Text)

    def __repr__(self):
        return f'<Journal_log journal_id={self.journal_id} journal_entry={self.journal_entry}>

class Messages(db.Model):
    """Accountability messages and replies"""

    __tablename__ = "messages"

    messages_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_habit_id = db.Column(db.Integer, db.ForeignKey('user_habit.user_habit_id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    timestamp = db.Column(db.Datetime)
    message = db.Column(db.Text)

    user_habit = db.relationship('User_habit', backref='messages')
    user = db.relationship('User', backref='messages')
    



def connect_to_db(flask_app, db_uri='postgresql:///habits', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)