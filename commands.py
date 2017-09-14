"""Module for the commands for ChessBot"""

import openings

class Commands():
    """Commands for ChessBot"""
    def __init__(self):
        self.openings = openings.Openings("eco/eco.json")
        self.commands = {"opening": self.opening, "commands": self.cmds, "help": self.help}

    def execute(self, cmd):
        """Executes a command from chat."""
        split = cmd.split(" ", 1)
        name = split[0]
        if len(split) > 1:
            args = split[1]
        else:
            args = ""
        if name in self.commands:
            return self.commands[name](args)
        return None

    def opening(self, args):
        """`opening` command"""
        found = self.openings.closest_match(args)
        if found is None:
            return "No matching opening found."
        return "**{0} {1}**. Moves: `{2}`. Board: <https://lichess.org/analysis/{3}>"\
            .format(found.eco, found.name, found.as_pgn_moves(), found.fen.replace(" ", "_"))

    def cmds(self, _):
        """`commands` command"""
        return "Commands: {}".format(", ".join(
            sorted(map(lambda x: "`" + x + "`", self.commands.keys()))
        ))

    def help(self, _):
        """`help` command"""
        return "Hello! I'm a bot, created by ProgramFOX. Use `commands` to see what I can do!"
