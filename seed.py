"""File to seed the habits database to run tests on functions"""
from datetime import datetime
import crud
from model import db, User, User_habit, Habit, Habit_log, Journal_log, Messages, connect_to_db


user_1 = User(fname="Andrew" lanme='Gerber', email='andrew.gerber@gmail.com', password='and123')
user_2 = User(fname="Lana" lanme='Landor', email='lana.landor@gmail.com', password='lan123')
user_3 = User(fname="Wana" lanme='Sour', email='wana.sour@gmail.com', password='wan123')

habit_1 = Habit(name='yoga')
habit_2 = Habit(name='running')
habit_3 = Habit(name='meditation')
habit_4 = Habit(name='reading')

journal_1 = Journal_log(journal_entry="Completing the task today was an achievement")
journal_2 = Journal_log(journal_entry="Tough run today")
journal_3 = Journal_log(journal_entry="Forgot to meditate today, will add 10 extra mins tom")
journal_4 = Journal_log(journal_entry="Breathing has gotten better")




if __name__=='__main__':
    from server import app
    connect_to_db(app)
    os.system('dropdb habits')
    os.system('createdb habits')
    connect_to_db(server.app)
    db.create_all()