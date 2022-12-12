import os
import requests
import json
from ...dependencies_container import celery, context


# External ZIP code API
zip_code_api = os.environ.get('ZIPCODE_API')
zip_code_api_token = os.environ.get('ZIP_API_TOKEN')


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


