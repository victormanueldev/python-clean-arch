import os
import requests
import json
from celery import Celery
from app.app_events import register

from ...dependencies_container import context

customer_service = context.customer_service


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://172.18.0.2:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://172.18.0.2:6379")

# External ZIP code API
zip_code_api = 'https://www.zipcodeapi.com/rest/'
zip_code_api_token = 'DemoOnly00Vjbv48XeZWzzxdp61OmV0oaOKqce7Ev2zZWZTDUxNuJbrUPObfCtQ7'


@celery.task
def related_zip_data(customer_id, zip_code):
    result = requests.get(f'{zip_code_api}/rest/{zip_code_api_token}/info.json/{zip_code}/degrees')
    try:
        data = json.loads(result.text)
        print(data)
        customer_service.update_customer(customer_id, data['city'], None, data['state'])
    except Exception as e:
        print(f'Error getting the zip code data', e)
    finally:
        return True
