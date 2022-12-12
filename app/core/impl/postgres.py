from contextlib import contextmanager

from sqlalchemy import (Column, Integer, String, Table, insert, update)

from ..models import Customer
from ..repositories import CustomerRepository


@contextmanager
def transactional(engine):
    """
    Transactional Context
    """
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()
        connection = None


class CustomerPostgreSQLRepository(CustomerRepository):
    """
    Customer Repository for PostgresQL
    """
    customers = None

    @classmethod
    def create_table_schema(cls, metadata):
        """ Create the table schema using SQL Alchemy"""
        if cls.customers is not None:
            return
        cls.customers = Table(
            'customers',
            metadata,
            Column('customer_id', Integer(), primary_key=True),
            Column('first_name', String(200), nullable=False),
            Column('middle_name', String(200), nullable=False),
            Column('last_name', String(200), nullable=False),
            Column('email', String(200), nullable=False),
            Column('zip_code', Integer(), nullable=False),
            Column('city', String(100), nullable=True),
            Column('county', String(200), nullable=True),
            Column('state', String(4), nullable=True),
        )

    def __init__(self, metadata, engine):
        self.__class__.create_table_schema(metadata)
        self.engine = engine

    def save_customer(self, customer):
        """ Insert a customer into DB """
        with transactional(self.engine) as connection:
            t = connection.begin()
            result = connection.execute(insert(self.__class__.customers).values(**self._from_object(customer)))
            if result:
                t.commit()
                return self._from_object(customer)
            raise Exception("Something went wrong trying to insert a customer")

    def update_customer(self, customer_id, city, count, state):
        with transactional(self.engine) as connection:
            t = connection.begin()
            rows_updated = connection.execute(update(self.__class__.customers).where(
                self.__class__.customers.column.customer_id == customer_id).values(
                city=city,
                count=count,
                state=state
            ))
            if rows_updated:
                t.commit()
                return True
            raise Exception("Something went wrong trying to update customer's city")

    @staticmethod
    def _from_object(customer):
        return dict(
            customer_id=customer.customer_id,
            first_name=customer.first_name,
            middle_name=customer.middle_name,
            last_name=customer.last_name,
            email=customer.email,
            zip_code=customer.zip_code,
        )

    @staticmethod
    def _to_object(row):
        for row in row:
            if not row:
                return None
            return Customer(
                row['customer_id'],
                row['first_name'],
                row['middle_name'],
                row['last_name'],
                row['email'],
                row['zip_code'],
            )
