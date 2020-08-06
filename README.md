# RIP Customers

REST in Python services for Customers data.

## Description

TODO simple description of the system

Techs used:
- [etcd](https://etcd.io) as key-value store
- [FastAPI](https://fastapi.tiangolo.com) as the web framework
- [Gunicorn](https://gunicorn.org/) server with
  [uvicorn](https://www.uvicorn.org/) workers.
- misc Python libs

### Scripts

There are some helper scripts in the [scripts](scripts/) folder:

#### `import_csv.py`

Given a csv file with customer data, add each row to the database.

Usage:

```
$ ETCD_HOST=db.example.com python scripts/import_csv.py customers.csv
```

In case no `ETCD_HOST` is provided, the script uses the value from the
`settings.env` file, i.e., `localhost`.

### Endpoints


## Running

This system needs access to an etcd3 instance running somewhere. Please set the
host in the `settings.env` file, as well as other configurations as needed.

### Docker

### In a Terminal

## Using

After the system boots up (might take a while, but less than a minute), check
the online documentation at:

- [swagger](http://localhost/docs)
- [redoc](http://localhost/redoc)

A simple way to test the system is to access the swagger and use the `Try it
out` buttons on each endpoint.


## License

Distributed under the GNU GPLv3. See [LICENSE](LICENSE) for details.
