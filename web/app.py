"""
Haoran Zhang's Flask API.
"""

from flask import Flask,render_template,abort
import os
import configparser
app = Flask(__name__)
config=configparser.ConfigParser()

if os.path.isfile("./credentials.ini"):
    config.read("./credentials.ini")#read credentials.ini if exist
else:
    config.read("./app.ini")#else read fallback.ini
global PORT #set PORT as global
PORT=config["DEFAULT"]["PORT"] 
#get port from DEFAULT of credentials.ini or app.ini
global DOCROOT #set DOCROOT as global
DOCROOT=config["DEFAULT"]["DOCROOT"] 
#get port from DEFAULT of credentials.ini or app.ini
global DEBUG
DEBUG= config["DEFAULT"]["DEBUG"] 
#get debug from DEFAULT of credentials.ini or app.ini
global HOST
HOST= config["DEFAULT"]["HOST"] 
#get host from DEFAULT of credentials.ini or app.ini

@app.route("/<path:p>")
def send(p):
    p= f'{DOCROOT}{p}'#add doc root in front of path
    if "//" in p or ".." in p or "~" in p:
    #if // or .. or ~ in path,call abort to 403
        abort(403)
    else:
        if os.path.isfile(p):
        #if target file exist in the path,send success and content of the file
            f=open(p,'r')
            return f.read(),200
        else:
        #else,send 404
            abort(404)

@app.errorhandler(404)
def error_404(e):
    #send content in 404.html when send() call abort(404)
    return render_template('404.html'),404

@app.errorhandler(403)
def error_403(e):
    #send content in 403.html when send() call abort(404)
    return render_template('403.html'),403

if __name__ == "__main__":
    #DEBUG,HOST and PORT get from app.ini or credentials.ini
    app.run(debug=DEBUG, host=HOST, port=PORT)
    #port in app.ini is default 5000

