# SchedHTTP

[This service is still under development]

A simple job scheduling service written in Python. Sends an HTTP request to a specified endpoint, at a specified time.

We have built this service to trigger jobs/events via HTTP endpoints.

1. Run service on your server
2. Add scheduled calls via JSON API

...and wait for the scheduler to call your HTTP endpoints on the scheduled time!

# Installation

### Download and extract latest release
```
wget https://github.com/benjiao/SchedHTTP/archive/SchedHTTP-v1.0.0-beta.1.tar.gz
tar -xvzf SchedHTTP-v1.0.0-beta.1.tar.gz
```
### (optional) Setup activate virtual environment 
```
virtualenv env
source env/bin/activate
```

### Install Dependencies
- SQLite: `sudo apt-get install sqlite3 libsqlite3-dev`

### Install required Python libraries
```
cd SchedHTTP-SchedHTTP-v1.0.0-beta.1/
pip install -r requirements.txt
```

### Initialize databases
```
cd app
mkdir -m 775 db
python create_db.py
python create_testdb.py
```

### Run Tests to confirm installation was successfull
```
nosetests
```

...if no errors were raised, you should be good to go! Proceed to the next part.

# Running the SchedHTTP
SchedHTTP is composed of two major components (1) The Service and (2) The API. 

## The Service
The service is the main daemon that is responsible for checking for tasks that should be run at a given time and call the HTTP endpoint tied to those tasks. Running the service is simple (you should be under `app`):
```
python schedhttp-service.py start
```

Logs for the service can be found in `/var/log/schedhttp-service.err.log`

Other commands available are stop and restart:
```
python schedhttp-service.py stop
python schedhttp-service.py restart
```

# The API
The API is an HTTP API Service where you can Add, Fetch, and Delete tasks. To run it (while under `app`):
```
python schedhttp-api.py
```

Examples on how to communicate with the API can be found under the `examples` folder.











