from flask import request, redirect, flash, render_template, session
from models import User, Blog
from app import app, db
from views.login import login
from views.signup import signup

def get_blogList():
    return Blog.query.all()

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

@app.route('/addBlog', methods=['POST'])
def add_Blog():
    new_blogTitle = request.form['blog_Title']
    new_blogEntry = request.form['blog_NewEntry']

    # grab current user
    owner = User.query.filter_by(username=session['username']).first()

    title_Error = ''
    entry_Error = ''

    if new_blogTitle == '':
        title_Error = 'Title is empty'
    if new_blogEntry == '':
        entry_Error = 'Entry is empty'

    if (title_Error != '') or (entry_Error != ''):
        return render_template('newpost.html',
                                title_Error = title_Error,
                                entry_Error = entry_Error)
    else:
        blog = Blog(title=new_blogTitle, body=new_blogEntry, owner_id=owner.id)
        db.session.add(blog)
        db.session.commit()

        return redirect('/blog?id='+str(blog.id))

@app.route("/newpost")
def newpost_page():
    return render_template('newpost.html',
                            sessionCheck=checkSession())

@app.route('/blog', methods=['GET'])
def blog():

    some_id = request.args.get('id') # extract the value of id
    userID = request.args.get('user')

    if userID:
        userPage_blogs = Blog.query.filter_by(owner_id=userID)
        userPage_username = User.query.filter_by(id=userID).first()
        return render_template('singleUser.html',
                                userPage_blogs=userPage_blogs,
                                userPage_username=userPage_username,
                                sessionCheck=checkSession())

    if some_id == None: # if value of id returns None render template blog.html
        return render_template('blog.html',
                                blogList=get_blogList(),
                                sessionCheck=checkSession())
    else:
        oneBlog = Blog.query.filter_by(id=some_id).all()
        return render_template('singleBlog.html',
                                indBlog=oneBlog,
                                sessionCheck=checkSession())

@app.route('/index')
def home():
    all_users = User.query.all()
    # sessionCheck = checkSession()

    return render_template('index.html',
                            all_users=all_users,
                            sessionCheck=checkSession())

@app.route("/")
def index():
    return redirect('/index')


if __name__ == "__main__":
    app.run()
