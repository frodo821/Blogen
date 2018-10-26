"""INTERNAL PACKAGE FOR USING THIS AS A STAND ALONE PROGRAM"""
from .command import (
    has_option,
    get_name,
    print_help,
    COMMANDS,
    CommandError,
    HelpCommand)
from .project import ProjectCommand
from .build import BuildCommand

h = HelpCommand()
ProjectCommand()
BuildCommand()

def main(args):
    """Main function"""
    args = list(args)
    if not args:
        raise CommandError(get_name(), "Command not specified.")
    if has_option(args, "-h", "-?", "--help"):
        if not args:
            return print_help()
        cmd = COMMANDS.get(args[0], None)
        if cmd is None:
            print(f"Unknown command: {args[0]}")
            return print_help()
        print(f"{args[0]}:")
        for l in cmd.summaries:
            print(f"    {l}")
        return
    cmd = COMMANDS.get(
        list(filter(lambda x: not x.startswith("-"), args))[0], h)
    cmd.main(args[1:])
