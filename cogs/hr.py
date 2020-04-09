import discord
import json
from discord.ext import commands

class hr(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        with open('data/hr.json', 'r') as readable:
                self.json_content = json.loads(readable.read())

    async def embed(self, command: str, channel: discord.TextChannel):

        #Fill .JSON path information
        json_path = self.json_content[command]
        fields = json_path['fields']
        footer = json_path.get('footer')

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
        name = 'mdma',
        description = "A brief overview of harm reduction for MDMA",
        aliases = ['molly', 'rollsafe', 'mdmahr']
    )
    async def mdma(self, ctx):
        await self.embed('mdma', ctx.channel)
        return



    @commands.command(
        name = 'reagents',
        description = "Information on reagent test kits and reputable sources",
        aliases = ['testkits', 'reagentkits', 'kits']
    )
    async def reagents(self, ctx):
        await self.embed('reagents', ctx.channel)
        await ctx.send(file=discord.File('media/color-chart.jpg'))
        return

    

    @commands.command(
        name = 'resources',
        description = "Small list of various harm reduction related websites and communities"
    )
    async def resources(self, ctx):
        await self.embed('resources', ctx.channel)
        return



    @commands.command(
        name = 'testmdma',
        description = "Detailed guide to reagent testing MDMA",
        aliases = ['testmolly', 'mdmatest', 'mollytest']
    )
    async def testmdma(self, ctx):
        await ctx.send(file = discord.File('media/mdma-instructions.jpg'))
        return
    


    @commands.command(
        name = 'testcoke',
        description = "Detailed guide to reagent testing cocaine",
        aliases = ['testcocaine', 'coketest', 'cocainetest']
    )
    async def testcoke(self, ctx):
        await ctx.send(file = discord.File('media/coke-instructions.jpg'))
        return
    


    @commands.command(
        name = 'testlsd',
        description = "Detailed guide to reagent testing LSD",
        aliases = ['testacid', 'lsdtest', 'acidtest']
    )
    async def testlsd(self, ctx):
        await ctx.send(file = discord.File('media/lsd-instructions.jpg'))
        return



    @commands.command(
        name = 'fentstrips',
        description = "Detailed guide to using fentanyl test strips",
        aliases = ['fenttest', 'strips', 'testfent', 'teststrips']
    )
    async def fentstrips(self, ctx):
        await ctx.send(file = discord.File('media/fentanyl-instructions.jpg'))
        return



    @commands.command(
        name = 'breathe',
        description = "Breathing gifs"
    )
    async def breathe(self, ctx):
        await ctx.send(file = discord.File('media/breathe2.gif'))
        return
    


    @commands.command(
        name = 'recovery',
        description = "Recovery position",
        aliases = ['recoveryposition', 'recoverypos']
    )
    async def recovery(self, ctx):
        await ctx.send(file = discord.File('media/recovery.jpg'))
        return



    @commands.command(
        name = 'scales',
        description = "Scale harm reduction information",
        aliases = ['scale']
    )
    async def scales(self, ctx):
        await self.embed('scales', ctx.channel)
        return



    @commands.command(
        name = 'prep',
        description = "Preparation tips for your first trip",
        aliases = ['firsttrip']
    )
    async def prep(self, ctx):
        await self.embed('prep', ctx.channel)
        return

    @commands.command(
        name = 'badtrip',
        description = "Various grounding techniques and images"
    )
    async def badtrip(self, ctx):
        json_content = self.json_content['badtrip']
        embed = discord.Embed(
            title = json_content['title'],
            colour = 0x7289da
        )
        embed.add_field(name = json_content['fields'][0][0], value = json_content['fields'][0][1], inline = json_content['fields'][0][2])
        embed.add_field(name = json_content['fields'][1][0], value = json_content['fields'][1][1], inline = json_content['fields'][1][2])
        embed.add_field(name = json_content['fields'][2][0], value = json_content['fields'][2][1], inline = json_content['fields'][2][2])
        embed.set_image(url = json_content['url'])
        return

def setup(bot):
    bot.add_cog(hr(bot))