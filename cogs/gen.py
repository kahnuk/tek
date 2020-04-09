import discord
import json
from datetime import datetime
from discord.ext import commands
import requests
import random


class gen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        with open('data/gen.json', 'r') as readable:
                self.json_content = json.loads(readable.read())

        with open('config.json', 'r') as readable:
            self.json_config = json.loads(readable.read())

    async def embed(self, command: str, channel: discord.TextChannel):

        #Fill .JSON path information
        json_path = self.json_content[command]
        fields = json_path['fields']
        footer = json_path['footer']
        
        #Create embed object
        embed = discord.Embed(
            title = json_path['title'],
            colour = 0x7289da
        )

        #Fill an embed field for every array under the 'fields' object
        for field in fields:
            embed.add_field(name = field[0], value = field[1], inline = field[2])

        if footer:
            embed.set_footer(text = json_path['footer'])

        await channel.send(embed = embed)
        return



    @commands.command(
        name = 'about',
        description = "About the bot"
    )
    async def about(self, ctx):
        json_about = self.json_content['about']

        embed = discord.Embed(
            title = "Tek v" + self.json_config['version'],
            colour = 0x7289da
        )
        
        embed.add_field(name = json_about['fields'][0][0], value = json_about['fields'][0][1], inline = json_about['fields'][0][2])
        embed.set_thumbnail(url = json_about['body_thumbnail'])
        embed.set_footer(text = json_about['footer'][0], icon_url = json_about['footer'][1])

        await ctx.send(embed = embed)
        return



    @commands.command(
        name = 'ping',
        description = "Ping to check bot latency"
    )
    async def ping(self, ctx):
        ping = round(self.bot.latency * 1000, 2)

        embed = discord.Embed(
            title = "Ping: " + str(ping) + "ms",
            colour = 0x7289da
        )
        embed.set_footer(text = "Bot Ping")
        await ctx.send(embed = embed)
        return

    @commands.command(
        name = 'apod',
        description = "Pulls NASA APoD"
    )
    async def apod(self, ctx, *arg):
        url = 'https://api.nasa.gov/planetary/apod?api_key=' + self.json_config['apod_key']
        request = requests.get(url = url)
        data = request.json()

        embed = discord.Embed(
                title = data['title'],
                colour = 0x7289da,
                description = data['explanation']
            )

        if not arg:
            embed.add_field(name = "**NASA Astronomy Picture of the Day**", value = data['date'], inline = False)
            embed.set_image(url = data['url'])
            embed.set_footer(text = "© " + data['copyright'])

            await ctx.send(embed = embed)
            return

        if arg[0] == "description":
            print('triggered')
            description = data['explanation']

            if len(description) < 1024:
                embed.add_field(name = "**NASA Astronomy Picture of the Day**", value = data['explanation'], inline = False)
                embed.set_thumbnail(url = data['url'])
                embed.set_footer(text = "© " + data['copyright'])

                await ctx.send(embed = embed)
                return

            else:
                tocut = len(description) - 946
                cut = description[:-tocut]
                cleanup = cut.rfind(' ')
                final = description[:cleanup]

                value = final + " [...] - Full description available at [NASA APoD](https://apod.nasa.gov/apod)"
                embed.add_field(name = "**NASA Astronomy Picture of the Day**", value = value, inline = False)
                embed.set_thumbnail(url = data['url'])
                embed.set_footer(text = "© " + data['copyright'])

                await ctx.send(embed = embed)
                return


    @commands.command(
        name = 'triptoy',
        description = "A collection of trippy websites"
    )
    async def triptoy(self, ctx):
        embed = discord.Embed(
            title = "Have a trip toy!",
            colour = 0x7289da,
            description = random.choice(self.json_content['triptoys']['toys'])
        )
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(gen(bot))