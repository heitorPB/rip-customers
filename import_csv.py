import csv
import logging
import json
import os

import click
from dotenv import load_dotenv
import etcd3
from etcd3.exceptions import ConnectionFailedError

from app.geo import coordinates


load_dotenv('settings.env')
ETCD_HOST = os.getenv('ETCD_HOST')
ETCD_PORT = os.getenv('ETCD_PORT')

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option('--dry-run', default=False, is_flag=True,
              help='perform a trial run with no changes made')
@click.argument('filename', type=click.File('r'))
def import_csv(dry_run, filename):
    etcd = etcd3.client(host=ETCD_HOST, port=ETCD_PORT)

    try:
        status = etcd.status()
    except ConnectionFailedError:
        logging.critical(f'Could not connect to etcd')
        return

    reader = csv.DictReader(filename)
    for row in reader:
        logging.info(f'Adding entry id={row["id"]} to db')

        customer = row.copy()
        customer.pop('id')
        city = customer['city']
        customer.update(coordinates(city))

        if not dry_run:
            etcd.put(row['id'], json.dumps(customer))
        else:
            logging.debug(customer)


if __name__ == '__main__':
    import_csv()
