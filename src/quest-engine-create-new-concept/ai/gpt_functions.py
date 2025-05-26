import os
import json 
from utils.utils import is_json
from typing import Optional, overload

class Gpt_Functions:

    def __init__(self, project_model) -> None:
        self.project_model = project_model

    def evaluate(self, call: dict):
        return self.__getattribute__(call['function']['name'])(**json.loads(call['function']['arguments']))

    def remove_directory_absolute(self, path):
        try:
            os.rmdir(path)
        except OSError as e:
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    self.remove_directory_absolute(os.path.join(root, name))
            os.rmdir(path)

    def create_project(self, name, author):
        if not name:
            return "Please enter a project name"

        project_path = os.path.join(self.project_model.parent_dir, name)
        template_path = "files/template_files"

        if os.path.exists(project_path):
            return f"Project {name} already exists"

        # Create the directory structure
        os.makedirs(project_path)
        os.makedirs(os.path.join(project_path, "objects"))
        os.makedirs(os.path.join(project_path, "objects", "characters"))
        os.makedirs(os.path.join(project_path, "objects", "world"))
        
        templates = {}
        for filename in os.listdir(template_path):
            with open(os.path.join(template_path, filename), "r") as f:
                templates[filename[:-5]] = f.read()

        for path in [
            "objects/characters/character.json",
            "objects/characters/player.json",
            "objects/world/item.json",
            "objects/world/location.json",
            "objects/world/object.json",
            "world.json"
        ]: 
            with open(os.path.join(project_path, path), "w") as f:
                f.write(templates[path.split("/")[-1][:-5]])

        return f"Project {name} created"

    def delete_project(self, name):
        project_path = os.path.join(self.project_model.parent_dir, name)
        if not os.path.exists(project_path):
            return f"Project {name} does not exist"
        self.remove_directory_absolute(project_path)
        return f"Project {name} deleted"

    def list_projects(self):
        return str(os.listdir(self.project_model.parent_dir))

    def list_files(self, project_name, path):
        full_path = os.path.join(self.project_model.parent_dir, project_name, path)
        if not os.path.exists(full_path):
            return f"Path {path} does not exist in project {project_name}"

        return str(os.listdir(full_path))
    
    def get_file_content(self, project_name, file_path):
        full_path = os.path.join(self.project_model.parent_dir, project_name, file_path)
        if not os.path.exists(full_path):
            return f"File {file_path} does not exist in project {project_name}"

        with open(full_path, "r") as f:
            return f.read()
    
    def set_file_content(self, project_name, file_path, content):
        full_path = os.path.join(self.project_model.parent_dir, project_name, file_path)
        if not os.path.exists(full_path):
            return f"File {file_path} does not exist in project {project_name}"

        with open(full_path, "w") as f:
            f.write(content)
            return f"Write to file successful"
    
    def add_property(self, project_name: str, file_path: str, value: str, name: Optional[str], path: Optional[str]):
        content = self.get_file_content(project_name ,file_path)
        if not is_json(content): return "File is not json"
        content = json.loads(content)
        property_location = content["properties"]

        if path != None:
            path = path.split("/")
            for namespace in path:
                for item in property_location:
                    if isinstance(item, list) and isinstance(item[1], list) and item[0] == namespace:
                        property_location = item[1]
        
        if name != None:
            value = [name, value]
        
        property_location.append(value)
        self.set_file_content(project_name, file_path, json.dumps(content, indent=4))
    
    @overload
    def remove_property(self, project_name: str, file_path: str, value: str, path: Optional[str]): "removes the unnamed property with the exact value specified"
    @overload
    def remove_property(self, project_name: str, file_path: str, index: str, path: Optional[str]): "removes the property at given index"
    @overload
    def remove_property(self, project_name: str, file_path: str, name: str, path: Optional[str]): "removes the first named property wih a given name"
    @overload
    def remove_property(self, project_name: str, file_path: str, name: str, value: str, path: Optional[str]): "removes the named property with a given name and value"
    
    def remove_property(self, project_name: str, file_path: str, name: Optional[str], value: Optional[str], index: Optional[str], path: Optional[str]):
        content = self.get_file_content(project_name ,file_path)
        if not is_json(content): return "File is not json"
        content = json.loads(content)
        property_location = content["properties"]

        if path != None:
            path = path.split("/")
            for namespace in path:
                for item in property_location:
                    if isinstance(item, list) and isinstance(item[1], list) and item[0] == namespace:
                        property_location = item[1]
                        break
        
        if value:
            if name:
                value = [name, value]
            if value in property_location:
                property_location.remove(value)
            else:
                return f"value {value} not found"
        
        elif name:
            for item in property_location:
                if isinstance(item, list) and isinstance(item[1], str) and item[0] == name:
                    property_location.remove(item)
                    break
        elif index:
            if not index.isdigit():
                return "index must be an integer string"
            index = int(index)
            property_location.pop(index)
        else:
            return "required parameters not specified"
        
        return "Succesfull removal"
    
    def get_properties(self, project_name: str, file_path: str, path: Optional[str]):
        content = self.get_file_content(project_name ,file_path)
        if not is_json(content): return "File is not json"
        content = json.loads(content)
        property_location = content["properties"]

        if path != None:
            path = path.split("/")
            for namespace in path:
                for item in property_location:
                    if isinstance(item, list) and isinstance(item[1], list) and item[0] == namespace:
                        property_location = item[1]
                        break
        
        return property_location
    
    def add_relation(self, project_name: str, file_path: str, id: str, relation: str, path: Optional[str]):
        ...

    def remove_relation(self, project_name: str, file_path: str, id: str, relation: str, path: Optional[str]):
        ...
    
    def get_relations(self, project_name: str, file_path: str, id: str, path: Optional[str]):
        ...

    def edit_data(self, project_name: str, file_path: str, key: str, value: str):
        content = self.get_file_content(project_name ,file_path)
        if not is_json(content): return "File is not json"
        content = json.loads(content)
        content[key] = value
        self.set_file_content(project_name, file_path, json.dumps(content, indent=4))