import abc


class CustomerRepository(metaclass=abc.ABCMeta):
    """ Customer Repository Interface"""

    @abc.abstractmethod
    def save_customer(self, customer):
        pass

    @abc.abstractmethod
    def update_customer(self, customer_id, city, count, state):
        pass
