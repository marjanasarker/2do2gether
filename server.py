from flask import Flask, render_template
from model import connect_to_db

app = Flask(__name__)
app.secret_key = "dev"
#app.jinja_env.undefined = StrictUndefined

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)