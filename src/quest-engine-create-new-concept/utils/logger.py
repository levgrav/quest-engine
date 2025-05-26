import re

class Log:
    def __init__(self, log_file):
        self.log_file = log_file

    def clear_log(self):
        with open(self.log_file, "w") as file:
            file.write("")
    
    def log(self, message):
        with open(self.log_file, "a") as file:
            file.write(message + "\n")

    def read_log(self):
        with open(self.log_file, "r") as file:
            return file.read()
        
    