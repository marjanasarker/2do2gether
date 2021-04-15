from flask import Flask, request, flash, session, redirect, render_template
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    
    return render_template('homepage.html')

@app.route('/create_account')
def show_newaccount_form(): 


    return render_template('create_account.html')


@app.route('/create_account', methods=['POST'])
def register_user():
    """Creating new user"""

    first_name = request.form.get('fname')
    last_name = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    #print(first_name, last_name, email, password)
    user = crud.get_user_by_email(email)
    

    if user:
        flash('Cannot create an account, email on file. Try again.')
    else:
        new_user = crud.create_user(first_name, last_name, email, password)
        flash('Account created! Please log in.') #where should I redirect them 

    return redirect('/login') #redirect to a profile page 


    #return render_template('login.html')
@app.route('/login')
def show_login():

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def regular_user_login():

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    

    if user and user.password == password:
        session['user_id'] = user.user_id
        num_habits=crud.get_number_of_habits(session['user_id'])
        print(session)
        if num_habits==3:
            return redirect('/habit_display')
        else:
            return redirect('/habit')
    else:
        flash('Password or email address entered incorrectly, try again.')

    
    return redirect('/login')  #change this

@app.route('/habit')
def show_habit():
    #max_habits = 3
    #if session['user_id']:
    #habits = 
        
    return render_template('habit.html')
    #else:
        #return redirect('/login')

     
@app.route('/habit', methods=['POST'])
def create_new_habit():
    """Setting up new habits"""
    
    goal = request.form.get('goal')
    habit_name = request.form.get('habit_name')
    type_goal = request.form.get('type_goal')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    num_habits=crud.get_number_of_habits(session['user_id'])
    user_habits = crud.get_habits_by_user(session['user_id'])
    print(user_habits)
    if num_habits<3:
        new_habit = crud.create_user_habit(session['user_id'],goal,habit_name,type_goal,start_date,end_date)
    else:
        flash('Reached limit for number of habits')
        return redirect('/habit_display')

    return redirect('/habit') 

@app.route('/habit_display')
def display_habits():
    "Display the habits user is set out to complete"
    user_habits = crud.get_habits_by_user(session['user_id'])
    print(user_habits[2])
    return render_template("habit_display.html", user_habits=user_habits)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)