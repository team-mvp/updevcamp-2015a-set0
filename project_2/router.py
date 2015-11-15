from flask import g, session
from helpers import functions, init
from controllers import follow, timeline, tweet, user

def set_router(app):
    # we're setting g.user as the user in the current session
    @app.before_request
    def before_request():
        g.user = None
        if 'user_id' in session:
            # if there is a user_id in session
            # select it and set g.user to it
            g.user = functions.query_db('select * from user where user_id = ?',
                              [session['user_id']], one=True)

    ### Our Routes ###

    # timeline routes
    app.route('/')(timeline.index)
    app.route('/public')(timeline.public)
    app.route('/<username>')(timeline.user)

    # follow routes
    app.route('/<username>/follow')(follow.follow_user)
    app.route('/<username>/unfollow')(follow.unfollow_user)

    # tweet routes
    app.route('/add_message', methods=['POST'])(tweet.add_message)

    # user routes
    app.route('/login', methods=['GET', 'POST'])(user.login)
    app.route('/register', methods=['GET', 'POST'])(user.register)
    app.route('/logout')(user.logout)
