

import os.path 
APP_FOLDER = os.path.dirname( os.path.realpath(__file__))


if __name__=="__main__":
   import sys
   sys.path.append( APP_FOLDER + "/bottle" )
   os.chdir( APP_FOLDER ) 

import uuid
import bottle 
import bottle.ext.sqlite # pylint: disable=E0611,E0401
import sqlite3
import logging as log

log.basicConfig(level=log.INFO)

import config 

BOTTLE_APP = bottle.Bottle()
BOTTLE_PLUGIN_SQL = bottle.ext.sqlite.Plugin(dbfile=config.DATABASE)
BOTTLE_APP.install( BOTTLE_PLUGIN_SQL )

SESSIONS = {}

def logout_raw():
    session = bottle.request.get_cookie("session")
    if session in SESSIONS:
        del SESSIONS[ session ]
        set_session("")
            
def set_session(value):
   bottle.response.set_cookie("session", value, httponly=True )

def check_login_raw():
    session = bottle.request.get_cookie("session")
    if session in SESSIONS:
        return SESSIONS[session]
    return None


def check_username_password( db, username, password ):
    # " OR "1"="1
    query = 'SELECT * from users WHERE username=\"%s\" AND password=\"%s\"' % (username, password)
    log.info("Execute querty %s", query )
    row = db.execute(query).fetchone()
    if row == None:
        return None
    return { x: row[x] for x in ["user_id", "username","level"] } 


import functools

def check_login(func):
    @functools.wraps(func)
    def wrapper( db ): # We need to have this explicitely said as DB, otherwise the bottle-sqlite wont wrap this.
        user = check_login_raw()
        if user == None:
            return bottle.redirect("/login")
        return func( db=db, user=user )
    return wrapper


@BOTTLE_APP.route('/', method='GET')
@check_login
def index( db , user ):
    rows = db.execute('SELECT comments.comment, users.username from comments join users using (user_id) ORDER BY comments.id DESC LIMIT %d' % config.LIMIT_RESULTS_ON_PAGE).fetchall()
    return bottle.template('index', { 'comments' : rows, 'user' : user } )


@BOTTLE_APP.route('/', method='POST')
@check_login
def index( db , user ):
    comment = bottle.request.forms.get('comment').strip()[0:config.MAX_COMMENT_SIZE]
    log.info("User %s comment: %s", user["username"], comment )
    db.execute("INSERT INTO comments (user_id,comment) VALUES (%d,'%s')" % (user["user_id"],comment ) )
    return bottle.redirect("/")

# This is the secret admin side .. pwwnd!
@BOTTLE_APP.route('/admin', method='GET')
@check_login
def admin_get( db, user ):
    return bottle.template('admin', { 'user' : user } )

@BOTTLE_APP.route('/admin', method='POST')
@check_login
def admin_post( db, user ):
    username = bottle.request.forms.get('username').strip()
    password = bottle.request.forms.get('password').strip()
    level    = int( bottle.request.forms.get('level').strip() )
    if not username or not password:
        return bottle.redirect("/admin")

    db.execute("INSERT INTO users (username,password,level) VALUES ('%s','%s', %d )" % (username, password, level ) )
    return bottle.redirect("/")


@BOTTLE_APP.route('/login', method='GET' )
def login_get( ):
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    return bottle.template('login')

@BOTTLE_APP.route('/logout', method='GET' )
@check_login
def logout_get( db, user ):
    log.info("User %s logout", user )
    logout_raw()
    return bottle.redirect("/login")


@BOTTLE_APP.route('/login', method='POST' )
def login_post( db ):
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    
    log.info("User %s trying to log in", username )
    user = check_username_password( db, username, password )
    
    if user == None:
       return bottle.redirect("/login")
    log.info("User %s logged in", user)
    
    session = str(uuid.uuid4())
    set_session( session )
    SESSIONS[session] = user
    return bottle.redirect("/")

    
@BOTTLE_APP.route('/static/<filename>')
def server_static(filename):
    return bottle.static_file( filename, root=APP_FOLDER + '/data_static/')


BOTTLE_APP.run(host='localhost', port=8080)

