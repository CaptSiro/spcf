from cli.arg import Arg
from abc import ABC, abstractmethod



class Command(ABC):
    @abstractmethod
    def get_cmd(self) -> str:
        ...

    @abstractmethod
    def get_help(self) -> str:
        ...

    @abstractmethod
    def execute(self, arg: Arg) -> None:
        ...



class CompoundCommand(Command, ABC):
    def __init__(self):
        self.cmds = CommandRegistry()
        self.register(self.cmds)

    @abstractmethod
    def register(self, commands):
        ...

    def get_subcommands(self) -> "CommandRegistry":
        return self.cmds



class CommandRegistry:
    def __init__(self):
        self.registry: dict[str, Command|CommandRegistry] = dict()
        self.default: Command|None = None

    def register(self, command: Command) -> None:
        if command.get_cmd() == "help":
            print("Error: Cannot register 'help', because it is reserved!")
            exit(1)

        if isinstance(command, CompoundCommand):
            cmds = command.get_subcommands()
            if cmds is None:
                print("Warning: Compound command '%s' has not returned any sub commands. Thus it will not be accessible" % command.get_cmd())
                return

            self.registry[command.get_cmd()] = cmds
            return

        self.registry[command.get_cmd()] = command

    def register_default(self, command: Command) -> None:
        self.default = command

    def generate_help(self, builder: str = "", depth = 0) -> str:
        for c in self.registry:
            builder += "    " * depth
            builder += c
            builder += "\n"

            if isinstance(self.registry[c], Command):
                builder += "    " * (depth + 1)
                h = self.registry[c].get_help()

                if h is None:
                    builder += "No documentation"
                else:
                    builder += h

                builder += "\n"
                continue

            builder = self.registry[c].generate_help(builder, depth + 1)

        return builder

    def execute(self, arg: Arg) -> None:
        literal = arg.shift()
        if literal is None:
            if self.default is None:
                print(self.generate_help())
                return

            self.default.execute(arg)
            return

        if literal == 'help':
            print(self.generate_help())
            return

        if literal not in self.registry:
            print("Error: Unknown command <%s>" % literal)
            exit(1)

        self.registry[literal].execute(arg)