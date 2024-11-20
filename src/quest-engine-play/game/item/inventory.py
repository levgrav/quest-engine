from game.item.item_slot import Item_slot

class Inventory(list):
    def __init__(self, items = []):
        for item in items:
            self.create_item_slot(item["item"], item["quantity"])
    
    def create_item_slot(self, item, quantity = 1):
        self.append(Item_slot.create_item_slot(item, quantity))    
    
    def remove_item_slot(self, item):
        item_slot = self.get_item_slot(item)
        if item_slot:
            self.remove(item_slot)
       
    def get_item_slot(self, item = None, item_name = None):
        for item_slot in self:
            if item and item_slot.item == item:
                return item_slot
            if item_slot.item.name == item_name:
                return item_slot
        return None
    
    def add_item(self, item, quantity = 1):
        item_slot = self.get_item_slot(item)
        if item_slot:
            item_slot.quantity += quantity
        else:
            self.create_item_slot(item, quantity)
            
    def remove_item(self, item, quantity = 1):
        item_slot = self.get_item_slot(item)
        if item_slot:
            item_slot.quantity -= quantity
            if item_slot.quantity == 0:
                self.remove(item_slot) 
                return quantity
            elif item_slot.quantity < 0:
                quantity += item_slot.quantity
                item_slot.quantity == 0 
                return quantity
            else:
                return quantity
        else:
            return 0
    
    def to_json(self):
        return [item_slot.to_json() for item_slot in self]
            
            