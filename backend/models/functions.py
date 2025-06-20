import json
import os
from typing import Optional, overload
from ..utils.file_ops import is_json
from .game import GameObject

class GptFunctions:
    def __init__(self, game_state):
        self.game_state = game_state

    def evaluate(self, call: dict):
        try:
            result = self.__getattribute__(call['function']['name'])(**json.loads(call['function']['arguments']))
            return str(result)
        except Exception as e:
            return str(e)

class PlayFunctions(GptFunctions):
    def list_objects(self):
        return list(self.game_state.game_objects.keys())

    def get_object_data(self, object_name):
        return self.game_state.game_objects[object_name]

    def update_object_data(self, object_name, data):
        self.game_state.game_objects[object_name].update(**data)
        return "Success"
    
    def remove_object(self, object_name):
        del self.game_state.game_objects[object_name]
        return "Success"

    def add_object(self, object_name, data):
        self.game_state.game_objects[object_name] = GameObject(**data)
        return "Success"

class CreateFunctions(GptFunctions):
    def explore(self):
        return self._explore_helper(self.project_model.parent_dir)

    def _explore_helper(self, path):
        disp_name = os.path.split(path)[-1]
        if os.path.isdir(path):
            items = os.listdir(path)
            return f"{disp_name} Folder contains files: {items}\n{"\n".join([self._explore_helper(os.path.join(path, item)) for item in items])}"
        elif os.path.isfile(path):
            with open(path, "r") as f:
                content = f.read()
                if is_json(content):
                    content = json.dumps(json.loads(content))
                return f"{disp_name} File contents: {content}" 
        else: return ""

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

    def list_dir(self, project_name, path):
        full_path = os.path.join(self.project_model.parent_dir, project_name, path)
        if not os.path.exists(full_path):
            return f"Path {path} does not exist in project {project_name}"

        listdir = os.listdir(full_path)
        folders = []
        files = []
        for elem in listdir:
            if os.path.isdir(elem): folders.append(elem)
            else: files.append(elem)

        return f"Folders: {folders}, Files: {files}"
    
    def get_file_content(self, project_name: str, file_path: str, as_dict: bool = False):
        full_path = os.path.join(self.project_model.parent_dir, project_name, file_path)
        if not os.path.exists(full_path):
            return f"File {file_path} does not exist in project {project_name}", False

        if os.path.isdir(full_path):
            return "Cannot open Folder as File", False

        with open(full_path, "r") as f:
            content = f.read()
            if not as_dict:
                return content, True
            elif is_json(content):
                return json.loads(content), True
            else:
                return "Content is not JSON", False
    
    def set_file_content(self, project_name, file_path, content):
        full_path = os.path.join(self.project_model.parent_dir, project_name, file_path)
        if not os.path.exists(full_path):
            return f"File {file_path} does not exist in project {project_name}"

        with open(full_path, "w") as f:
            f.write(content)
            return f"Write to file successful"
    
    def add_property(self, project_name: str, file_path: str, value: str, name: Optional[str], path: Optional[str]):
        content, success = self.get_file_content(project_name, file_path, True)
        if not success: return content
        
        property_location = path_location(content["properties"], path)
        if property_location == None:
            return "Invalid path"
        
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
        content, success = self.get_file_content(project_name ,file_path, True)
        if not success: return content
        
        property_location = path_location(content["properties"], path)
        if property_location == None:
            return "Invalid path"
        
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
        content, success = self.get_file_content(project_name ,file_path, True)
        if not success: return content
        property_location = path_location(content["properties"], path)
        if property_location == None:
            return "Invalid path"
        
        return property_location
    
    def add_relation(self, project_name: str, file_path: str, id: str, relation: str, path: Optional[str]):
        content, success = self.get_file_content(project_name, file_path, True)
        if not success: return content
        
        relation_location = path_location(content["relations"], path)
        if relation_location == None:
            return "Invalid path"
        
        relation_location.append([id, relation])
        return "Success"

    def remove_relation(self, project_name: str, file_path: str, id: str, relation: Optional[str], path: Optional[str]):
        content, success = self.get_file_content(project_name, file_path, True)
        if not success: return content
        
        relation_location = path_location(content["relations"], path)
        if relation_location == None:
            return "Invalid path"
        
        for id_relation in relation_location:
            if id_relation[0] == id and (id_relation[1] == relation or relation == None):
                relation_location.remove(id_relation)
            
        return "Success"
    
    def get_relations(self, project_name: str, file_path: str, id: str, path: Optional[str]):
        content, success = self.get_file_content(project_name, file_path, True)
        if not success: return content
        
        relation_location = path_location(content["relations"], path)
        if relation_location == None:
            return "Invalid path"
        
        return relation_location
    
    def add_namespace(self, project_name, file_path, category, path, name):
        content, success = self.get_file_content(project_name, file_path, True)
        if not success: return content

        namespace_location = path_location(content[category], path)
        if namespace_location == None:
            return "Invalid path"
        
        namespace_location.append([name, []])
            
        return "Success"        
    
    def remove_namespace(self, project_name, file_path, category, path, name):
        content, success = self.get_file_content(project_name, file_path, True)
        if not success: return content

        namespace_location = path_location(content[category], path)
        if namespace_location == None:
            return "Invalid path"
        
        for namespace in namespace_location:
            if namespace[0] == id and (namespace[1] == name or name == None):
                namespace_location.remove(namespace)
            
        return "Success"        

    def edit_data(self, project_name: str, file_path: str, key: str, value: str):
        content, success = self.get_file_content(project_name ,file_path, True)
        if not success: return content
        content[key] = value
        self.set_file_content(project_name, file_path, json.dumps(content, indent=4))

def path_location(location, path):
    if path != None:
        path = path.split("/")
        for namespace in path:
            for item in location:
                if isinstance(item, list) and isinstance(item[1], list) and item[0] == namespace:
                    location = item[1]
                    break
            else: return None
    return location

if __name__ == "__main__":
    p = PlayFunctions(0)
    print(p.evaluate({
        'function': {
            'name': 'ex_func',
            'arguments': '{"a": 1,"b": 2,"c": 3}'
        }
    }))