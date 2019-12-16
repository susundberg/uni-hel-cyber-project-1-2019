

import os.path 
APP_FOLDER = os.path.dirname( os.path.realpath(__file__))


if __name__=="__main__":
   import sys
   sys.path.append( APP_FOLDER + "/bottle" )


import bottle 
import bottle.ext.sqlite

BOTTLE_APP = bottle.Bottle()
BOTTLE_PLUGIN_SQL = bottle.ext.sqlite.Plugin(dbfile='/tmp/test.db')
BOTTLE_APP.install( BOTTLE_PLUGIN_SQL )

@BOTTLE_APP.route('/')
def index( db ):
    #row = db.execute('SELECT * from items').fetchone()
    return bottle.template('login')



@BOTTLE_APP.route('/static/<filename>')
def server_static(filename):
    return bottle.static_file( filename, root=APP_FOLDER + '/data_static/')


BOTTLE_APP.run(host='localhost', port=8080)

