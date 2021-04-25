import asyncio
import json
import os
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands

commands_data = {}

for filename in os.listdir('data/page_embeds'):
    if filename.endswith('.json'):
        with open('data/page_embeds/' + filename) as json_file:
            json_content = json.load(json_file)
            commands_data[filename[:-5]] = json_content


class page_embeds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open('config.json') as config:
            self.json_config = json.load(config)

    class paginator:
        def __init__(self, ctx, command: str, *pages: list):
            self.bot = ctx.bot
            if pages:
                self.pages = pages[0]
            else:
                self.data = commands_data[command]
                self.pages = self.embed_pages(self.data)
            self.max_pages = len(self.pages) - 1
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

        # Create the list of embeds/pages
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
                    embed.set_footer(text = f"{page_num}/{len(data['pages'])} {data['footer']}")
                else:
                    embed.set_footer(text = f"{page_num}/{len(data['pages'])}  Please use drugs responsibly")
                if 'image' in data:
                    embed.set_image(url = data['image'])
                if 'thumbnail' in data:
                    embed.set_thumbnail(url = data['thumbnail'])

                pages.append(embed)
            return pages

        # Send the first embed and add the reaction buttons
        async def setup(self):
            self.msg = await self.channel.send(embed = self.pages[0])
            if len(self.pages) == 1:
                return

            for (r, _) in self.reactions:
                await self.msg.add_reaction(r)

        # Change to defined page
        async def alter(self, page: int):
            await self.msg.edit(embed = self.pages[page])

        # Jump to first page
        async def first_page(self):
            self.current = 0
            await self.alter(self.current)

        # Jump to last page
        async def last_page(self):
            self.current = self.max_pages
            await self.alter(self.current)

        # Move back one page
        async def backward(self):
            if self.current == 0:
                self.current = self.max_pages
                await self.alter(self.current)
            else:
                self.current -= 1
                await self.alter(self.current)

        # Move forward one page
        async def forward(self):
            if self.current == self.max_pages:
                self.current = 0
                await self.alter(self.current)
            else:
                self.current += 1
                await self.alter(self.current)

        # Stop paginating
        async def stop(self):
            asyncio.ensure_future(self.msg.clear_reactions())
            self.paginating = False

        def check(self, reaction, user):
            # Stops the bot from reacting to the reactions as they are added
            if user.id == self.bot.user.id:
                return False

            # Ignore reactions on other messages
            if reaction.message.id != self.msg.id:
                return False

            # Check if the emote is in the list of defined buttons, and set the associated function to self.execute
            for (emoji, func) in self.reactions:
                if reaction.emoji == emoji:
                    self.execute = func
                    return True
            return False

        async def paginate(self):
            await self.setup()
            while self.paginating:

                # Wait for reactions that fit the criteria in check for 120 seconds
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check = self.check, timeout = 120)
                except asyncio.TimeoutError:
                    return await self.stop()

                # Clear the reaction that was used
                try:
                    await self.msg.remove_reaction(reaction, user)
                except discord.HTTPException:
                    pass

                # Execute the function associated with the reaction that was added
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
    async def help(self, ctx):
        pages = self.paginator(ctx, 'help')
        await pages.paginate()

    @commands.command(
        name = 'apod',
        description = "NASA Astronomy Picture of the Day"
    )
    async def apod(self, ctx, *date):
        async with aiohttp.ClientSession() as session:
            if date:
                url = f"https://api.nasa.gov/planetary/apod?api_key = {self.json_config['apod_key']}&date = {date[0]}"
            else:
                url = f"https://api.nasa.gov/planetary/apod?api_key = {self.json_config['apod_key']}"

            async with session.get(url) as r:
                if r.status == 200:
                    data = await r.json()

        pages = []

        if data['media_type'] == 'image':
            page_one = discord.Embed(
                title = data['title'],
                colour = 0x7289da,
                timestamp = datetime.utcnow()
            )
            page_one.set_author(name = f"NASA Astronomy Picture of the Day - {data['date']}")
            page_one.set_image(url = data['url'])
            if 'copyright' in data:
                page_one.set_footer(text = f"© {data['copyright']}")
            pages.append(page_one)

            page_two = discord.Embed(
                title = data['title'],
                colour = 0x7289da,
                description = data['explanation'],
                timestamp = datetime.utcnow()
            )
            page_two.set_author(name = f"NASA Astronomy Picture of the Day - {data['date']}")
            if 'copyright' in data:
                page_two.set_footer(text = f"© {data['copyright']}")
            pages.append(page_two)

        if data['media_type'] == 'video':
            page_one = discord.Embed(
                title = data['title'],
                colour = 0x7289da,
                description = f"Video URL: {data['url']}",
                timestamp = datetime.utcnow()
            )

            page_one.set_author(name = f"NASA Astronomy Video of the Day - {data['date']}")
            if 'copyright' in data:
                page_one.set_footer(text = f"© {data['copyright']}")
            pages.append(page_one)

            page_two = discord.Embed(
                title = data['title'],
                colour = 0x7289da,
                description = data['explanation'],
                timestamp = datetime.utcnow()
            )

            page_two.set_author(name = f"NASA Astronomy Video of the Day - {data['date']}")
            if 'copyright' in data:
                page_two.set_footer(text = f"© {data['copyright']}")
            pages.append(page_two)

        paginator = self.paginator(ctx, 'apod', pages)
        await paginator.paginate()


def setup(bot):
    bot.add_cog(page_embeds(bot))
