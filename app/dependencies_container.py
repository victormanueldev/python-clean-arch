from sqlalchemy import MetaData, create_engine
from collections import namedtuple
from flask import Flask
from celery import Celery
from .core.impl.postgres import CustomerPostgreSQLRepository
from .core.services import CustomerService

Context = namedtuple('Context', ['customer_service'])


def create_context(config):
    global context
    print('[CONFIG]', config)

    sql_host = config.get('SQL_HOST')
    sql_port = config.get('SQL_PORT')
    sql_user = config.get('SQL_USER')
    sql_pass = config.get('SQL_PASS')

    metadata = MetaData()
    engine = create_engine(f'postgresql+psycopg2://{sql_user}:{sql_pass}@{sql_host}:{sql_port}/urban_pilot')

    customers_repository = CustomerPostgreSQLRepository(metadata, engine)
    customer_service = CustomerService(customers_repository)

    metadata.create_all(engine)
    __app = create_app(config)
    context = Context(customer_service)
    return context, __app, create_celery(config, __app)


def create_app(config):
    global app
    config_broker_url = config.get('BROKER_URL') or 'redis://localhost:6379/0'
    config_result_backend = config.get('BROKER_URL') or 'redis://localhost:6379/0'
    _app = Flask('urban_pilot_LM')
    _app.config['CELERY_BROKER_URL'] = config_broker_url
    _app.config['CELERY_RESULT_BACKEND'] = config_result_backend
    _app.config.from_object(config)
    app = _app
    return _app


def create_celery(config, app_arg):
    global celery
    _celery = Celery(app_arg.name, broker=app_arg.config['CELERY_BROKER_URL'])
    _celery.conf.update(app_arg.config)
    celery = _celery
    return _celery


context = None
app = None
celery = None
