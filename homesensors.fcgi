#!/home/precosky/.local/share/hatch/env/virtual/iot-homesensor-dashboard/jF9Rdmx3/iot-homesensor-dashboard/bin/python

from flup.server.fcgi import WSGIServer
from iot_homesensor_dashboard.fridgeapi import app

if __name__ == '__main__':
    WSGIServer(app).run()
