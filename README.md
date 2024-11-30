# About

Provides an HTTP API for querying historic sensor data, and provides a web site showing plots of sensor data.

It's hosted at http://homesensors.alexwarrior.cc where the project is described further.

# Requirements

* [Python Hatch](https://hatch.pypa.io/latest/)
* A MySQL serer

# Setup

There's a submodule that's needed - the
[rickshaw](https://tech.shutterstock.com/rickshaw/) JavaScript time series
plotting toolkint, so after cloning this repository, get the submodule with...

```
git submodule init
git submodule update
```

Recreate the python virtual environment.

```
hatch shell
```

The database should be set up in a MySQL instance, by restoring the provided schema. The database can be named whatever you want:
```
mysql -u [uname] -p[pass] -h[host] [db_to_restore] < schema.sql
```

Fake data for the past 24 hours can be inserted using the test script populate_test_db.py


The connection info must be set in a file ```config.ini``` to be placed in directory FridgeAPI, formatted like:
```
[mysql]
host = mysql.mysite.com
user = my_username
password = myPassWord
db = my_db_name
```

# Serving

## Locally

To test locally, using Windows...:
```
hatch run serve
```

The site is then available at http://localhost:8000

## Serving using Passenger

File `passenger_wsgi.py` was used by Apache to host the site, but it hasn't been
tried with other servers.

DreamHost removed Passenger support in 2024 from its shared hosting plan so this
isn't used anymore.

## Serving using FastCGI

File `homesensors.fcgi` can be modified to let Apache serve this using
FastCGI. Modify the path to the Python interpreter in the first line to point to
the Python interpreter set up if `hatch shell` is run. That interpreter will be
able to find the dependencies this application needs.


# HTTP API
* /getData
For plots by the rickshaw package. Returns temperatures and battery voltages

Parameters: 
 * since: ISO8601 timestamp of where to start samples from
 * maxPoints: maximum number of points to return

 * /last24hours
For rickshaw plotting.  No parameters.  Returns a bunch of points using the /getData function, but for only the last 24 hours

# TODO

Remove unneeded requirements from the pip requirements.txt list 

# License

This is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
