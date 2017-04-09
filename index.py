#!/usr/bin/python

import cgitb
cgitb.enable()

import pdb

import StringIO
import csv

from datetime import date

import site
site.addsitedir("/home/precosky/lib/python/")

import urllib2

import plotTemp
import plotBattery

import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

# mode append, 1 megabyte max size, one backup
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)




public_key='lzovRNoOO6hm7RwrNRg2'
base_url = 'http://data.sparkfun.com'
#get_url = base_url + '/output/' + public_key + '.csv?gt[timestamp]=' + date.today().strftime("%m-%d-%Y")


# Query data for temperature plot
samples_to_read=650
decimation=10


csvTemplines = []
for page_num in range(1,2):
    get_url = '%s/output/%s.csv?limit=%d&sample=%d' % (base_url, public_key, samples_to_read, decimation)

    logger.info("Requesting data from " + get_url)

    pagelines = urllib2.urlopen(get_url).readlines()

    if page_num==1:
        csvTemplines += pagelines
    else:
        csvTemplines += pagelines[1:]

    logger.info("Read %d lines total" % len(csvTemplines))

logger.info("Temp data received")



# Query data for voltage plot
samples_to_read=1550
decimation=315

csvBatterylines = []
for page_num in range(1,2):
    get_url = '%s/output/%s.csv?limit=%d&sample=%d' % (base_url, public_key, samples_to_read, decimation)

    logger.info("Requesting data from " + get_url)

    pagelines = urllib2.urlopen(get_url).readlines()

    if page_num==1:
        csvBatterylines += pagelines
    else:
        csvBatterylines += pagelines[1:]

    logger.info("Read %d lines total" % len(csvBatterylines))



logger.info("Battery data received")



print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>Alex Home Sensors</title>'
print '</head>'
print '<body>'
print '<h2>Hi here are sensors</h2>'



plotTemp.makePlot(csvTemplines)
plotBattery.makePlot(csvBatterylines, 59)

logger.info("Plot prepared")

print '<img src="GeneralPlot.png" />  <img src="BatteryPlot.png" \>'
#print '<img src="GeneralPlot.png" /> '


print '</body>'
print '</html>'
