"""The entry point of the bot"""

# pylint: disable=C0103

import sys
import commands
import discord

prefix = "?"
client = discord.Client()
cmds = commands.Commands()

@client.event
async def on_ready():
    """Runs when the bot logged in."""
    print("Logged in:")
    print(client.user.name)
    print(client.user.id)


@client.event
async def on_message(message):
    """Runs when a chat message is posted."""
    if message.content.split(" ")[0].startswith(prefix):
        executed = cmds.execute(message.content[len(prefix):])
        if executed is not None:
            is_embed = executed[0]
            msg = executed[1]
            if is_embed:
                await client.send_message(message.channel, embed=msg)
            else:
                await client.send_message(message.channel, msg)

if len(sys.argv) != 2:
    print("Usage: python bot.py token")
    sys.exit(1)
token = sys.argv[1]
client.run(token)
