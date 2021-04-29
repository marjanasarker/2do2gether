from flask import Flask, request, flash, session, redirect, render_template, jsonify
from model import connect_to_db
from datetime import datetime, date, timedelta 
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.jinja_env.filters['zip'] = zip

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
    
    num_habits=crud.get_number_of_habits(session['user_id'])
    
    
    if num_habits:
        num_habits=num_habits
    else:
        num_habits=0
    return render_template('habit.html', num_habits=num_habits)
    

     
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
    num_habits=crud.get_number_of_habits(session['user_id'])
    user_name = crud.get_user_by_id(session['user_id'])
    
    if num_habits<3:
        num_habit=3-num_habits
    else:
        num_habit=0
      
    return render_template("habit_display.html", user_habits=user_habits, num_habit=num_habit, user_name=user_name)

@app.route('/habit_log_display/<user_habit_id>')
def display_habit_log(user_habit_id):
    """Renders habit logging page and also shows progress made so far"""
    
    user_habit_id = user_habit_id
    user_habit_name = crud.get_user_habit_name(user_habit_id)

    sum_logins = crud.get_user_habit_progress_sum(user_habit_id)
    goal = crud.get_user_habit_goal(user_habit_id)

    date_of = date.today()
    
    if sum_logins:
        progress = float(sum_logins/goal)*100
    else:
        progress = 0

    return render_template("habit_log_display.html", user_habit_name=user_habit_name, user_habit_id=user_habit_id, progress=progress, date_of=date_of)

@app.route('/habit_log_display/<user_habit_id>', methods=['POST'])
def display_track_habit_log(user_habit_id):
    """Function to create new habit_log for user's habit"""
    
    user_habit_id = user_habit_id
    print(user_habit_id)
    #user_habit_name = crud.get_user_habit_name(user_habit_id)
    log_in_time = request.form.get('log_in_time')
    journal_entry=request.form.get('journal_entry')

    date_of = date.today()
    time_added = timedelta(days=7)
    date_logs = crud.get_user_habit_log_dates(user_habit_id)
    
    
    if str(date_of) not in date_logs:
        journal_entry_today = crud.create_journal_log(journal_entry)
        new_habit_log = crud.create_habit_log(user_habit_id, journal_entry_today.journal_id, date_of, log_in_time)
        flash('New habit login details recorded, would you like to login another habit?')
    else:
        flash('Log not recorded')
        flash('Log for this habit already created for today')
        return display_habit_log(user_habit_id)

    
    
    return redirect('/habit_display')

@app.route('/habit_progress/<user_habit_id>') 
def user_habit_progress(user_habit_id):
    """Renders habit tracking page and shows progress made so far and number of days left to meet goal"""
    
    user_habit_id = user_habit_id
    user_habit_name = crud.get_user_habit_name(user_habit_id)

    sum_logins = crud.get_user_habit_progress_sum(user_habit_id)
    goal = crud.get_user_habit_goal(user_habit_id)
    date_of = date.today()

    end_date = crud.get_user_habit_end_date(user_habit_id).date()
    days_left = (end_date-date_of).days
    
    journal_entries = crud.get_journal_entries_by_user_habit(user_habit_id)
    log_date = crud.get_user_habit_log_dates(user_habit_id)
    
    if sum_logins:
        progress = float(sum_logins/goal)*100
    else:
        progress = 0
    return render_template("habit_progress.html", progress=progress, user_habit_name=user_habit_name, days_left=days_left, journal_entries=journal_entries, log_date=log_date)

@app.route('/logout')
def logout():
    """User must be logged in to use logout"""

    del session['user_id']
    flash("You have been logged out")

    return redirect('/')

@app.route('/messages/<user_habit_id>')
def display_accountability_page(user_habit_id):
    """Rendering an accountability partner setup and messages page"""

    user_name = crud.get_user_by_id(session['user_id'])
    user_habit_id = user_habit_id
    user_habit_name = crud.get_user_habit_name(user_habit_id)
    print(user_habit_name)
    receiver_id = session['user_id']

    messages_db = crud.get_messages_user_habit(user_habit_id)
    
    if messages_db:
        sender_id = crud.get_sender_id(user_habit_id)
        
        sender_name = crud.get_user_by_id(sender_id)
        accountability_habit_id = crud.get_user_habit_id_habitname_userid(user_habit_name, sender_id)
        print(accountability_habit_id)
        check_messages_sender = crud.get_messages_user_habit(accountability_habit_id)
        check_messages_receiver = crud.get_messages_user_habit(user_habit_id)

        partner_sum_logins = crud.get_user_habit_progress_sum(accountability_habit_id)
        partner_goal = crud.get_user_habit_goal(accountability_habit_id)
        
        if partner_sum_logins:
            partner_progress = float(partner_sum_logins/partner_goal)*100
        else:
            partner_progress = 0
        return render_template("messages.html", user_habit_id=user_habit_id,user_name=user_name, user_habit_name=user_habit_name, sender_name=sender_name, messages_db=messages_db,partner_progress=partner_progress, check_messages_receiver=check_messages_receiver, check_messages_sender=check_messages_sender)

    else:
        return render_template("messages.html", user_habit_id=user_habit_id, user_name=user_name,user_habit_name=user_habit_name, messages_db=messages_db)

    
@app.route('/messages/<user_habit_id>', methods=['POST'])
def partner_set_up(user_habit_id):
    """Setting up accountability partners and sending messages"""
    
    
    messages = request.form.get('messages')
    message_date = date.today()  
    user_habit_id = user_habit_id
     
    receiver_id = session['user_id']
    
    messages_db = crud.get_messages_user_habit(user_habit_id)
    
      
    if not messages_db:
        email = request.form.get('email')
        sender_id = crud.get_user_by_email(email).user_id
        print(sender_id)
        messages_start = crud.create_messages(user_habit_id, sender_id, receiver_id, message_date, messages)
        flash("New partner has been sent your message")
    else:
        sender_id = crud.get_sender_id(user_habit_id)
        sender_name = crud.get_user_by_id(sender_id)
        more_messages = crud.create_messages(user_habit_id, sender_id, receiver_id, message_date, messages)   
        flash("Your partner received your message")

    return display_accountability_page(user_habit_id)
    

 
 



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)