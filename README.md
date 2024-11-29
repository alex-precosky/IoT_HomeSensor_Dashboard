
# About

Provides an HTTP API for querying historic sensor data, and provides a web site showing plots of sensor data.

It's hosted at http://homesensors.alexwarrior.cc where the project is described further.

# Requirements

* Python 2.7
* MySQL
* The mysql-client package, which might not install in Windows with pip as below, so might be installed separately perhaps through Anaconda

# Setup

There's a submodule that's needed, so after cloning this repository, get the submodule with...
```
git submodule init
git submodule update
```

Recreate the pip virtual environment, probably in a virtual environment of some sort.  I use Anaconda sometimes, so I might do...

```
conda create -n HomeSensors python=2.7 anaconda
activate HomeSensors
pip install -r requirements.txt
```

On windows with anaconda you might also need to do 
```
conda install mysql-python
```

Since the pip mysql-client might not install.

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

# Running

To test locally, using Windows...:
```
cd FridgeAPI
python fridgeapi.py
```

The site is then available at http://localhost:5000

Serving from using Passenger:

passenger_wsgi.py was used by Apache to host the site, but it hasn't been tried with other servers

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
