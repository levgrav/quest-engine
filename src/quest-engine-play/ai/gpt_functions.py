import os
import random
from game.item.inventory import Inventory
from game.item.item import Item
from game.character.character import Character


class Gpt_Functions:

    def __init__(self, project_model) -> None:
        self.project_model = project_model
        self.references = {
            f'player_{player.name}': player for player in self.project_model.world.players
        } | {
            f'npc_{npc.name}': npc for npc in self.project_model.world.npcs
        }
        self.helper = HelperFunctions(self)
        
    # --- General Functions --- #
    def rng(self, min = 0, max = 1):
        return str(random.random() * (max - min) + min)
    
    def get_data(self, entity_reference):
        entity = self.helper.get_reference(entity_reference)
        if entity == None:
            entity = self.helper.get_location(entity_reference)
        if entity == None:
            return f"entity {entity_reference} not found"
        return repr(entity)
    
    def quit_program(self):
        global done
        done = True
        return "Goodbye!"
    
    # --- World Interaction and Modification --- #
    def create_generic_item(self, name, inventory_reference, set_reference = None, **kwargs):
        item = Item(name = name, **kwargs)
        inventory = self.helper.get_reference(inventory_reference)
        if inventory == None:
            return f"Inventory {inventory_reference} not found"
        inventory.add_item(item)
        if set_reference:
            self.helper.create_reference(set_reference, item)
            
        return f"Created a {name} with the following properties: {kwargs}"
    
    def create_generic_npc(self, name, set_reference = None, **kwargs):
        npc = Character(name = name, **kwargs)
        if set_reference:
            self.helper.create_reference(set_reference, npc)
        
        return f"Created an NPC named {name} with the following properties: {kwargs}"
    
    def move_item(self, item_reference, from_inventory_reference, to_inventory_reference, **kwargs):
        item = self.helper.get_reference(item_reference)
        from_inventory = self.helper.get_reference(from_inventory_reference)
        to_inventory = self.helper.get_reference(to_inventory_reference)
        
        if item == None: return f"Item {item_reference} not found"
        if from_inventory == None: return f"Inventory {from_inventory_reference} not found"
        if to_inventory == None: return f"Inventory {to_inventory_reference} not found" 
        
        quantity = kwargs.get('quantity', 1)
        quantity = from_inventory.remove_item(item, quantity)
        to_inventory.add_item(item, quantity)
        
        return f"Moved ({quantity}) {item_reference} from {from_inventory_reference} to {to_inventory_reference}"
    
    def add_event(self, **kwargs):
        return f"Added event: {kwargs.get('name', 'Unnamed Event')}"
    
    def remove_object(self, object_name, inventory_reference, set_reference = None):
        
        inventory = self.helper.get_reference(inventory_reference)
        if inventory == None:
            return f"Inventory {inventory_reference} not found"

        if isinstance(inventory, list):
            if object_name in [inventory[i].name for i in range(len(inventory))]:
                inventory.remove(object_name)
        elif isinstance(inventory, dict):
            inventory.pop(object_name, None)
        else:
            try:
                inventory.remove(object_name)
            except:
                return f"Object {object_name} not found in {inventory_reference}"
        return f"Removed {object_name} from {inventory_reference}"
    
    # --- Refrences Management --- # 
    def get_reference(self, name):
        reference_object = self.helper.get_reference(name)
        if reference_object:
            return f"Found reference: {name}. Object data: {reference_object}"
        
    def create_reference(self, object_name, inventory_reference, set_reference):
        inventory = self.helper.get_reference(inventory_reference)
        if inventory == None:    
            return f"Inventory {inventory_reference} not found"
        found_object = self.helper.find_object(object_name, inventory, set_reference)
        if found_object:
            self.helper.create_reference(object_name, found_object)
            return f"Created reference: {object_name} for {found_object}"
        else:
            return f"Could not find object {object_name} in {inventory_reference}"

    def create_location_reference(self, location_path, set_reference):
        if '.' in location_path:
            location_path = self.helper.get_reference(location_path)
            if location_path == None:
                return f"Reference {location_path} not found"
        location = self.helper.get_location(location_path)
        if location == None:
            return f"Location {location_path} not found"
        self.helper.create_reference(set_reference, location)
        return f"Created reference: {set_reference} for {location_path}"

    def list_references(self):
        return str(list(self.references.keys()))
            
    def remove_reference(self, name):
        self.references.pop(name, None)
        return f"Removed reference: {name}"
    
    def clear_references(self):
        self.references.clear()
        return "Cleared all references" 
                         
    # --- Player and NPC Interactions --- #
    def action_time(self, entity_reference, time):
        entity = self.helper.get_reference(entity_reference)
        if entity == None:
            return f"entity {entity_reference} not found"
        return f"Entity {entity.name} took {time} seconds to complete the action"
    
    def add_status_effect(self, entity_reference, effect):
        entity = self.helper.get_reference(entity_reference)
        if entity == None:
            return f"entity {entity_reference} not found"
        return f"Added status effect {effect} to {entity.name}"
    
    def remove_status_effect(self, entity_reference, effect):
        entity = self.helper.get_reference(entity_reference)
        if entity == None:
            return f"entity {entity_reference} not found"
        return f"Removed status effect {effect} from {entity.name}"
    
    def entity_action(self, entity_reference, action):
        entity = self.helper.get_reference(entity_reference)
        if entity == None:
            return f"entity {entity_reference} not found"
        return f"entity {entity.name} performed action: {action}"
    
    def npc_memory_update(self, npc_reference, memory):
        npc = self.helper.get_reference(npc_reference)
        if npc == None:
            return f"npc {npc_reference} not found"
        return f"NPC {npc.name} updated memory: {memory}"
    
    def move_entity(self, entity_reference, location_path):
        entity = self.helper.get_reference(entity_reference)
        location = self.helper.get_reference(location_path)
        if entity == None:
            return f"entity {entity_reference} not found"
        if location == None:
            return f"location {location_path} not found"
        entity.location = location_path
        return f"Moved {entity.name} to {location.name}"
    
    # --- Notes and logging --- #
    def update_player_notes(self, player_reference, notes):
        player = self.helper.get_reference(player_reference)
        if player == None:
            return f"player {player_reference} not found"
        return f"Updated {player} notes: {notes}"
    
    def log_event(self, event, **kwargs):
        return f"Logged event: {event}"

