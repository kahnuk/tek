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
        if 'description' in data:
            embed = discord.Embed(
                    title = data['title'],
                    description = data['description'],
                    colour = 0x7289da,
                    timestamp = datetime.utcnow()
            )
        else:
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
        return embed


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



    @commands.command(
        name = 'neurotoxic',
        description = "Example of MDMA induced neurotoxicity",
        aliases = commands_data['neurotoxic']['aliases']
    )
    async def neurotoxic(self, ctx):
        self.embed('neurotoxic', ctx.channel)


    @commands.command(
        name = 'rule',
        description = "Prints rules"
    )
    async def rule(self, ctx, rule):
        rulename = 'rule' + rule
        self.embed(rulename, ctx.channel)



    @commands.command(
        name = 'rule1',
        description = "Prints rule 1",
        aliases = commands_data['rule1']['aliases']
    )
    async def rule1(self, ctx):
        self.embed('rule1', ctx.channel)



    @commands.command(
        name = 'rule2',
        description = "Prints rule 2",
        aliases = commands_data['rule2']['aliases']
    )
    async def rule2(self, ctx):
        self.embed('rule2', ctx.channel)



    @commands.command(
        name = 'rule3',
        description = "Prints rule 3",
        aliases = commands_data['rule3']['aliases']
    )
    async def rule3(self, ctx):
        self.embed('rule3', ctx.channel)



    @commands.command(
        name = 'rule4',
        description = "Prints rule 4",
        aliases = commands_data['rule4']['aliases']
    )
    async def rule4(self, ctx):
        self.embed('rule4', ctx.channel)


    @commands.command(
        name = 'rule5',
        description = "Prints rule 5",
        aliases = commands_data['rule5']['aliases']
    )
    async def rule5(self, ctx):
        self.embed('rule5', ctx.channel)



    @commands.command(
        name = 'rule6',
        description = "Prints rule 6",
        aliases = commands_data['rule6']['aliases']
    )
    async def rule6(self, ctx):
        self.embed('rule6', ctx.channel)



    @commands.command(
        name = 'rule7',
        description = "Prints rule 7",
        aliases = commands_data['rule7']['aliases']
    )
    async def rule7(self, ctx):
        self.embed('rule7', ctx.channel)



    @commands.command(
        name = 'gtoke',
        description = "Starts a group toke",
        aliases = ['tokeup', 'sesh']
    )
    async def gtoke(self, ctx):
        emotes = ['<:Weeed:581023462534021120>', '<:weed:255964645561466880>', '<:smoke:478661373417619476>', '<:pepetoke:502604660927102977>', '<:musky:487937634157461505>', '<:joint:585773581980663811>', '<:blunt:585774074094026763>', '<:bongface:456821076387823626>']
        bot_message = await ctx.channel.send(f"{ctx.author.display_name} has started a group toke - use the reaction to join in! Toke up in: two minutes")
        emote = random.choice(emotes)
        reaction_add = await bot_message.add_reaction(emote)
        cached_message = await ctx.channel.fetch_message(bot_message.id)
        users = list()
        users.append(str(ctx.author.display_name))
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60)
                if str(reaction) == str(emote):
                    if not str(user.display_name) in users:
                        users.append(str(user.display_name))
            except asyncio.TimeoutError:
                break
        bot_message = await ctx.channel.send("Group toke commencing in one minute! Use the reaction to join in")
        emote = random.choice(emotes)
        reaction_add = await bot_message.add_reaction(emote)
        cached_message = await ctx.channel.fetch_message(bot_message.id)
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60)
                if str(reaction) == str(emote):
                    if not str(user.display_name) in users:
                        users.append(str(user.display_name))
            except asyncio.TimeoutError:
                break
        finished_users = ', '.join(users)
        await ctx.channel.send(f"{finished_users} toked up! {emote}")
        
def setup(bot):
    bot.add_cog(static_embeds(bot))
