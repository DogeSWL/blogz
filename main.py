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

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

def get_blogList():
    return Blog.query.all()

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login',methods=['POST', 'GET'])
def login():
    userN_error = ''
    pwd_error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if username == '':
            userN_error = 'Username is empty'
        if password == '':
            pwd_error = 'Password is empty'

        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        if user and user.password != password:
            pwd_error = 'Password is incorrect'
        if user != '' and user == None:
            fuserN_error = 'Username is incorrect'

    return render_template('login.html',
                            userN_error = userN_error,
                            pwd_error = pwd_error)

@app.route('/signup', methods=['POST', 'GET'])
def add_User():
    return render_template('signup.html')

@app.route('/addBlog', methods=['POST'])
def add_Blog():
    new_blogTitle = request.form['blog_Title']
    new_blogEntry = request.form['blog_NewEntry']

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
        blog = Blog(title=new_blogTitle, body=new_blogEntry)
        db.session.add(blog)
        db.session.commit()

        # lastID = db.session.query(Blog.id).order_by(Blog.id.desc()).first()
        #
        # for curID in lastID:
        #     return redirect('/blog?id'+str(curID))
        return redirect('/blog?id='+str(blog.id))

@app.route("/newpost")
def newpost_page():
    return render_template('newpost.html')

@app.route('/blog', methods=['GET'])
def blogPage():
    some_id = request.args.get('id') # extract the value of id
    if some_id == None: # if value of id returns None render template blog.html
        return render_template('blog.html',blogList=get_blogList())
    else:
        oneBlog = Blog.query.filter_by(id=some_id).all()
        return render_template('singleBlog.html', indBlog=oneBlog)

@app.route("/")
def index():
    return redirect('/blog')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'


if __name__ == "__main__":
    app.run()
