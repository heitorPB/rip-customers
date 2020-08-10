import csv
import logging
import json

import click
import etcd3
from etcd3.exceptions import ConnectionFailedError

from app.geo import coordinates
from app.main import db


logging.basicConfig(level=logging.INFO)


@click.command()
@click.option('--dry-run', default=False, is_flag=True,
              help='perform a trial run with no changes made')
@click.argument('filename', type=click.File('r'))
def import_csv(dry_run, filename):
    etcd = db()

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
