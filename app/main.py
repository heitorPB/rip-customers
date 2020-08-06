import logging
import json
import os
from typing import List

from dotenv import load_dotenv
import etcd3
from etcd3.exceptions import ConnectionFailedError
from fastapi import FastAPI, HTTPException

from .models import Customer, Message

load_dotenv('settings.env')
ETCD_HOST = os.getenv('ETCD_HOST')
ETCD_PORT = os.getenv('ETCD_PORT')

app = FastAPI()


def db():
    etcd = etcd3.client()

    try:
        status = etcd.status()
    except ConnectionFailedError:
        logging.critical(f'Could not connect to etcd')
        raise HTTPException(status_code=503,
                            detail='Could not connect to the database')

    return etcd


@app.get('/customers/',
         response_model=List[Customer])
async def customers():
    etcd = db()

    data = list()
    for customer in etcd.get_all():
        # TODO add the customer's ID here?
        data.append(json.loads(customer[0]))

    return data


@app.get('/customers/{customer_id}',
         response_model=Customer,
         responses={
             404: {'model': Message, 'description': 'Customer not found'}
         }
)
async def customer(customer_id: str):
    etcd = db()

    data = etcd.get(customer_id)
    if data[0] is None:
        raise HTTPException(status_code=404,
                            detail=f'Customer {customer_id} not found')
    else:
        return json.loads(data[0])
