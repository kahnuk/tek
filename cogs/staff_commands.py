import discord
import json
import asyncio
import os
import random
from datetime import datetime
from discord.ext import commands

verification_users = {}

class staff_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_role(253619793691803658)
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
        verification = discord.utils.get(ctx.guild.roles, id = 476377701154947082)
        await user.add_roles(verification)
        embed = discord.Embed(
            title = "Success!",
            description = f"User **{user.name} [{user.id}]** has been put in verification.",
            colour = 0x7289da
        )
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.has_role(253619793691803658)
    @commands.command(
        name = 'verified'
    )
    async def verified(self, ctx, user: discord.Member, *reason: str):
        verification = discord.utils.get(ctx.guild.roles, id = 476377701154947082)
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
        verified_channel = discord.utils.get(ctx.guild.text_channels, id = int(655009478936363008))
        await verified_channel.send(embed = embed)
def setup(bot):
    bot.add_cog(staff_commands(bot))
