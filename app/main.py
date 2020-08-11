import logging
import json
import os
from typing import List

from dotenv import load_dotenv
import etcd3
from etcd3.exceptions import ConnectionFailedError
from fastapi import FastAPI, HTTPException

from .geo import coordinates
from .models import Customer, CustomerId, Message

load_dotenv('settings.env')
ETCD_HOST = os.getenv('ETCD_HOST')
ETCD_PORT = os.getenv('ETCD_PORT')

app = FastAPI(title='RIP Customers',
              description='Rest api In Python for managing customer data',
              version='0.2.1')


def db():
    etcd = etcd3.client(host=ETCD_HOST, port=ETCD_PORT)

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


@app.post('/customers/',
          status_code=201,
          responses={
              403: {'model': Message, 'description': "Customer's id already exists"}
          }
)
async def create_customer(customer: CustomerId):
    etcd = db()

    customer = customer.dict()
    id_ = customer.pop('id')
    data = etcd.get(id_)

    if data[0] is None:
        coords = coordinates(customer['city'])
        customer.update(coords)
        etcd.put(id_, json.dumps(customer))
    else:
        raise HTTPException(status_code=403,
                            detail=f'Customer {id_} already exists')


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
