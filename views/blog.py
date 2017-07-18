from flask import request, render_template, session
from models import User, Blog
from app import app, db

def get_blogData_all():
    return db.engine.execute('''SELECT user.id AS id, user.username AS username, blog.id as blog_id, blog.title as title, blog.body as body
                                FROM blog
                                LEFT JOIN user ON user.id = blog.owner_id''')

def checkSession():
    if session:
        return 'True'
    else:
        return 'False'

@app.route('/blog', methods=['GET'])
def blog():
    blogID = request.args.get('id') # extract the value of id
    userID = request.args.get('user')

    if userID:
        blogData = Blog.query.filter_by(owner_id=userID).all()
        oneUser = User.query.filter_by(id=userID).first()

        return render_template('singleUser.html',
                                blogData=blogData,
                                oneUser=oneUser,
                                sessionCheck=checkSession())

    if blogID == None: # if value of id returns None render template blog.html


        return render_template('blog.html',
                                blogList=get_blogData_all(),
                                sessionCheck=checkSession())
    else:
        oneBlog = Blog.query.filter_by(id=blogID).first()
        oneUser = User.query.filter_by(id=oneBlog.owner_id).first()

        return render_template('singleBlog.html',
                                oneBlog=oneBlog,
                                oneUser=oneUser,
                                sessionCheck=checkSession())
