from flask import request, redirect, render_template, session
from models import User
from app import app

import bcrypt

@app.route('/login',methods=['POST', 'GET'])
def login():
    userN_error = ''
    pwd_error = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        # if not encoded will cause =>
        # TypeError: Unicode-objects must be encoded before hashing
        testpw = str.encode(password)
        testsalt = str.encode(user.hashSalt)
        testhashpw = bcrypt.hashpw(testpw, testsalt)

        # convert from bytes to str
        salted_inputpwd = testhashpw.decode('utf-8')

        print(salted_inputpwd)
        print(user.hashpwd)

        if username == '':
            userN_error = 'Username required'
        if password == '':
            pwd_error = 'Password required'

        if user and user.hashpwd == salted_inputpwd:
            session['username'] = username
            return redirect('/newpost')
        if user and user.hashpwd != salted_inputpwd:
            pwd_error = 'Password is incorrect'
        if username != '' and not user:
            userN_error = 'Username is incorrect'

    return render_template('login.html',
                            userN_error = userN_error,
                            pwd_error = pwd_error)
