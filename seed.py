"""File to seed the habits database to run tests on functions"""
from datetime import datetime
import crud
from model import db, User, User_habit, Habit, Habit_log, Journal_log, Messages, connect_to_db





if __name__=='__main__':
    from server import app
    connect_to_db(app)
    os.system('dropdb habits')
    os.system('createdb habits')
    model.connect_to_db(server.app)
    model.db.create_all()