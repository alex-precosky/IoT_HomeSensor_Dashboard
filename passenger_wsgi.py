import sys, os
INTERP = os.path.join(os.environ['HOME'], 'homesensors.alexwarrior.cc', 'bin', 'python')
if sys.executable != INTERP:
        os.execl(INTERP, INTERP, *sys.argv)
        sys.path.append(os.getcwd())
sys.path.insert(0, "/home/precosky/homesensors.alexwarrior.cc/WSGISQLPlot")
sys.path.insert(0, "/home/precosky/homesensors.alexwarrior.cc/FridgeAPI")

import fridgeapi
from fridgeapi import app as application
