from datetime import date, timedelta
from typing import List

class Order:
    def __init__(
            self, 
            cents_order: str = None, 
            cc_order: str = None, 
            notes: str = "", 
            detergent: str = "Regular", 
            addons: List[str] = [], 
            wash_temp: str = "Cold", 
            dry_temp: str = "Med", 
            due_date: date = None,
            is_picked_up: bool = False,
            is_paid: bool = False
            ):
        self.cents_order = cents_order
        self.cc_order = cc_order
        self.notes = notes
        self.detergent = detergent
        self.addons = addons
        self.wash_temp = wash_temp
        self.dry_temp = dry_temp
        self.due_date = due_date if due_date else date.today() + timedelta(days=1)
        self.is_picked_up = is_picked_up
        self.is_paid = is_paid