class HelperFunctions():
    
    def __init__(self, parent) -> None:
        self.parent = parent
    
    def find_object(self, object_name, location, set_reference = None):
        found_object = None
        if isinstance(location, Inventory):
            found_object = location.get_item_slot(item_name = object_name).item
        elif isinstance(location, list):
            for i in location:
                if i.name.lower().replace(' ', '_') == object_name.lower().replace(' ', '_'):
                    found_object = i
        elif isinstance(location, dict):
            found_object = self.find_object(object_name, list(location.values()))
        else:
            try:
                found_object = self.find_object(object_name, list(location))
            except:
                pass
        
        if set_reference:
            self.create_reference(set_reference, found_object)
            
        return found_object
    
    def get_location(self, location_path):
        if location_path.split('/')[0] != 'world_map':
            return None
        location = self.parent.project_model.world.world_map
        for i in location_path.split('/')[1:]:
            location = self.find_object(i, location.locations)
        return location

    # --- Reference Management --- #
    def create_reference(self, name, entity):
        self.parent.references[name] = entity
    
    def get_reference(self, name):
        referene_object = None
        if '.' in name:
            name = name.split('.')
            if '/' in name[0]:
                referene_object = self.get_location(name[0])
            else:
                referene_object = self.parent.references.get(name[0], None)
            if referene_object == None:
                return None
            for i in name[1:]:
                referene_object = getattr(referene_object, i, None)
                if referene_object == None:
                    return None
        elif '/' in name:
            referene_object = self.get_location(name)
        else:
            referene_object = self.parent.references.get(name, None)
                  
        return referene_object
    
    def remove_reference(self, name):
        self.parent.references.pop(name, None)
    
    def clear_references(self):
        self.parent.references.clear()
