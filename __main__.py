"""main"""
from sys import argv
from ._program import main
from ._program.command import CommandError

try:
    main(argv[1:])
except CommandError as e:
    if e.command is None:
        print(f"{e.reason}")
    else:
        print(f"{e.command}: {e.reason}")
