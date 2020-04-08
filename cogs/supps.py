import discord
import json
from discord.ext import commands

class supps(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        with open('data/supps.json', 'r') as readable:
                self.json_content = json.loads(readable.read())

    async def embed(self, command: str, footer: bool, channel: discord.TextChannel):

        #Fill .JSON path information
        json_path = self.json_content[command]
        fields = json_path['fields']
        num = len(fields)

        #Create embed object
        embed = discord.Embed(
            title = json_path['title'],
            colour = 0x7289da
        )

        #Fill an embed field for every array under the 'fields' object
        for x in range(0, num):
            embed.add_field(name = fields[x][0], value = fields[x][1], inline = fields[x][2])

        if footer == True:
            embed.set_footer(text = json_path['footer'])

        await channel.send(embed = embed)
        return



    @commands.command(
        name = 'mdmasupps',
        description = "A brief overview of supplements for MDMA"
    )
    async def mdmasupps(self, ctx):
        await self.embed('mdmasupps', False, ctx.message.channel)
        return



    @commands.command(
        name = 'supps',
        description = "A list of various beneficial supplements",
        aliases = ['supplements']
    )
    async def supps(self, ctx):
        await self.embed('supps', False, ctx.message.channel)
        return



    @commands.command(
        name = 'ala',
        description = "A brief overview of alpha-lipoic acid"
    )
    async def ala(self, ctx):
        await self.embed('ala', False, ctx.message.channel)
        return



    @commands.command(
        name = 'alcar',
        description = "A brief overview of acetyl-l-carnitine"
    )
    async def alcar(self, ctx):
        await self.embed('alcar', False, ctx.message.channel)
        return

    

    @commands.command(
        name = 'vitc',
        description = "A brief overview of vitamin C"
    )
    async def vitc(self, ctx):
        await self.embed('vitc', False, ctx.message.channel)
        return


    
    @commands.command(
        name = 'magnesium',
        description = "A brief overview of magnesium"
    )
    async def magnesium(self, ctx):
        await self.embed('magnesium', False, ctx.message.channel)
        return

    

    @commands.command(
        name = 'hydration',
        description = "A brief overview of electrolytic/isotonic solutions"
    )
    async def hydration(self, ctx):
        await self.embed('hydration', False, ctx.message.channel)
        return



    @commands.command(
        name = 'ginger',
        description = "A brief overview of ginger"
    )
    async def ginger(self, ctx):
        await self.embed('ginger', False, ctx.message.channel)
        return



    @commands.command(
        name = '5htp',
        description = "A brief overview of 5-HTP"
    )
    async def fivehtp(self, ctx):
        await self.embed('5htp', False, ctx.message.channel)
        return



def setup(bot):
    bot.add_cog(supps(bot))