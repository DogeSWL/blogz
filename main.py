from flask import Flask, request, redirect, flash, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:MyNewPass@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner_id):
        self.title = title
        self.body = body
        self.owner_id = owner_id

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

@app.route('/login',methods=['POST', 'GET'])
def login():
    userN_error = ''
    pwd_error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if username == '':
            userN_error = 'Username required'
        if password == '':
            pwd_error = 'Password required'

        if user and user.password == password:
            session['username'] = username
            return redirect('/index')
        if user and user.password != password:
            pwd_error = 'Password is incorrect'
        if username != '' and not user:
            userN_error = 'Username is incorrect'

    return render_template('login.html',
                            userN_error = userN_error,
                            pwd_error = pwd_error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    signUp_user_error = ''
    signUp_pass_error = ''
    signUp_vpass_error = ''
    signUp_invalid_error = ''

    if request.method == 'POST':
        su_username = request.form['username']
        su_password = request.form['password']
        su_vpassword = request.form['verifyPass']

        user_check = User.query.filter_by(username=su_username).first()

        # checks if there is input for username and if username is already in db
        # if both are true, 'username taken' error would display
        if su_username != '' and user_check:
            signUp_user_error = 'Username taken'


        # checks if inputs in forms are filled
        # if request returns empty correct error would be displayed
        if su_username == '':
            signUp_user_error = 'Username required'
        if su_password == '':
            signUp_pass_error = 'Password required'
        if su_vpassword == '':
            signUp_vpass_error = 'Verify Pass required'
        if  (su_password != '') and (su_vpassword != '') and (su_vpassword != su_password):
            signUp_vpass_error = 'Password and Verify Pass does not match'
        # checks to see if either password or username is less than 3 leters
        # if true, error would display
        if (su_password != '' or su_username != '') and (len(su_password) < 3 or len(su_username) < 3):
            signUp_invalid_error = 'Either username or password is invalid'

        # commit to db if username & password is filld and password & verify pass is the same
        # after committing redirect to login page
        if (su_username != '') and (su_password != '') and (su_password == su_vpassword):
            user = User(username=su_username, password=su_password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')

    return render_template('signup.html',
                            signUp_user_error = signUp_user_error,
                            signUp_pass_error = signUp_pass_error,
                            signUp_vpass_error = signUp_vpass_error,
                            signUp_invalid_error = signUp_invalid_error)

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
    return render_template('newpost.html')

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

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'


if __name__ == "__main__":
    app.run()
