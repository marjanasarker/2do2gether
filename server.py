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

    user = crud.get_user_by_email(email)
    

    if user:
        flash('Cannot create an account, email on file. Try again.')
    else:
        new_user = crud.create_user(first_name, last_name, email, password)
        flash('Account created! Please log in.') #where should I redirect them 

    return redirect('/login') #redirect to a profile page 


    #return render_template('login.html')
@app.route('/login')
def regular_user_login():

    return render_template('login.html')

#@app.route('/login', methods=['POST'] )
#def regular_user_login():

    #redirect('login.html')  change this
    

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)