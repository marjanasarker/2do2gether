from flask import Flask, render_template
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    
    return render_template('homepage.html')

@app.route('/login')
def show_login_form(): #get the login page


    return render_template('login.html')


@app.route('/login', methods=['POST'])
def register_user():
    """Creating new user"""

    first_name = request.form.get('fname')
    last_name = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash('Cannot create an account with that email. Try again.')
    else:
        crud.create_user(fname, lname, email, password)
        flash('Account created! Please log in.')

    return redirect('/login') #redirect to a profile page 


    #return render_template('login.html')

    

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)