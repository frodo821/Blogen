"""Project command"""

from os import makedirs, getcwd
from os.path import exists, join, dirname
from shutil import copyfile as copy
from .command import Command, UnsatisfiableArgumentError, CommandError

class ProjectCommand(Command):
    """This command is to create a project."""
    def __init__(self):
        super().__init__("create")

    @property
    def summaries(self):
        yield "This command is used for creating a project."
        yield ""
        yield "Usage:"
        yield "    create PROJECT_NAME"

    def main(self, args):
        if len(args) != 1:
            raise UnsatisfiableArgumentError(self.__name__, len(args), 1)
        name = args[0]
        path = join(getcwd(), name)
        if exists(path):
            raise CommandError(
                self.__name__,
                ("Cannot create a project("
                 f"specified path '{path}' is already exists)"))
        makedirs(path)
        makedirs(join(path, "src"))
        copy(join(dirname(__file__), "resources", "config.txt"), join(path, "config.py"))
        print(f"Created new project '{name}'")
        print(f"Your project folder is '{path}'")
        print(f"To build this project, please execute build command in project folder.")
