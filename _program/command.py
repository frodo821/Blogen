"""defininition of base command"""
from typing import Dict

def has_option(args, *alias):
    """option is included to command-line arguments?"""
    return any(list((option in args and args.remove(option)) is None for option in alias))

def get_name():
    """returns called module name"""
    if "__package__" in globals():
        return __package__.split(".")[0]
    return __name__

def print_help():
    """Print help messages"""
    print(f"Usage: {get_name()} COMMAND ARGS...")
    print("Generate HTML and article indices from markdown source and template HTML.")
    print()
    print("Datail of each commands:")
    for k, v in COMMANDS.items():
        print(f"    {k}:")
        for l in v.summaries:
            print(f"        {l}")

class Command:
    """The basis of all commands"""
    def __init__(self, name):
        self.__name__ = name
        COMMANDS[name] = self

    @property
    def summaries(self):
        """This property is expected to return an iterator or this being a generator."""
        yield "The basis of all commands."

    def main(self, args):
        """The main function of this command."""
        pass

class CommandError(Exception):
    """The basis of all exceptions which is related to Command"""
    def __init__(self, command, reason):
        super().__init__()
        self.command = command
        self.reason = reason

    def __str__(self):
        if not self.command:
            return f"CommandError: {self.reason}"
        return f"CommandError: {self.reason}: {self.command}"

    def __repr__(self):
        return str(self)

class UnknownCommandError(CommandError):
    """This will be thrown when the command is unknown."""
    def __init__(self, command):
        super().__init__(command, "Unknown command")

class UnsatisfiableArgumentError(CommandError):
    """This will be thrown when command count is invalid."""
    def __init__(self, command, wrong, actual):
        super().__init__(command, (
            "Invalid number of commands are passed."
            f" Expected {actual}, but {wrong}"))

class HelpCommand(Command):
    def __init__(self):
        super().__init__("help")

    @property
    def summaries(self):
        yield "This command only shows this help message."

    def main(self, args):
        print_help()

COMMANDS: Dict[str, Command] = {}
