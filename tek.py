import json
import logging

import discord
from discord.ext import commands

with open('config.json', 'r') as readable:
    json_content = json.loads(readable.read())

with open('auth.json', 'r') as readable:
    auth_content = json.loads(readable.read())

bot = commands.Bot(
    command_prefix = json_content['prefix'],
    description = json_content['description'] + json_content['version'],
    owner_id = json_content['owner_id'],
    case_insensitive = True
)

logging.basicConfig(level = logging.INFO)


@bot.event
async def on_ready():
    print("discord.py v" + discord.__version__)

    bot.remove_command('help')

    for cog in json_content['cogs']:
        bot.load_extension(cog)

    await bot.change_presence(activity = discord.Game(name = ".help on v" + json_content['version']))

    print("Ready")
    return


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        if not ctx.message.content.startswith('..'):
            cmd = ctx.message.content[1:]
            embed = discord.Embed(
                title = "Error - Command '{}' not found".format(cmd),
                color = 0x7289da
            )
            await ctx.message.channel.send(embed = embed, delete_after = 5)
            return


bot.run(auth_content['token'])
