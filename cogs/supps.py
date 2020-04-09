import discord
import json
from discord.ext import commands

class supps(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        with open('data/supps.json', 'r') as readable:
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
        name = 'mdmasupps',
        description = "A brief overview of supplements for MDMA"
    )
    async def mdmasupps(self, ctx):
        await self.embed('mdmasupps', ctx.message.channel)
        return



    @commands.command(
        name = 'supps',
        description = "A list of various beneficial supplements",
        aliases = ['supplements']
    )
    async def supps(self, ctx):
        await self.embed('supps', ctx.message.channel)
        return



    @commands.command(
        name = 'ala',
        description = "A brief overview of alpha-lipoic acid"
    )
    async def ala(self, ctx):
        await self.embed('ala', ctx.message.channel)
        return



    @commands.command(
        name = 'alcar',
        description = "A brief overview of acetyl-l-carnitine"
    )
    async def alcar(self, ctx):
        await self.embed('alcar', ctx.message.channel)
        return

    

    @commands.command(
        name = 'vitc',
        description = "A brief overview of vitamin C"
    )
    async def vitc(self, ctx):
        await self.embed('vitc', ctx.message.channel)
        return


    
    @commands.command(
        name = 'magnesium',
        description = "A brief overview of magnesium"
    )
    async def magnesium(self, ctx):
        await self.embed('magnesium', ctx.message.channel)
        return

    

    @commands.command(
        name = 'hydration',
        description = "A brief overview of electrolytic/isotonic solutions"
    )
    async def hydration(self, ctx):
        await self.embed('hydration', ctx.message.channel)
        return



    @commands.command(
        name = 'ginger',
        description = "A brief overview of ginger"
    )
    async def ginger(self, ctx):
        await self.embed('ginger', ctx.message.channel)
        return



    @commands.command(
        name = '5htp',
        description = "A brief overview of 5-HTP"
    )
    async def fivehtp(self, ctx):
        await self.embed('5htp', ctx.message.channel)
        return



def setup(bot):
    bot.add_cog(supps(bot))