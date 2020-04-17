import discord
import json
import asyncio
import os
import random
from datetime import datetime
from discord.ext import commands


commands_data = {}

for filename in os.listdir('data/static_embeds'):
    if filename.endswith('.json'):
        with open('data/static_embeds/' + filename) as json_file:
            json_content = json.load(json_file)
            commands_data[filename[:-5]] = json_content

class static_embeds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def embed(self, command: str, channel: discord.TextChannel):
        data = commands_data[command]
        embed = discord.Embed(
                title = data['title'],
                colour = 0x7289da,
                timestamp = datetime.utcnow()
        )

        if 'fields' in data:
            for field in data['fields']:
                embed.add_field(name = field[0], value = field[1], inline = field[2])

        if 'footer' in data:
            if 'footer_thumbnail' in data:
                embed.set_footer(text = data['footer'], icon_url = data['footer_thumbnail'])
            else:
                embed.set_footer(text = data['footer'])
        else:
            embed.set_footer(text = "Please use drugs responsibly")
            
        if 'image' in data:
            embed.set_image(url = data['image'])
        
        if 'thumbnail' in data:
            embed.set_thumbnail(url = data['thumbnail'])
        
        asyncio.ensure_future(channel.send(embed = embed))


    @commands.command(
        name = 'badtrip',
        description = "Various grounding techniques and images"
    )
    async def badtrip(self, ctx):
        self.embed('badtrip', ctx.channel)


    @commands.command(
        name = 'resources',
        description = "List of various harm reduction related websites"
    )
    async def resources(self, ctx):
        self.embed('resources', ctx.channel)



    @commands.command(
        name = 'supps',
        description = "Various beneficial supplements",
        aliases = commands_data['supps']['aliases']
    )
    async def supps(self, ctx):
        self.embed('supps', ctx.channel)

    

    @commands.command(
        name = 'ala',
        description = "Information about alpha-lipoic acid"
    )
    async def ala(self, ctx):
        self.embed('ala', ctx.channel)



    @commands.command(
        name = 'alcar',
        description = "Information about acetyl-l-carnitine"
    )
    async def alcar(self, ctx):
        self.embed('alcar', ctx.channel)



    @commands.command(
        name = 'vitc',
        description = "Information about vitamin C"
    )
    async def vitc(self, ctx):
        self.embed('vitc', ctx.channel)



    @commands.command(
        name = 'hydration',
        description = "Information about staying hydrated when using MDMA"
    )
    async def hydration(self, ctx):
        self.embed('hydration', ctx.channel)



    @commands.command(
        name = 'ginger',
        description = "Information about ginger"
    )
    async def ginger(self, ctx):
        self.embed('ginger', ctx.channel)



    @commands.command(
        name = '5htp',
        description = "Information about 5-HTP",
        aliases = commands_data['5htp']['aliases']
    )
    async def htp(self, ctx):
        self.embed('5htp', ctx.channel)



    @commands.command(
        name = 'about',
        description = "About the bot"
    )
    async def about(self, ctx):
        self.embed('about', ctx.channel)



    @commands.command(
        name = 'triptoy',
        description = "Collection of various trippy websites"
    )
    async def triptoy(self, ctx):
        embed = discord.Embed(
            title = "Have a trip toy!",
            colour = 0x7289da,
            description = random.choice(commands_data['triptoy']['toys'])
        )
        asyncio.ensure_future(ctx.channel.send(embed = embed))
    


    @commands.command(
        name = 'ping',
        description = "Shows bot latency to websocket"
    )
    async def ping(self, ctx):
        ping = round(self.bot.latency * 1000, 2)
        embed = discord.Embed(
            title = "Ping: " + str(ping) + "ms",
            colour = 0x7289da
        )
        embed.set_author(name = "Bot websocket ping")
        embed.set_footer(text = "Not client ping")
        asyncio.ensure_future(ctx.channel.send(embed = embed))


def setup(bot):
    bot.add_cog(static_embeds(bot))