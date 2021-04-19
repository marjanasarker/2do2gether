from flask import Flask, request, flash, session, redirect, render_template
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Homepage of app"""
    return render_template('homepage.html')

@app.route('/create_account')
def show_newaccount_form(): 
    """Renders page where user can create new account"""
    return render_template('create_account.html')


@app.route('/create_account', methods=['POST'])
def register_user():
    """Creating new user"""

    first_name = request.form.get('fname')
    last_name = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

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
    """Renders page where user can login"""

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def regular_user_login():
    """Check if user exists, and redirect to create new habit if they have less than 3 habits setup"""

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

    
    return redirect('/login') 

@app.route('/habit')
def show_habit():
    """Renders page where user can set up habits"""
    
    return render_template('habit.html')
    

     
@app.route('/habit', methods=['POST'])
def create_new_habit():
    """Setting up new habits"""
    
    goal = request.form.get('goal')
    habit_name = request.form.get('habit_name').lower()
    type_goal = request.form.get('type_goal')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    num_habits=crud.get_number_of_habits(session['user_id'])
    user_habits = crud.get_habits_by_user(session['user_id'])

    if habit_name in crud.get_habits():
        habit_id = crud.get_habit_id(habit_name)
    else:
        crud.create_habit(habit_name)
        habit_id = crud.get_habit_id(habit_name)
    #print(user_habits)

    if num_habits<3:
        new_habit = crud.create_user_habit(session['user_id'],habit_id,goal,habit_name,type_goal,start_date,end_date)
    else:
        flash('Reached limit for number of habits')
        return redirect('/habit_display')

    return redirect('/habit') 

@app.route('/habit_display')
def display_habits():
    """Display the habits user is set out to complete"""
    
    user_habits = crud.get_habits_by_user(session['user_id'])
    #print(user_habits)
        
    return render_template("habit_display.html", user_habits=user_habits)

@app.route('/habit_log_display/<habit_id>')
def display_habit_log(habit_id):
    """Renders habit tracking page and shows progress made so far"""
    
    habit_id = habit_id
    user_habit_name = crud.get_user_habit_name(habit_id)
    sum_logins = crud.get_user_habit_progress_sum(habit_id)
    #print(sum_logins)
    goal = crud.get_user_habit_goal(habit_id)

    if sum_logins:
        progress = float(sum_logins/goal)*100
    else:
        progress = 0

    return render_template("habit_log_display.html", user_habit_name=user_habit_name, habit_id=habit_id, progress=progress)

@app.route('/habit_log_display/<habit_id>', methods=['POST'])
def display_track_habit_log(habit_id):
    """Function to create new habit_log for user's habit"""
    
    habit_id = habit_id
    log_in_time = request.form.get('log_in_time')
    date_of = request.form.get('date_of') 
    journal_entry=request.form.get('journal_entry')
    journal_entry_today = crud.create_journal_log(journal_entry)
    new_habit_log = crud.create_habit_log(habit_id, journal_entry_today.journal_id, date_of, log_in_time)
    flash('New habit login details recorded, would you like to login another habit?')
    
    return redirect('/habit_display')
    
@app.route('/logout')
def logout():
    """User must be logged in to use logout"""

    del session['user_id']
    flash("You have been logged out")

    return redirect('/login')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)