import os
from flask import Flask, request, render_template, redirect, url_for, flash, session
from functools import wraps
from sqlalchemy import and_, or_
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

#user table store user information
class User(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.name


@app.before_first_request
def create_db():
    if os.path.exists("data.db"):
        return

    db.create_all()

    # create admin, this line cannot be fixed.
    admin = User(name='admin', password='admin')
    db.session.add(admin)


    # insert some user example
    guestes = [User(name='guest1', password='guest1'),
               User(name='guest2', password='guest2')]
    db.session.add_all(guestes)
    db.session.commit()

#check if the user name and password are right
def valid_login(name, password):
    user = User.query.filter(and_(User.name == name, User.password == password)).first()
    if user:
        return True
    else:
        return False

#check if the user name has been registered
def valid_regist(name):
    user = User.query.filter(or_(User.name == name)).first()
    if user:
        return False
    else:
        return True

#for security, make sure some page can only be accessed after login
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('name'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))
    return wrapper

#return home page
@app.route('/')
def index():
    return render_template('index.html', name=session.get('name'))

# @app.route('/chatbot', methods=['GET', 'POST'])
# @login_required
# def chatbot():
#     return render_template('chatbot.html')
#login api
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # login function
    if request.method == 'POST':
        # print('test_name', request.form['name'])
        # print('test_pass', request.form['pass'])
        # print('test_存在', valid_regist(request.form['name']))
        # print('test_密码是否对', valid_login(request.form['name'], request.form['pass']))
        if valid_regist(request.form['name']):
            error = 'account has not been signed up'

        elif valid_login(request.form['name'], request.form['pass']):
            session['name'] = request.form.get('name')
            return redirect(url_for('chatbot'))

        else:
            error = 'wrong name or password！'
    # access login page
    return render_template('login.html', error=error)

# logout api
@app.route('/logout')
def logout():
    # pop user session and return home page
    session.pop('name', None)
    return redirect(url_for('index'))

# sign up api
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    print("sadasda")
    error = None
    if request.method == 'POST':
        # check if the password are equal
        if request.form['pass'] != request.form['re_pass']:
            error = 'passwords are different！'
        # check if user has been registered
        elif valid_regist(request.form['name']):
            user = User(name=request.form['name'], password=request.form['pass'])
            db.session.add(user)
            db.session.commit()
            print("test1")
            return redirect(url_for('login'))
        else:

            error = 'name has been used'

    return render_template('sign_up.html', error=error)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run()








