import os
import json

class User_Functions:

    def __init__(self, project_model) -> None:
        self.project_model = project_model

    def create_project(self, name, author):
        if not name:
            return "Please enter a project name"

        project_path = os.path.join(self.project_model.parent_dir, name)

        if os.path.exists(project_path):
            return f"Project {name} already exists"

        # Create the directory structure
        os.makedirs(os.path.join(project_path, "world", "locations"))
        os.makedirs(os.path.join(project_path, "world", "routes"))
        os.makedirs(os.path.join(project_path, "npcs", "template"))
        os.makedirs(os.path.join(project_path, "npcs", "custom"))
        os.makedirs(os.path.join(project_path, "items", "template"))
        os.makedirs(os.path.join(project_path, "items", "custom"))

        # Create the main project JSON file
        project_json = {
            "name": name,
            "author": author,
            "settings": {}
        }
        with open(os.path.join(project_path, f"{name}.json"), "w") as f:
            json.dump(project_json, f, indent=4)

        return f"Project {name} created"

    def delete_project(self, name):
        project_path = os.path.join(self.project_model.parent_dir, name)
        if not os.path.exists(project_path):
            return f"Project {name} does not exist"
        self.remove_directory_absolute(project_path)
        return f"Project {name} deleted"

    def list_projects(self):
        return str(os.listdir(self.project_model.parent_dir))

    def create_location(self, project_name, location_name, description="", properties=None):
        if properties is None:
            properties = {}

        location_path = os.path.join(self.project_model.parent_dir, project_name, "world", "locations")
        if not os.path.exists(location_path):
            return f"Project {project_name} does not exist"

        location_file = os.path.join(location_path, f"{location_name}.json")
        if os.path.exists(location_file):
            return f"Location {location_name} already exists"

        location_data = {
            "name": location_name,
            "description": description,
            "other_properties": properties
        }
        with open(location_file, "w") as f:
            json.dump(location_data, f, indent=4)

        return f"Location {location_name} created"

    def create_npc(self, project_name, npc_name, npc_type="template", **kwargs):
        if npc_type not in ["template", "custom"]:
            return "NPC type must be 'template' or 'custom'"

        npc_path = os.path.join(self.project_model.parent_dir, project_name, "npcs", npc_type)
        if not os.path.exists(npc_path):
            return f"Project {project_name} does not exist"

        npc_file = os.path.join(npc_path, f"{npc_name}.json")
        if os.path.exists(npc_file):
            return f"NPC {npc_name} already exists"

        npc_data = {
            "name": npc_name,
            "description": kwargs.get("description", ""),
            "attributes": kwargs.get("attributes", []),
            "skills": kwargs.get("skills", []),
            "status_effects": kwargs.get("status_effects", []),
            "inventory": kwargs.get("inventory", []),
            "current_location": kwargs.get("current_location", ""),
            "notes": kwargs.get("notes", "")
        }
        with open(npc_file, "w") as f:
            json.dump(npc_data, f, indent=4)

        return f"NPC {npc_name} created"

    def create_item(self, project_name, item_name, item_type="template", **kwargs):
        if item_type not in ["template", "custom"]:
            return "Item type must be 'template' or 'custom'"

        item_path = os.path.join(self.project_model.parent_dir, project_name, "items", item_type)
        if not os.path.exists(item_path):
            return f"Project {project_name} does not exist"

        item_file = os.path.join(item_path, f"{item_name}.json")
        if os.path.exists(item_file):
            return f"Item {item_name} already exists"

        item_data = {
            "name": item_name,
            **kwargs
        }
        with open(item_file, "w") as f:
            json.dump(item_data, f, indent=4)

        return f"Item {item_name} created"

    def create_route(self, project_name, route_name, endpoints, distance, description="", properties=None):
        if properties is None:
            properties = {}

        route_path = os.path.join(self.project_model.parent_dir, project_name, "world", "routes")
        if not os.path.exists(route_path):
            return f"Project {project_name} does not exist"

        route_file = os.path.join(route_path, f"{route_name}.json")
        if os.path.exists(route_file):
            return f"Route {route_name} already exists"

        route_data = {
            "name": route_name,
            "endpoints": endpoints,
            "distance": distance,
            "description": description,
            "other_properties": properties
        }
        with open(route_file, "w") as f:
            json.dump(route_data, f, indent=4)

        return f"Route {route_name} created"

    def list_files(self, project_name, path):
        full_path = os.path.join(self.project_model.parent_dir, project_name, path)
        if not os.path.exists(full_path):
            return f"Path {path} does not exist in project {project_name}"

        return str(os.listdir(full_path))
