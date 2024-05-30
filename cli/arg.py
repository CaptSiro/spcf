import re



class Arg:
    def __init__(self, program: str, vec: list[str], flags: dict[str, None|str]):
        self.program = program
        self.vec: list[str] = vec
        self.flags = flags

    def shift(self) -> str|None:
        if len(self.vec) == 0:
            return None

        return self.vec.pop(0)

    @staticmethod
    def parse(args: [str]) -> "Arg":
        program = args.pop(0)
        flag_regex = r"(?:^-([^\s\-=]+)$)|(?:^--([^\s=]+)(?:=(\S+))?$)"
        flags = dict()
        vec = []

        for arg in args:
            matches = re.search(flag_regex, arg)
            if matches is None:
                vec.append(arg)
                continue

            if matches.group(1) is not None:
                for char in matches.group(1):
                    flags[char] = None
                continue

            flags[matches.group(2)] = matches.group(3)

        return Arg(program, vec, flags)