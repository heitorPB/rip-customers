# RIP Customers

REST in Python services for Customers data.

## Description

A simple customers REST API in Python.

Techs used:
- [etcd](https://etcd.io) as key-value store
- [FastAPI](https://fastapi.tiangolo.com) as the web framework
- [Gunicorn](https://gunicorn.org/) server with
  [uvicorn](https://www.uvicorn.org/) workers.
- misc Python libs
- [MapQuest](https://mapquest.com/) for geolocation


### Scripts

There are some helper scripts for common tasks:

#### `import_csv.py`

Given a csv file with customer data, add each row to the database.

Usage:

```
$ ETCD_HOST=db.example.com python import_csv.py customers.csv
```

In case no `ETCD_HOST` is provided, the script uses the value from the
`settings.env` file, i.e., `localhost`.

The csv should have the following structure:

```
id,first_name,last_name,email,gender,company,city,title
```

The system then queries [MapQuest](https://mapquest.com/) to get the geographic
coordinates of that customer before saving in the database.

### Endpoints

The system has three endpoints:

- GET `/customers/`: list all customers in the database
- POST `/customers/`: add a new customer
- GET `/customers/{id}`: display a single customer by its `id`


## Running

This system needs access to an etcd3 instance running somewhere. Please set the
host in the `settings.env` file, as well as other configurations as needed.

It also needs a MapQuest's key to use their public API. Simply go to [MapQuest
Developer Network](https://developer.mapquest.com/user/me/apps) and create one.
The main advantage over GoogleMaps API is that MapQuest does no require your
credit card to use the free tier. Then add the key to the configuration file.

### Docker

Set your MapQuest's API key in the `settings.env` file or in the
`docker-compose.yml` file and fire it:

```
$ docker-compose up --detach
```

This starts the database and the server, running on port 80. Check
[Using](#using) below for usage.

### In a Terminal

You need a modern Python installation:

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ uvicorn app.main:app --reload
```

This will install all python dependencies and start a uvicorn server on port
8000. The `--reload` flags tells the server to reload on any source code
change, so you don't need to kill the process and start again.


## Using

After the system boots up (might take a while, but less than a minute), check
the online documentation at:

- [swagger](http://localhost/docs)
- [redoc](http://localhost/redoc)
- [openapi.json](http://localhost/openapi.json) - OpenAPI spefication

A simple way to test the system is to access the swagger and use the `Try it
out` buttons on each endpoint.

## Tests

Tests are available in the folder [tests](tests/), using `pytest`. To run them,
first start etcd:

```
$ docker-compose up --detach etcd
```

Now, run `pytest` and generate a nice HTML coverage report:

```
$ coverage run -m --souce=app pytest
$ coverage html
```

The report is available in `htmlcov/index.html`.


## License

Distributed under the GNU GPLv3. See [LICENSE](LICENSE) for details.
