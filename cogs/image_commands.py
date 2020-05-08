import discord
import json
import asyncio
import os
import random
from datetime import datetime
from discord.ext import commands


commands_data = {}

for filename in os.listdir('data/image_commands'):
    if filename.endswith('.json'):
        with open('data/image_commands/' + filename) as json_file:
            json_content = json.load(json_file)
            commands_data[filename[:-5]] = json_content

class image_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @commands.command(
        name = 'testmdma',
        description = "Detailed guide to reagent testing MDMA",
        aliases = commands_data['testmdma']['aliases']    
        )
    async def testmdma(self, ctx):
        await ctx.send(file = discord.File(commands_data['testmdma']['image']))

    


    @commands.command(
        name = 'testcoke',
        description = "Detailed guide to reagent testing cocaine",
        aliases = commands_data['testcoke']['aliases']
    )
    async def testcoke(self, ctx):
        await ctx.send(file = discord.File(commands_data['testcoke']['image']))

    


    @commands.command(
        name = 'testlsd',
        description = "Detailed guide to reagent testing LSD",
        aliases = commands_data['testlsd']['aliases']
    )
    async def testlsd(self, ctx):
        await ctx.send(file = discord.File(commands_data['testlsd']['image']))




    @commands.command(
        name = 'fent',
        description = "Detailed guide to using fentanyl test strips",
        aliases = commands_data['fent']['aliases']
    )
    async def fent(self, ctx):
        await ctx.send(file = discord.File(commands_data['fent']['image']))




    @commands.command(
        name = 'breathe',
        description = "Breathing gifs"
    )
    async def breathe(self, ctx):
        await ctx.send(file = discord.File(random.choice(commands_data['breathe']['image'])))

    


    @commands.command(
        name = 'recovery',
        description = "Recovery position",
        aliases = commands_data['recovery']['aliases']
    )
    async def recovery(self, ctx):
        await ctx.send(file = discord.File(commands_data['recovery']['image']))



    @commands.command(
        name = 'combochart',
        description = "TripSit Combochart",
        aliases = commands_data['combochart']['aliases']
    )
    async def combochart(self, ctx):
        await ctx.send(file = discord.File(commands_data['combochart']['image']))


def setup(bot):
    bot.add_cog(image_commands(bot))