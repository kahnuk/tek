import discord
import asyncio
from discord.ext import commands

async def roletimer(self, user, role, length):
        i = 0
        print(str(user) + ' started timer for role ' + str(role) + ', expires in: ' + str(length) + 's')
        while i < length:
            i += 1
            await asyncio.sleep(1)
        print(str(user) + "'s timer expired for role " + str(role) + ' after ' + str(length) + 's')
        return



class rolemgr(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='drunk',
        description='Manages drunk role',
        aliases=['sloshed']
    )
    async def drunk(self, ctx):
        user = ctx.message.author
        chnl = ctx.message.channel
        drunk = discord.utils.get(user.guild.roles, name='Drunk')

        embed = discord.Embed(color=0xde89ff)

        if drunk not in user.roles:

            #Add role, send notification & start role timer
            await user.add_roles(drunk)
            embed.add_field(name="**Roles Updated**", value="**Drunk** added to {}, starting timer for 5 minutes".format(user.mention), inline=False)
            await chnl.send(embed=embed,delete_after=(5))
            await ctx.message.delete()
            embed.clear_fields()
            await roletimer(self, ctx.message.author, drunk, 300)

            #If the timer expires and the user still has the role, remove it & send notification
            if drunk in user.roles:
                await user.remove_roles(drunk)
                embed.add_field(name="**Timer Expired**", value="**Drunk** removed from {}".format(user.mention), inline=False)
                await chnl.send(embed=embed,delete_after=(5))
                embed.clear_fields()
                return
            return

        #Remove role if user already has it
        if drunk in user.roles:
            await user.remove_roles(drunk)
            embed.add_field(name="**Roles Updated**", value="**Drunk** removed from {}".format(user.mention), inline=False)
            await chnl.send(embed=embed,delete_after=(5))
            embed.clear_fields()
            return
        return



    @commands.command(
        name='high',
        description='Manages high role',
        aliases=['stoned', 'baked', 'zooted']
    )
    async def high(self, ctx):
        user = ctx.message.author
        chnl = ctx.message.channel
        high = discord.utils.get(user.guild.roles, name='Stoned')

        embed = discord.Embed(colour=0xde89ff)

        if high not in user.roles:

            #Add role, send notification & start role timer
            await user.add_roles(high)
            embed.add_field(name="**Roles Updated**", value="**High** added to {}, starting timer for 5 minutes".format(user.mention), inline=False)
            await chnl.send(embed=embed,delete_after=(5))
            await ctx.message.delete()
            embed.clear_fields()
            await roletimer(self, ctx.message.author, high, 300)

            #If the timer expires and the user still has the role, remove it & send notification
            if high in user.roles:
                await user.remove_roles(high)
                embed.add_field(name="**Timer Expired**", value="**High** removed from {}".format(user.mention), inline=False)
                await chnl.send(embed=embed,delete_after=(5))
                embed.clear_fields()
                return
            return

        #Remove role if user already has it
        if high in user.roles:
            await user.remove_roles(high)
            embed.add_field(name="**Roles Updated**", value="**High** removed from {}".format(user.mention), inline=False)
            await chnl.send(embed=embed,delete_after=(5))
            embed.clear_fields()
            return
        return

def setup(bot):
    bot.add_cog(rolemgr(bot))