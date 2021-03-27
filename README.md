# Net API

A Flask RESTful API to list, get, create, update and delete network devices.

## Run Locally

* Set up a dev virtual environment: `/setup_dev.sh`
* Run the Flask app: `python server.py`

## Run Container

* Run `docker build -t net-api .`
* Run `docker run -d -p 8080:8080 --name net-api net-api`
