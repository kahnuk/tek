import discord
import sqlite3
import asyncio
import json
from sqlite3 import Error
from discord.ext import tasks, commands
import time

database = '/home/kanuk/dev/tek/db/role_tracker.db'
conn = sqlite3.connect(database)
cursor = conn.cursor()

with open('data/roles.json') as json_file:
    json_content = json.load(json_file)
    json_roles = json_content['role_commands']

class role_tracker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.sql_execute('create_table.sql')
        self.check_role_table.start()



    @tasks.loop(seconds = 60.0)
    #Check the role table every 60 seconds for entries where the timestamp has passed and pass them to func role_toggle, then clear the entry
    async def check_role_table(self):
        with conn:
            self.sql_execute('select_passed.sql')
            all_rows = cursor.fetchall()
            for row in all_rows:
                guild = self.bot.get_guild(row[0])
                member = guild.get_member(row[1])
                role = discord.utils.get(guild.roles, id = row[2])
                bot_channel_id = int(json_content[str(row[0])]['bot_channel'])
                bot_channel = discord.utils.get(guild.text_channels, id = bot_channel_id)
                self.remove_role(guild, member, role, bot_channel)



    @check_role_table.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()



    def check_member_roles(self, guild: discord.Guild, member: discord.Member, role: discord.Role, channel: discord.TextChannel, duration: int):
        if role in member.roles:
            self.remove_role(guild, member, role, channel)
        else:
            self.add_role(guild, member, role, channel, duration)



    def remove_role(self, guild: discord.Guild, member: discord.Member, role: discord.Role, channel: discord.TextChannel):
        embed = discord.Embed(colour = 0x7289da)
        embed.add_field(name = '**Roles Updated**', value = f"Role **'{role}'** removed from: {member.mention}", inline = False)
        asyncio.ensure_future(channel.send(embed = embed, delete_after = 5))
        asyncio.ensure_future(member.remove_roles(role))
        self.sql_execute('delete.sql', guild.id, member.id, role.id)


    def add_role(self, guild: discord.Guild, member: discord.Member, role: discord.Role, channel: discord.TextChannel, duration: int):
        duration_hrs = duration * 3600
        expiry = time.time() + duration_hrs
        embed = discord.Embed(colour = 0x7289da)
        embed.add_field(name = "**Roles Updated**", value = f"Role **'{role}'** added to: {member.mention}", inline = False)
        asyncio.ensure_future(channel.send(embed = embed, delete_after = 5))
        asyncio.ensure_future(member.add_roles(role))
        self.sql_execute('insert.sql', guild.id, member.id, role.id, expiry)



    def sql_execute(self, filename, *params):
        with open('sql/' + filename, 'r') as readable:
            sql_file = readable.read()
            readable.close()

        try:
            cursor.execute(sql_file, params)
            conn.commit()
        except Error as e:
            print('Error in execution of: ' + filename)
            print(e)

    @commands.command(
        name = 'role',
        description = "Manages various status roles",
        aliases = json_roles
    )
    async def change_role(self, ctx):
        if ctx.invoked_with == 'gabaergic':
            self.check_member_roles(ctx.guild, ctx.author, discord.utils.get(ctx.guild.roles, name = 'GABAergic'), ctx.channel, 30)
        if discord.utils.get(ctx.guild.roles, name = ctx.invoked_with.capitalize()):
            self.check_member_roles(ctx.guild, ctx.author, discord.utils.get(ctx.guild.roles, name = ctx.invoked_with.capitalize()), ctx.channel, 30)
        asyncio.ensure_future(ctx.message.delete())
        

def setup(bot):
    bot.add_cog(role_tracker(bot))