import discord
import sqlite3
import asyncio
from sqlite3 import Error
from discord.ext import tasks, commands
import time

database = '/home/kanuk/dev/tek/db/role_tracker.db'
conn = sqlite3.connect(database)
cursor = conn.cursor()

create_table_sql = """
    CREATE TABLE IF NOT EXISTS role_tracker (
    guild integer NOT NULL,
    member integer NOT NULL,
    role integer NOT NULL,
    timestamp integer NOT NULL
    );
"""

class role_tracker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        try:
            cursor.execute(create_table_sql)
        except Error as e:
            print(e)
        
        self.check_roles.start()



    @tasks.loop(seconds = 60.0)
    #Check the role table every 60 seconds for entries where the timestamp has passed and pass them to func role_toggle, then clear the entry
    async def check_roles(self):
        with conn:
            cursor.execute("SELECT * FROM role_tracker WHERE timestamp < strftime('%s', 'now')")
            all_rows = cursor.fetchall()
            for row in all_rows:
                guild_id = row[0]
                member_id = row[1]
                role_id = row[2]
                
                await self.role_toggle(guild_id, member_id, role_id)
            
            cursor.execute("DELETE FROM role_tracker WHERE timestamp < strftime('%s', 'now')")
            conn.commit()



    @check_roles.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()



    async def role_toggle(self, guild_id: int, member_id: int, role_id: int, *args):
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(member_id)
        role = discord.utils.get(guild.roles, id = role_id)
        
        embed = discord.Embed(
            colour = 0x7289da
        )

        #If two extra arguments have been passed (i.e it's being called from a command & not from check_roles), create an expiry timestamp & use the provided channel
        if len(args) == 2:
            now = time.time()
            expiry = now + args[0]
            channel = args[1]
        else:
            channel = discord.utils.get(guild.text_channels, name = 'bot-spam')

        #If the member has role, remove the role & delete any matching entries. Send a notification embed
        if role in member.roles:
            await member.remove_roles(role)
            with conn:
                cursor.execute('DELETE FROM role_tracker WHERE guild=? AND member=? AND role=?', (guild_id, member_id, role_id))
                conn.commit()
            
            embed.add_field(name = '**Roles Updated**', value = "Role **'{}'** removed from: {}".format(role, member.mention), inline = False)
            await channel.send(embed = embed , delete_after = 5)
            
        #If the member does not have the role, add the role & create a corresponding entry in the database. Send a notification embed
        else:
            await member.add_roles(role)
            with conn:
                cursor.execute('INSERT INTO role_tracker VALUES(?,?,?,?)', (guild_id, member_id, role_id, expiry))
                conn.commit()
            
            embed.add_field(name = '**Roles Updated**', value = "Role **'{}'** added to: {}".format(role, member.mention), inline = False)
            await channel.send(embed = embed, delete_after = 5)
            



    @commands.command(
        name = 'drunk',
        description = "Manages Drunk role",
        aliases = ['sloshed']
    )
    async def drunk(self, ctx):
        await self.role_toggle(ctx.guild.id, ctx.author.id, discord.utils.get(ctx.guild.roles, name = 'Drunk').id, 30, ctx.channel)
        await asyncio.sleep(5)
        await ctx.message.delete()
    
    @commands.command(
        name = 'high',
        description = "Manages High role",
        aliases = ['stoned', 'baked', 'zooted']
    )
    async def high(self, ctx):
        await self.role_toggle(ctx.guild.id, ctx.author.id, discord.utils.get(ctx.guild.roles, name = 'High').id, 30, ctx.channel)
        await asyncio.sleep(5)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(role_tracker(bot))