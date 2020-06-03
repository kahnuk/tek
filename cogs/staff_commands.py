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
        user_roles = user.roles[1:]
        if not str(user.id) in verification_users:
            verification_users[str(user.id)] = user_roles
        for i in user.roles[1:]:
            await user.remove_roles(i)
        verification = discord.utils.get(ctx.guild.roles, id = 476377701154947082)
        await user.add_roles(verification)

    @commands.has_role(253619793691803658)
    @commands.command(
        name = 'verified'
    )
    async def verified(self, ctx, user: discord.Member):
        verification = discord.utils.get(ctx.guild.roles, id = 476377701154947082)
        if str(user.id) in verification_users:
            for i in verification_users[str(user.id)]:
                await user.add_roles(i)
        await user.remove_roles(verification)

def setup(bot):
    bot.add_cog(staff_commands(bot))