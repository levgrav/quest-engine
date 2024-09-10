import os


class Gpt_Functions:

    sys_args = {}

    @staticmethod
    def remove_directory_absolute(path):
        try:
            os.rmdir(path)
        except OSError as e:
            for root, dirs, files in os.walk(path, topdown=False):
                for name in dirs:
                    print(name)
                    Gpt_Functions.remove_directory_absolute(os.path.join(root, name))
                for name in files:
                    print(name)
                    os.remove(os.path.join(root, name))

            os.rmdir(path)

    @staticmethod
    def create_project(name):
        global project
        project = name
        if os.path.exists(f"{Gpt_Functions.sys_args['parent_dir']}/{name}"):
            return f"Project {name} already exists"
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/character_types")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/items")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/items/template")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/items/custom")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/npcs")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/npcs/template")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/npcs/custom")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/quests")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/world")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/world/features")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/world/locations")
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/world/routes")
        # creates files for each folder
        with open(
            f"{Gpt_Functions.sys_args['parent_dir']}/{name}/{name.lower().replace(' ', '_')}.json",
            "w",
        ) as f:
            f.write("{}")
        with open(f"{Gpt_Functions.sys_args['parent_dir']}/{name}/notes.txt", "w") as f:
            f.write("")
        with open(
            f"{Gpt_Functions.sys_args['parent_dir']}/{name}/world/world.json", "w"
        ) as f:
            f.write("{}")

        return f"Project {name} created"

    @staticmethod
    def delete_project(name=None):
        global project
        if project is None and name is None:
            return "Please create a project first"
        if name is None:
            Gpt_Functions.remove_directory_absolute(
                f"{Gpt_Functions.sys_args['parent_dir']}/{project}"
            )
            project = None
            return f"Project {project} deleted"
        else:
            if not os.path.exists(f"{Gpt_Functions.sys_args['parent_dir']}/{name}"):
                return f"Project {name} does not exist"
            Gpt_Functions.remove_directory_absolute(
                f"{Gpt_Functions.sys_args['parent_dir']}/{name}"
            )
            return f"Project {name} deleted"

    @staticmethod
    def list_projects():
        return (
            f"Projects in directory: {os.listdir(Gpt_Functions.sys_args['parent_dir'])}"
        )

    @staticmethod
    def change_project(name):
        global project
        if not os.path.exists(f"{Gpt_Functions.sys_args['parent_dir']}/{name}"):
            return f"Project {name} does not exist"
        project = name
        return f"Project changed to {name}"

    @staticmethod
    def create_file(name, content=""):
        if project is None:
            return "Please enter a project first"
        with open(f"{Gpt_Functions.sys_args['parent_dir']}/{project}/{name}", "w") as f:
            f.write(content)
        return f"File {name} created with content: {content}"

    @staticmethod
    def read_file(name):
        if project is None:
            return "Please enter a project first"
        with open(f"{Gpt_Functions.sys_args['parent_dir']}/{project}/{name}", "r") as f:
            content = f.read()
        return f"File {name} read with content: {content}"

    @staticmethod
    def append_file(name, content):
        if project is None:
            return "Please enter a project first"
        with open(f"{Gpt_Functions.sys_args['parent_dir']}/{project}/{name}", "a") as f:
            f.write(content)
        return f"File {name} appended with content: {content}"

    @staticmethod
    def delete_file(name):
        if project is None:
            return "Please enter a project first"
        os.remove(f"{Gpt_Functions.sys_args['parent_dir']}/{project}/{name}")
        return f"File {name} deleted"

    @staticmethod
    def list_files(
        path,
    ):  # list files and folders and contents of folders (recursively)
        if project is None:
            return "Please enter a project first"
        return f"Files in directory: {os.listdir(f'{Gpt_Functions.sys_args["parent_dir"]}/{project}/{path}')}"

    @staticmethod
    def create_folder(name):
        if project is None:
            return "Please enter a project first"
        if os.path.exists(f"{Gpt_Functions.sys_args['parent_dir']}/{project}/{name}"):
            return f"Folder {name} already exists"
        os.mkdir(f"{Gpt_Functions.sys_args['parent_dir']}/{project}/{name}")
        return f"Folder {name} created"

    @staticmethod
    def delete_folder(name):
        if project is None:
            return "Please enter a project first"
        Gpt_Functions.remove_directory_absolute(
            f"{Gpt_Functions.sys_args['parent_dir']}/{project}/{name}"
        )
        return f"Folder {name} deleted"

    @staticmethod
    def quit_program():
        global done
        done = True
        return "Goodbye!"
