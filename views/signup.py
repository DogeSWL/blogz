from flask import request, redirect, render_template
from models import User
from app import app, db

import bcrypt

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
            return render_template('signup.html',
                                    signUp_user_error=signUp_user_error)

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
        if (su_password  and su_username) and (len(su_password) < 3 or len(su_username) < 3):
            signUp_invalid_error = 'Either username or password is invalid'

        # commit to db if username & password is filld and password & verify pass is the same
        # after committing redirect to login page
        if (su_username) and (su_password) and (su_vpassword) and (su_password == su_vpassword) and (signUp_invalid_error == ''):

            # generate salt
            pwdSalt = bcrypt.gensalt()
            # hash password
            hashed = bcrypt.hashpw(str.encode(su_password),pwdSalt)

            user = User(username=su_username, hashSalt=pwdSalt, hashpwd=hashed)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')

    return render_template('signup.html',
                            signUp_user_error = signUp_user_error,
                            signUp_pass_error = signUp_pass_error,
                            signUp_vpass_error = signUp_vpass_error,
                            signUp_invalid_error = signUp_invalid_error)
