import discord
import asyncio
import json
import os
from discord.ext import commands
from datetime import datetime


commands_data = {}

for filename in os.listdir('data/page_embeds'):
    if filename.endswith('.json'):
        with open('data/page_embeds/' + filename) as json_file:
            json_content = json.load(json_file)
            commands_data[filename[:-5]] = json_content

class page_embeds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    class paginator:
        def __init__(self, ctx, command: str):
            self.bot = ctx.bot
            self.data = commands_data[command]
            self.pages = self.embed_pages(self.data)
            self.max_pages = len(self.pages)-1
            self.msg = ctx.message
            self.paginating = True
            self.channel = ctx.channel
            self.current = 0
            self.reactions = [
                            ('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self.first_page),
                            ('\N{BLACK LEFT-POINTING TRIANGLE}', self.backward),
                            ('\N{BLACK RIGHT-POINTING TRIANGLE}', self.forward),
                            ('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self.last_page),
                            ('\N{BLACK SQUARE FOR STOP}', self.stop)
                            ]

        #Create the list of embeds/pages
        def embed_pages(self, data: dict):
            pages = []
            for idx, page in enumerate(data['pages']):
                page_num = idx + 1
                embed = discord.Embed(
                    title = page[0],
                    description = page[1],
                    colour = 0x7289da,
                    timestamp = datetime.utcnow()
                )
                embed.set_author(name = data['title'])

                if 'footer' in data:
                    embed.set_footer(text = str(page_num) + '/' + str(len(data['pages'])) + data['footer'])
                else:
                    embed.set_footer(text = str(page_num) + '/' + str(len(data['pages'])) + '  Please use drugs responsibly')
                if 'image' in data:
                    embed.set_image(url = data['image'])
                if 'thumbnail' in data:
                    embed.set_thumbnail(url = data['thumbnail'])

                pages.append(embed)
            return pages
        
        #Send the first embed and add the reaction buttons
        async def setup(self):
            self.msg = await self.channel.send(embed = self.pages[0])
            if len(self.pages) == 1:
                return
            
            for (r, _) in self.reactions:
                await self.msg.add_reaction(r)


        #Change to defined page
        async def alter(self, page: int):
            await self.msg.edit(embed = self.pages[page])
            
        #Jump to first page
        async def first_page(self):
            self.current = 0
            await self.alter(self.current)
        

        #Jump to last page
        async def last_page(self):
            self.current = self.max_pages
            await self.alter(self.current)


        #Move back one page
        async def backward(self):
            if self.current == 0:
                self.current = self.max_pages
                await self.alter(self.current)
            else:
                self.current -= 1
                await self.alter(self.current)
            

        #Move forward one page    
        async def forward(self):
            if self.current == self.max_pages:
                self.current = 0
                await self.alter(self.current)
            else:
                self.current += 1
                await self.alter(self.current)
        

        #Stop paginating
        async def stop(self):
            asyncio.ensure_future(self.msg.clear_reactions())
            self.paginating = False



        def check(self, reaction, user):
            #Stops the bot from reacting to the reactions as they are added
            if user.id == self.bot.user.id:
                return False

            #Ignore reactions on other messages
            if reaction.message.id != self.msg.id:
                return False

            #Check if the emote is in the list of defined buttons, and set the associated function to self.execute
            for (emoji, func) in self.reactions:
                if reaction.emoji == emoji:
                    self.execute = func
                    return True
            return False



        async def paginate(self):
            await self.setup()
            while self.paginating:

                #Wait for reactions that fit the criteria in check for 120 seconds
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=self.check, timeout=120)
                except asyncio.TimeoutError:
                    return await self.stop()

                #Clear the reaction that was used
                try:
                    await self.msg.remove_reaction(reaction, user)
                except discord.HTTPException:
                    pass

                #Execute the function associated with the reaction that was added
                await self.execute()



    @commands.command(
        name = 'mdma',
        description = "MDMA harm reduction information",
        aliases = commands_data['mdma']['aliases']
    )
    async def mdma(self, ctx):
        pages = self.paginator(ctx, 'mdma')
        await pages.paginate()



    @commands.command(
        name = 'reagents',
        description = "Test kit vendors & use instructions",
        aliases = commands_data['reagents']['aliases']
    )
    async def reagents(self, ctx):
        pages = self.paginator(ctx, 'reagents')
        await pages.paginate()



    @commands.command(
        name = 'prep',
        description = "First trip preparation guide",
        aliases = commands_data['prep']['aliases']
    )
    async def prep(self, ctx):
        pages = self.paginator(ctx, 'prep')
        await pages.paginate()
    


    @commands.command(
        name = 'scales',
        description = "Scale vendors & information",
        aliases = commands_data['scales']['aliases']
    )
    async def scales(self, ctx):
        pages = self.paginator(ctx, 'scales')
        await pages.paginate()



    @commands.command(
        name = 'mdmasupps',
        description = "Information on MDMA & supplements"
    )
    async def mdmasupps(self, ctx):
        pages = self.paginator(ctx, 'mdmasupps')
        await pages.paginate()



    @commands.command(
        name = 'magnesium',
        description = "Information on magnesium"
    )
    async def magnesium(self, ctx):
        pages = self.paginator(ctx, 'magnesium')
        await pages.paginate()



    @commands.command(
        name = 'help',
        description = 'Help command'
    )
    async def help_cmd(self, ctx):
        pages = self.paginator(ctx, 'help')
        await pages.paginate()




def setup(bot):
    bot.add_cog(page_embeds(bot))