import asyncio
import random
from datetime import datetime

import discord
from discord.ext import commands

verification_users = {}
chill_users = {}


def is_in_guild(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id

    return commands.check(predicate)


class utility_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(253619793691803658, 345951762173394954)
    @commands.command(
        name = 'verify',
        description = "ID Verification"
    )
    async def verify(self, ctx, user: discord.Member):
        print(verification_users)
        user_roles = user.roles[1:]
        if not str(user.id) in verification_users:
            verification_users[str(user.id)] = user_roles
        for i in user.roles[1:]:
            await user.remove_roles(i)
        if ctx.guild.id == 253612214148136981:
            verification = discord.utils.get(ctx.guild.roles, id = 476377701154947082)
        else:
            verification = discord.utils.get(ctx.guild.roles, id = 730509216883802244)
        await user.add_roles(verification)
        embed = discord.Embed(
            title = "Success!",
            description = f"User **{user.name} [{user.id}]** has been put in verification.",
            colour = 0x7289da
        )
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.has_any_role(401512090449215489)
    @commands.command(
        name = 'chill',
        description = "Chill toggle"
    )
    async def chill(self, ctx, user: discord.Member):
        chill = discord.utils.get(ctx.guild.roles, id = 739272333512147066)
        user_roles = user.roles[1:]
        if not chill in user.roles:
            if not str(user.id) in chill_users:
                chill_users[str(user.id)] = user_roles
            for i in user.roles[1:]:
                await user.remove_roles(i)
            await user.add_roles(chill)
            embed = discord.Embed(
                title = "Success!",
                description = f"User **{user.name}** has been chilled!",
                colour = 0x7289da
            )
            embed.set_thumbnail(url = user.avatar_url)
            await ctx.send(embed = embed)
        else:
            if str(user.id) in chill_users:
                for i in chill_users[str(user.id)]:
                    await user.add_roles(i)
            await user.remove_roles(chill)
            embed = discord.Embed(
                title = "Success!",
                description = f"User **{user.name}** is now chill!",
                colour = 0x7289da
            )
            embed.set_thumbnail(url = user.avatar_url)
            await ctx.send(embed = embed)

    @commands.has_any_role(253619793691803658, 345951762173394954)
    @commands.command(
        name = 'verified'
    )
    async def verified(self, ctx, user: discord.Member, *reason: str):
        if ctx.guild.id == 253612214148136981:
            verification = discord.utils.get(ctx.guild.roles, id = 476377701154947082)
        else:
            verification = discord.utils.get(ctx.guild.roles, id = 730509216883802244)
        if reason:
            reason_str = ": " + " ".join(reason)
        else:
            reason_str = ""
        if str(user.id) in verification_users:
            for i in verification_users[str(user.id)]:
                await user.add_roles(i)
        await user.remove_roles(verification)
        embed = discord.Embed(
            title = "Verified User",
            description = f"User **{user.name} [{user.id}]** has been verified by **{ctx.author.name}**{reason_str}",
            colour = 0x7289da,
            timestamp = datetime.utcnow()
        )
        embed.set_thumbnail(url = user.avatar_url)
        embed.set_footer(text = f"User ID: {user.id}")
        if ctx.guild.id == 253612214148136981:
            verified_channel = discord.utils.get(ctx.guild.text_channels, id = int(655009478936363008))
        else:
            verified_channel = discord.utils.get(ctx.guild.text_channels, id = int(730512825449185472))
        await verified_channel.send(embed = embed)
        success_embed = discord.Embed(
            title = "Success!",
            description = f"User **{user.name} [{user.id}]** has been successfully verified.",
            colour = 0x7289da
        )
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = success_embed)

    @commands.has_any_role(585550892091310080, 345951762173394954)
    @commands.command(
        name = 'colour',
        aliases = ['color']
    )
    async def colour(self, ctx, r: int, g: int, b: int):
        rgb = [r, g, b]
        if all(0 <= i <= 255 for i in rgb):
            role_colour = discord.Colour.from_rgb(r, g, b)
            baked = discord.utils.get(ctx.guild.roles, name = 'Baked')
            new_position = int(baked.position)
            new_position -= 1
            print(new_position)
            if not discord.utils.get(ctx.guild.roles, name = str(ctx.author.id)):
                await ctx.guild.create_role(name = str(ctx.author.id), colour = role_colour)
                new_role = discord.utils.get(ctx.guild.roles, name = str(ctx.author.id))
                await new_role.edit(position = int(new_position))
                await ctx.author.add_roles(new_role)
            else:
                new_role = await discord.utils \
                    .get(ctx.guild.roles, name = str(ctx.author.id)) \
                    .edit(colour = role_colour, position = new_position)

            embed = discord.Embed(
                title = "Custom colour applied!",
                description = f"Applied colour **[{r}, {g}, {b}]** to **{ctx.author.display_name}**!",
                colour = role_colour
            )
            await ctx.channel.send(embed = embed)
        else:
            await ctx.channel.send('**Error:** That is not a valid RGB colour code!')

    @commands.command(
        name = 'clearcolour',
        aliases = ['clearcolor']
    )
    async def clearcolour(self, ctx):
        colour_role = discord.utils.get(ctx.guild.roles, name = str(ctx.author.id))
        if colour_role:
            await colour_role.delete()
            await ctx.channel.send(f"Custom role for {ctx.author.display_name} deleted.")

    @commands.has_any_role(401512090449215489, 723896600086315079, 339896504447795210, 335169145039486976)
    @commands.command(
        name = 'triptoggle',
        aliases = ['toggletrip']
    )
    async def triptoggle(self, ctx, member: discord.Member):
        if ctx.guild.id == 335167514961248256:
            trip_role = discord.utils.get(ctx.guild.roles, id = 455415325018685451)
        else:
            trip_role = discord.utils.get(ctx.guild.roles, id = 273134198498394112)
        if trip_role in member.roles:
            await member.remove_roles(trip_role)
            await ctx.channel.send(f"The tripping role has been taken off {member.display_name}.")
        else:
            await member.add_roles(trip_role)
            await ctx.channel.send(f"{member.display_name} has been given the tripping role.")

    @commands.command(
        name = 'gtoke',
        description = "Starts a group toke",
        aliases = ['tokeup', 'sesh']
    )
    async def gtoke(self, ctx):
        sent_messages = list()  # Notifications the bot has sent
        message_templates = [
            f"{ctx.author.display_name} has started a group toke - toke up in two minutes! Use the reaction button to join in",
            "Toke up in: one minute! Use the reaction button to join in",
            "Toke up in: 30 seconds! Use the reaction button to join in"
        ]
        emotes = [
            '<:Weeed:581023462534021120>', '<:weed:255964645561466880>', '<:smoke:478661373417619476>',
            '<:pepetoke:502604660927102977>', '<:musky:487937634157461505>', '<:joint:585773581980663811>',
            '<:blunt:585774074094026763>', '<:bongface:456821076387823626>', '<a:bong:585769584888512521>',
            '<:smonke:777647646684610620>'
        ]
        emote_list = list()
        tokers = list()  # Final list of tokers display names
        tokers.append(ctx.author.display_name)

        i = 0
        for message in message_templates:
            i += 1
            # For each message in the templates list, send the message and append the message ID to the list
            sent_message = await ctx.channel.send(message)
            sent_messages.append(sent_message.id)
            # Choose an emote to react with and add it to the running list
            emote = random.choice(emotes)
            await sent_message.add_reaction(emote)
            emote_list.append(str(emote))

            if i == 1:
                interval = 60
                await asyncio.sleep(interval)
            if i == 2:
                interval = 30
                await asyncio.sleep(interval)
            if i == 3:
                interval = 22
                await asyncio.sleep(interval)

        # Send the countdown and toke signal
        timer = 5
        msg = await ctx.channel.send("5...")
        for i in range(timer):
            timer = timer - 1
            await asyncio.sleep(1)
            if not timer == 0:
                await msg.edit(content = f'{timer}...')
            else:
                await msg.edit(content = 'Toke up!')

        tokers_id_list = list()
        dice = random.randrange(100)
        # For each message sent, cache it (required for accurate reaction counts) and count the reactions
        # This is a bit of a gross block but I couldn't immediately see a nice way to break it up
        for message in sent_messages:
            cached_message = await ctx.channel.fetch_message(message)
            for reaction in cached_message.reactions:
                # If the reaction is one of the trigger emotes, iterate through the list of users who hit it
                if str(reaction) in emote_list:
                    async for user in reaction.users():
                        if not user.id in tokers_id_list:
                            # 1/100 chance for Tek to get lit ;)
                            if dice == 69:
                                tokers_id_list.append(user.id)
                            else:
                                if not user.id == 693968173883457536:
                                    tokers_id_list.append(user.id)

        # Since reaction.users() can return User objects that don't play nice with server nicknames, fetch the member
        # object from ID and append the display name to the list
        for toker_id in tokers_id_list:
            toker_obj = await ctx.guild.fetch_member(toker_id)
            if not str(toker_obj.display_name) in tokers:
                tokers.append(str(toker_obj.display_name))

        # Toke up!
        await asyncio.sleep(3)
        formatted_tokers = ', '.join(tokers)
        await ctx.channel.send(f"{formatted_tokers} toked up! {emote}")

def setup(bot):
    bot.add_cog(utility_commands(bot))
