

class Customer:
    def __init__(self, customer_id, first_name, middle_name, last_name, email, zip_code, city, county, state):
        self.customer_id = customer_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.zip_code = zip_code
        self.city = city
        self.county = county
        self.state = state

    def to_json(self):
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'zip_code': self.zip_code,
            'city': self.city,
            'county': self.county,
            'state': self.state,
        }


