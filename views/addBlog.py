from flask import request, redirect, render_template, session
from models import User, Blog
from app import app, db

@app.route('/addBlog', methods=['POST'])
def addBlog():
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
