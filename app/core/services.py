from .repositories import CustomerRepository
from .models import Customer


class CustomerService:

    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def save_customer(
        self,
        customer_id,
        first_name,
        middle_name,
        last_name,
        email,
        zip_code,
        city,
        county,
        state
    ):
        customer = Customer(
            customer_id=customer_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            zip_code=zip_code,
            city=city,
            county=county,
            state=state
        )
        return self.customer_repository.save_customer(customer)

    def update_customer(self, customer_id, city, county, state):
        return self.customer_repository.update_customer(customer_id, city, county, state)

