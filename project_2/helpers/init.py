from helpers import functions

def start(app):
    # add some filters to jinja, to enable us to use it on our template files
    app.jinja_env.filters['datetimeformat'] = functions.format_datetime
    app.jinja_env.filters['gravatar'] = functions.gravatar_url
    app.jinja_env.filters['url_for'] = functions.url_for

    # teardown_appcontext closes the database
    app.teardown_appcontext(functions.close_database)

    # we're adding the cli command to initialize the database
    app.cli.command('initdb')(functions.initdb_command)

