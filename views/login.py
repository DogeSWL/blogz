from flask import request, redirect, render_template, session
from models import User
from app import app

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
            return redirect('/newpost')
        if user and user.password != password:
            pwd_error = 'Password is incorrect'
        if username != '' and not user:
            userN_error = 'Username is incorrect'

    return render_template('login.html',
                            userN_error = userN_error,
                            pwd_error = pwd_error)
