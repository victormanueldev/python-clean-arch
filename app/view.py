from flask import Flask, request, jsonify
from app.app_events import poke, register
from app.events import related_zip_data

from .dependencies_container import app, context

customer_service = context.customer_service


@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.json
    customer_id = data['customer_id']
    first_name = data['first_name']
    middle_name = data['middle_name']
    last_name = data['last_name']
    email = data['email']
    zip_code = data['zip_code']
    customer_created = customer_service.save_customer(
        int(customer_id),
        first_name,
        middle_name,
        last_name,
        email,
        int(zip_code),
        None,
        None,
        None
    )

    related_zip_data.delay(int(customer_id), int(zip_code))
    return jsonify(customer_created), 200

