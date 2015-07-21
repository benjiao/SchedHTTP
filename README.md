# SchedHTTP

[This service is still under development]

A simple job scheduling service written in Python. Sends an HTTP request to a specified endpoint, at a specified time.

We have built this service to trigger jobs/events via HTTP endpoints.

1. Run service on your server
2. Add scheduled calls via JSON API

...and wait for the scheduler to call your HTTP endpoints on the scheduled time!

# Contribute
## Installation
Run `pip install -r requirements.txt`

## Testing
Under `app/` run `nosetests`
