from flask_app import app
from flask_app.models.login import User
from flask import render_template,redirect,request,session,flash

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register/user', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    print(request.form)
    user_id = User.create_user(data)
    session['user_id'] = user_id
    return redirect('/success')



@app.route('/login',methods=['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    print('user:',user_in_db)
    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    print(user_in_db.first_name)
    flash('You have successfully logged in')
    return redirect('/success')


@app.route('/success')
def show_user():
    if not "user_id" in session:
        flash('Please log in!')
        return redirect("/")
    data = {
            "id" :session["user_id"]
        }
    user = User.choose_user_by_email(data)
    return render_template("signedin.html", user = user)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')