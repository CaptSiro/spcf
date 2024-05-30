import sys

from cli.arg import Arg
from cli.todo import todo
from cli.cmd import CommandRegistry



def init(cmds: CommandRegistry) -> None:
    todo("Add commands for cli application")



if __name__ == "__main__":
    commands = CommandRegistry()

    init(commands)
    commands.execute(Arg.parse(sys.argv))
