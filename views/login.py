from flask import request, redirect, render_template, session
from app import app
from models import User

import bcrypt

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

        if userN_error or pwd_error:
            return render_template('login.html',
                                    userN_error = userN_error,
                                    pwd_error = pwd_error)

        else:
            if not user:
                userN_error = 'Username is incorrect'
                return render_template('login.html',
                                        userN_error=userN_error)

            # if not encoded will cause =>
            # TypeError: Unicode-objects must be encoded before hashing
            testpw = str.encode(password)
            testsalt = str.encode(user.hashSalt)
            testhashpw = bcrypt.hashpw(testpw, testsalt)

            # convert from bytes to str
            salted_inputpwd = testhashpw.decode('utf-8')

            if user and user.hashpwd != salted_inputpwd:
                pwd_error = 'Password is incorrect'
                return render_template('login.html',
                                        pwd_error = pwd_error)

            if user and user.hashpwd == salted_inputpwd:
                session['username'] = username
                return redirect('/newpost')

    return render_template('login.html')
