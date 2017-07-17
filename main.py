from flask import request, redirect, flash, render_template, session
from models import User, Blog
from app import app, db

from views.login import login
from views.signup import signup
from views.addBlog import addBlog

def get_blogData_all():
    return db.engine.execute('''SELECT user.id AS id, user.username AS username, blog.title as title, blog.body as body
                                FROM blog
                                LEFT JOIN user ON user.id = blog.owner_id''')

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

@app.route('/blog', methods=['GET'])
def blog():
    some_id = request.args.get('id') # extract the value of id
    userID = request.args.get('user')

    blogData = Blog.query.filter_by(owner_id=userID)
    userData = User.query.filter_by(id=userID).first()

    if userID:
        return render_template('singleUser.html',
                                blogData=blogData,
                                userData=userData,
                                sessionCheck=checkSession())

    if some_id == None: # if value of id returns None render template blog.html


        return render_template('blog.html',
                                blogList=get_blogData_all(),
                                sessionCheck=checkSession())
    else:
        oneBlog = Blog.query.filter_by(id=some_id).all()
        return render_template('singleBlog.html',
                                indBlog=oneBlog,
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
