from dataclasses import dataclass


@dataclass
class Category:
    def __init__(self, rate, quantity, weight):
        self.rate = rate
        self.quantity = quantity
        self.weight = weight

    def __repr__(self):
        return f'Category({self.rate}, {self.quantity}, {self.weight})'
