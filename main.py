from flask import request, redirect, flash, render_template, session
from app import app, db
from models import User, Blog

# importing views
from views.login import login
from views.signup import signup
from views.blog import blog
from views.addBlog import addBlog

def checkSession():
    if session:
        return 'True'
    else:
        return 'False'

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'home']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route("/newpost")
def newpost_page():
    return render_template('newpost.html',
                            sessionCheck=checkSession())

@app.route('/index')
def home():
    all_users = User.query.all()

    return render_template('index.html',
                            all_users=all_users,
                            sessionCheck=checkSession())

@app.route("/")
def index():
    return redirect('/index')


if __name__ == "__main__":
    app.run()
