"""Models for 2do 2gether"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    email = db.Column(db.String(40), unique = True)
    password = db.Column(db.String(8)) #how do you make the requirement alphanumeric
    
    #habits = db.relationship('User_habit')

    def __repr__(self):
        return f'<User fname={self.fname} lname={self.lname} email={self.email} password={self.password}>'

class User_habit(db.Model):
    """A user's habit description and other details"""

    __tablename__ = 'user_habit'

    user_habit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)      
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.habit_id'))
    accountability_partner_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) 
    goal = db.Column(db.Integer)
    completed = db.Column(db.Boolean) #default=False
    name = db.Column(db.String)
    type_of_execution = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    user = db.relationship('User', foreign_keys=[user_id])
    accountability_user = db.relationship('User', foreign_keys=[accountability_partner_id])
    habits = db.relationship('Habit', backref='user_habit')


    def __repr__(self):
        return f'<User_habit user_id={self.user_id} name={self.name} goal={self.goal} start_date={self.start_date} end_date={self.end_date}>'

class Habit(db.Model):
    """the Habit list"""

    __tablename__ = 'habit'

    habit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f'<Habit habit_id={self.habit_id} name={self.name}>'

class Habit_log(db.Model):
    """A daily habit-log for user"""

    __tablename__ = 'habit_log'

    habit_log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_habit_id = db.Column(db.Integer, db.ForeignKey('user_habit.user_habit_id'))
    journal_id = db.Column(db.Integer, db.ForeignKey('journal_log.journal_id'))
    date_of = db.Column(db.DateTime)
    log_in_time = db.Column(db.Numeric) #how much time did the user put in day of
    #progress = db.Column(db.Numeric) #what the user starts with default

    user_habit = db.relationship('User_habit', backref='habit_log')
    journal_log = db.relationship('Journal_log', backref='habit_log')

    def __repr__(self):
        return f'<Habit_log habit_log_id={self.habit_log_id} user_habit_id={self.user_habit_id} journal_id={self.journal_id} log_in_time={self.log_in_time} date_of={self.date_of}>'

class Journal_log(db.Model):
    """Journal entries"""

    __tablename__ = 'journal_log'

    journal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    journal_entry = db.Column(db.Text)

    def __repr__(self):
        return f'<Journal_log journal_id={self.journal_id} journal_entry={self.journal_entry}>'

class Messages(db.Model):
    """Accountability messages and replies"""

    __tablename__ = "messages"

    messages_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_habit_id = db.Column(db.Integer, db.ForeignKey('user_habit.user_habit_id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    message_date = db.Column(db.DateTime)
    message = db.Column(db.Text)

    sender = db.relationship('User', foreign_keys=[sender_id]) #sender is an attribute to Messages
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    user_habit = db.relationship('User_habit', backref='messages')
    
    
    def __repr__(self):
        return f'<Messages messages_id={self.messages_id} user_habit_id={self.user_habit_id} sender_id={self.sender_id} receiver_id={self.receiver_id} message_date={self.message_date} message={self.message}>'

def example_data():
    """Sample data to run tests with"""

    User.query.delete()
    User_habit.query.delete()

    #sample user_habit data
    ua = User_habit(user_id = 1, name="jogging")
    uj = User_habit(user_id = 2, name="yoga")
    ur = User_habit(user_id = 3, name="jogging")
    un = User_habit(user_id = 4, name="yoga")
    uo = User_habit(user_id = 1, name="yoga")
    uk = User_habit(user_id = 1, name="meditation")

    #sample users
    amanda = User(fname="Amanda", lname="Smith", email="amanda.smith@gmail.com", password="ama123")
    joel = User(fname="Joel", lname="Don",email="joel.don@gmail.com", password="joe123")
    raquel = User(fname="Raquel", lname="Junior", email="raquel.junior@gmail.com", password="raq123")
    nondita = User(fname='Nondita', lname="Sarkar", email="nondita.sarkar@gmail.com", password="non123")

    db.session.add_all([ua,uj,ur,un,uo,uk,amanda,joel,raquel,nondita])
    db.session.commit()


def connect_to_db(flask_app, db_uri='postgresql:///habits', echo=False):
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