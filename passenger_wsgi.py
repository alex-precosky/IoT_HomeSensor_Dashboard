import sys, os
INTERP = os.path.join(os.environ['HOME'], 'homesensors.alexwarrior.cc', 'bin', 'python')
if sys.executable != INTERP:
        os.execl(INTERP, INTERP, *sys.argv)
        sys.path.append(os.getcwd())
sys.path.insert(0, "/home/precosky/homesensors.alexwarrior.cc/WSGISQLPlot")
sys.path.insert(0, "/home/precosky/homesensors.alexwarrior.cc/FridgeAPI")

import fridgeapi
#import plotApp

from fridgeapi import app as application
#from plotApp import app as application

#def application(environ, start_response):
#    start_response('200 OK', [('Content-type', 'text/html')])
#    return plotApp.getResponse()

