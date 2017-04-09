#!/usr/bin/python


import dateutil.parser
from datetime import datetime,timedelta
import pytz

import csv

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager


font_path = '/home/precosky/homesensors.alexwarrior.cc/Humor-Sans-1.0.ttf'
font_prop = font_manager.FontProperties(fname=font_path)
matplotlib.rcParams['font.family'] = font_prop.get_name()

matplotlib.use('Agg')



def makePlot( f, numDays ):
    temps =[]
    batvoltages=[]
    times = []


    plt.xkcd()

    csvreader = csv.DictReader(f)

    for row in csvreader:
        batvoltages.insert(0,row['batvoltage'])

        time_utc = dateutil.parser.parse(row['timestamp'])

        time = time_utc.astimezone(pytz.timezone('US/Pacific'))
        times.insert(0, time)


    fig, ax = plt.subplots(1)
    fig.autofmt_xdate()

    ax.yaxis.grid(linewidth=1.0)
    

    batvoltageLine, = plt.plot(times,batvoltages, '-', markersize=0, linewidth=2, label='Battery Voltage')
    batvoltageLine.set_antialiased(True)

#    plt.grid(b=True, which='major', color='r', linestyle='-')
    
    plt.title('Fridge Temp Sensor Battery Voltagae, Past %d Days' % numDays, fontproperties=font_prop)
    plt.xlim(datetime.utcnow() - timedelta(days=numDays), datetime.utcnow() )
    plt.ylim(2.5,4.5)
    plt.xlabel('Sample Time (Pacific Time)')
    plt.legend(prop=font_prop)


    for text in ax.texts:
        text.set_fontproperties(font_prop)
    

    for label in ax.get_xticklabels():
        label.set_fontproperties(font_prop)

    for label in ax.get_yticklabels():
        label.set_fontproperties(font_prop)

    label = ax.xaxis.get_label()
    label.set_fontproperties(font_prop)


    plt.savefig('BatteryPlot.png')      
    

if __name__ == "__main__":
    print "Content-type:text/html\r\n\r\n"
    makePlot( open("batteryData.csv"))
    



