from game.item.item import Item

class Item_slot:
    def __init__(self, item: Item, quantity = 1):
        self.item = item
        self.quantity = quantity
        
    @staticmethod
    def create_item_slot(item: Item, quantity = 1):
        return Item_slot(item, quantity)
    
    def __repr__(self):
        return f"{self.item} x{self.quantity}"
    
    def to_json(self):
        return {
            "item": self.item.to_json() if hasattr(self.item, "to_json") else self.item,
            "quantity": self.quantity
        }