import os
from flask import Flask, send_file
import time
import threading
import traceback
import sys
import io

app = Flask(__name__)

@app.route("/")
def hello_world():
    return send_file( os.path.join( 'data', 'input-data.m3u' ) )


class FlaskStub( threading.Thread ):
    """This is just a test stub for the unittests

    its running as a daemon making sure when the tests are done the thread is stopped as well
    """
    def __init__(self):
        threading.Thread.__init__( self, daemon = True )
        return

    def start( self ):
        print( "Starting the STUB" )
        # Remove the startup messages form the Flask and werkzeug modules
        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = sys.stderr = io.StringIO()
        threading.Thread.start( self )
        # This is needed to let the Flask framework startup before the tests may start
        time.sleep( 1 )
        # Return to normal
        sys.stdout = stdout
        sys.stderr = stderr
        print( "STUB running" )

        return

    def run(self) -> None:
        try:
            app.run( host = 'localhost', port = 5000, debug = False)

        except Exception as exc:
            print( traceback.format_exc() )

        except BaseException as exc:
            print( traceback.format_exc() )

        return
