"""Classes for melon orders."""

from random import randint
from datetime import datetime


class AbstractMelonOrder(object):
    """An abstract melon order"""

    base_price = 5
    shipped = False

    # Children need these:
    order_type = None
    tax = None

    def __init__(self, species, qty):
        """Initialize melon order"""

        self.species = species
        self.qty = qty

    def get_base_price(self):
        """Randomly choose base price between 5 and 9"""

        price = randint(5, 9)

        now = datetime.now()
        weekday = now.weekday()
        hour = now.hour

        if weekday < 5 and 7 < hour < 12:
            price = price + 4

        return price

    def get_total(self):
        """Calculate price, including tax"""

        self.base_price = self.get_base_price()

        if self.species == "christmas melon":
            self.base_price = self.base_price * 1.5

        total = (1 + self.tax) * self.qty * self.base_price
        return total

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True


class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    order_type = "domestic"
    tax = 0.08


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    order_type = "international"
    tax = 0.17

    def __init__(self, species, qty, country_code):
        """Initialize melon order attributes."""

        self.country_code = country_code
        return super(InternationalMelonOrder, self).__init__(species, qty)

    def get_total(self):
        """ Calculate total including $3 flat fee for qty < 10"""

        total = super(InternationalMelonOrder, self).get_total()
        if self.qty < 10:
            total = total + 3
        return total

    def get_country_code(self):
        """Return the country code."""

        return self.country_code


class GovernmentMelonOrder(AbstractMelonOrder):
    """A Government melon order"""

    order_type = "government"
    tax = 0
    passed_inspection = False

    def mark_inspection(self, passed):
        """Mark as passed or not passed"""

        self.passed_inspection = passed
