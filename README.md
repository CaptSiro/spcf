# SPCF
Simple Python CLI Framework

## Usage

### Create a simple echo command

```python
from cli.arg import Arg
from cli.cmd import Command
```

Import Arg class and Command class

```python
class EchoCommand(Command):
    def get_cmd(self) -> str:
        # return how the command will be called:
        #   ./program echo [args...]
        return "echo"

    def get_help(self) -> str:
        # function provides information about command and it will be called when program has help argument
        return "Prints first argument to stdout. If -h is set, it will print in hexadecimal format"

    def execute(self, arg: Arg) -> None:
        # get first argument after echo
        a = arg.shift()

        # check if 'h' has been set
        if 'h' in arg.flags:
            for c in a:
                print("%02x " % c, end='')
        else:
            print(a)
```

Implementation of abstract Command methods

### Create a complex list command

```python
from cli.arg import Arg
from cli.cmd import CompoundCommand, CommandRegistry, Command
```

Import Arg class and needed Command classes

```python
class ListCommand(CompoundCommand):
    def __init__(self):
        # must call __init__ of CompoudCommand
        super().__init__()

    def register(self, commands: CommandRegistry):
        # register sub commands

        # default is called if no other arguments follow current command
        # example: ./program list
        # when default is unset, generation of help for sub command is used
        commands.register_default(self)

        # register sub commands (implementation of ListAddCommand is explained later on)
        commands.register(ListAddCommand())

    def get_cmd(self) -> str:
        return "list"

    def get_help(self) -> str:
        return "Help for list"

    def execute(self, arg: Arg) -> None:
        # custom default behavior handler
        pass
```

Implementation of custom CompoundCommand with definition of default behaviour

```python
class ListAddCommand(Command):
    def get_cmd(self) -> str:
        return "add"

    def get_help(self) -> str:
        return "Help for list add"

    def execute(self, arg: Arg) -> None:
        # command behaviour

        # get following argument and print it
        item = arg.shift()
        if item is None:
            print("You need to specify item to be added")
            exit(1)

        print("Adding '%s' to list" % item)
```

Implementation of simple sub command for list add
