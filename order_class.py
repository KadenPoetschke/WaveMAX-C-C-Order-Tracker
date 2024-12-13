from datetime import date, timedelta
from typing import List

class Order:
    def __init__(
            self, 
            cents_order: str = None, 
            cc_order: str = None, 
            notes: str = "", 
            detergent: str = "Regular", 
            addons: List[int] = [], 
            wash_temp: str = "Cold", 
            dry_temp: str = "Med", 
            due_date: date = None,
            picked_up: bool = False,
            paid: bool = False
            ):
        self.cents_order = cents_order
        self.cc_order = cc_order
        self.notes = notes
        self.detergent = detergent
        self.addons = addons
        self.wash_temp = wash_temp
        self.dry_temp = dry_temp
        self.due_date = due_date if due_date else date.today() + timedelta(days=1)
        self.picked_up = picked_up
        self.paid = paid

    def is_picked_up(self):
        return self.picked_up
    
    def is_paid(self):
        return self.paid