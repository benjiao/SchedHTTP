# SchedHTTP

[This service is still under development]

A simple job scheduling service written in Python. Sends an HTTP request to a specified endpoint, at a specified time.

We have built this service to trigger jobs/events via HTTP endpoints.

1. Run service on your server
2. Add scheduled calls via JSON API

...and wait for the scheduler to call your HTTP endpoints on the scheduled time!

# Installation

## Download and extract latest release
```
wget https://github.com/benjiao/SchedHTTP/archive/SchedHTTP-v1.0.0-beta.1.tar.gz
tar -xvzf SchedHTTP-v1.0.0-beta.1.tar.gz
```
## (optional) Setup activate virtual environment 
```
virtualenv env
source env/bin/activate
```

## Install Dependencies
- SQLite: `sudo apt-get install sqlite3 libsqlite3-dev`

## Install required Python libraries
```
cd SchedHTTP-SchedHTTP-v1.0.0-beta.1/
pip install -r requirements.txt
```

## Initialize databases
```
cd /app
mkdir -m 775 db
python create_db.py
python create_testdb.py
```

## Run Tests to confirm installation is successfull
```
nosetests
```

...if no errors were raised, you should be good to go!
