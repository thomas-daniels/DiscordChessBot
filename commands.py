"""Module for the commands for ChessBot"""

import openings
import discord

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
            return (False, "No matching opening found.")
        embed = discord.Embed()
        embed.title = found.eco + " " + found.name
        embed.description = "https://lichess.org/analysis/" + found.fen.replace(" ", "_")
        embed.colour = discord.Colour.dark_gold()
        embed.set_footer(text=found.as_pgn_moves())
        return (True, embed)

    def cmds(self, _):
        """`commands` command"""
        return (False, "Commands: {}".format(", ".join(
            sorted(map(lambda x: "`" + x + "`", self.commands.keys()))
        )))

    def help(self, _):
        """`help` command"""
        return (False, "Hello! I'm a bot, created by ProgramFOX. Use `commands` to see what I can do!")
