from helpers import functions
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

def login():
    """Logs the user in."""
    if g.user:
        return redirect(functions.url_for('/'))
    error = None
    if request.method == 'POST':
        user = functions.query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(functions.url_for('/'))
    return render_template('login.html', error=error)

def register():
    """Registers the user."""
    if g.user:
        return redirect(functions.url_for('/'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif functions.get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            db = functions.get_db()
            db.execute('''insert into user (username, email, pw_hash) values (?, ?, ?)''', [request.form['username'], request.form['email'],  generate_password_hash(request.form['password'])])
            db.commit()
            flash('You were successfully registered and can login now')
            return redirect(functions.url_for('login'))
    return render_template('register.html', error=error)

def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(functions.url_for('/public'))