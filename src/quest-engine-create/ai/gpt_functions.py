import os


class Gpt_Functions:

    def __init__(self, project_model) -> None:
        self.project_model = project_model

    def remove_directory_absolute(self, path):
        try:
            os.rmdir(path)
        except OSError as e:
            for root, dirs, files in os.walk(path, topdown=False):
                for name in dirs:
                    print(name)
                    self.remove_directory_absolute(os.path.join(root, name))
                for name in files:
                    print(name)
                    os.remove(os.path.join(root, name))

            os.rmdir(path)

    def create_project(self, name):
        self.project_model.project_name = name
        if os.path.exists(f"{self.project_model.parent_dir}/{name}"):
            return f"Project {name} already exists"
        os.mkdir(f"{self.project_model.parent_dir}/{name}")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/character_types")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/items")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/items/template")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/items/custom")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/npcs")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/npcs/template")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/npcs/custom")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/quests")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/world")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/world/features")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/world/locations")
        os.mkdir(f"{self.project_model.parent_dir}/{name}/world/routes")
        # creates files for each folder
        with open(
            f"{self.project_model.parent_dir}/{name}/{name.lower().replace(' ', '_')}.json",
            "w",
        ) as f:
            f.write("{}")
        with open(f"{self.project_model.parent_dir}/{name}/notes.txt", "w") as f:
            f.write("")
        with open(f"{self.project_model.parent_dir}/{name}/world/world.json", "w") as f:
            f.write("{}")

        return f"Project {name} created"

    def delete_project(self, name=None):
        if not self.project_model.is_project_open and name is None:
            return "Please create a project first"

        if name is None:
            self.remove_directory_absolute(
                f"{self.project_model.parent_dir}/{self.project_model.project_name}"
            )
            self.project_model.project_name = None
            return f"Project {self.project_model.project_name} deleted"
        else:
            if not os.path.exists(f"{self.project_model.parent_dir}/{name}"):
                return f"Project {name} does not exist"
            self.remove_directory_absolute(f"{self.project_model.parent_dir}/{name}")
            return f"Project {name} deleted"

    def list_projects(
        self,
    ):
        print("list_projects")
        return f"Projects in directory: {os.listdir(self.project_model.parent_dir)}"

    def change_project(self, name):
        if not os.path.exists(f"{self.project_model.parent_dir}/{name}"):
            return f"Project {name} does not exist"
        self.project_model.project_name = name
        return f"Project changed to {name}"

    def create_file(self, name, content=""):
        if not self.project_model.is_project_open:
            return "Please enter a project first"

        with open(
            f"{self.project_model.parent_dir}/{self.project_model.project_name}/{name}",
            "w",
        ) as f:
            f.write(content)
        return f"File {name} created with content: {content}"

    def read_file(self, name):
        if not self.project_model.is_project_open:
            return "Please enter a project first"

        with open(
            f"{self.project_model.parent_dir}/{self.project_model.project_name}/{name}",
            "r",
        ) as f:
            content = f.read()
        return f"File {name} read with content: {content}"

    def append_file(self, name, content):
        if not self.project_model.is_project_open:
            return "Please enter a project first"

        with open(
            f"{self.project_model.parent_dir}/{self.project_model.project_name}/{name}",
            "a",
        ) as f:
            f.write(content)
        return f"File {name} appended with content: {content}"

    def delete_file(self, name):
        if not self.project_model.is_project_open:
            return "Please enter a project first"

        os.remove(
            f"{self.project_model.parent_dir}/{self.project_model.project_name}/{name}"
        )
        return f"File {name} deleted"

    def list_files(
        self,
        path,
    ):  # list files and folders and contents of folders (recursively)
        if not self.project_model.is_project_open:
            return "Please enter a project first"

        return f"Files in directory: {os.listdir(f'{self.project_model.parent_dor}/{self.project_model.project_name}/{path}')}"

    def create_folder(self, name):
        if not self.project_model.is_project_open:
            return "Please enter a project first"

        if os.path.exists(
            f"{self.project_model.parent_dir}/{self.project_model.project_name}/{name}"
        ):
            return f"Folder {name} already exists"
        os.mkdir(
            f"{self.project_model.parent_dir}/{self.project_model.project_name}/{name}"
        )
        return f"Folder {name} created"

    def delete_folder(self, name):
        if not self.project_model.is_project_open:
            return "Please enter a project first"

        self.remove_directory_absolute(
            f"{self.project_model.parent_dir}/{self.project_model.project_name}/{name}"
        )
        return f"Folder {name} deleted"

    def quit_program(
        self,
    ):
        global done
        done = True
        return "Goodbye!"
