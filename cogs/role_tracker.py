import asyncio
import json
import sqlite3
import time
from datetime import datetime
from sqlite3 import Error

import discord
from discord.ext import tasks, commands

database = 'db/role_tracker.db'
conn = sqlite3.connect(database)
cursor = conn.cursor()

with open('data/roles/roles.json') as json_file:
    json_content = json.load(json_file)
    json_roles = json_content['roles']
    json_aliases = json_content['aliases']

    role_list = list(json_roles.keys())
    alias_list = list(json_content['aliases'].keys())
    roles = role_list + alias_list

with open('config.json') as json_config:
    json_config_content = json.load(json_config)
    json_guilds = json_config_content['guilds']


def is_in_guild(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id

    return commands.check(predicate)


class role_tracker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.sql_execute('create_table.sql')
        self.check_role_table.start()

    @tasks.loop(seconds = 60.0)
    # Check the role table every 60 seconds for entries where the timestamp has passed and pass them to func
    # role_toggle, then clear the entry
    async def check_role_table(self):
        with conn:
            self.sql_execute('select_passed.sql')
            all_rows = cursor.fetchall()
            for row in all_rows:
                try:
                    guild = self.bot.get_guild(row[0])
                    member = await guild.fetch_member(row[1])
                    role = discord.utils.get(guild.roles, id = row[2])
                    self.check_member_roles(guild, member, role)
                except:
                    print('Member ' + str(row[1]) + ' does not exist.')
                    self.sql_execute('delete.sql', row[0], row[1], row[2])

    @check_role_table.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

    def check_member_roles(self, guild: discord.Guild, member: discord.Member, role: discord.Role, *channel: discord.TextChannel):
        if not channel:
            channel = discord.utils.get(guild.text_channels, id = int(json_guilds[str(guild.id)]['bot_channel']))
        else:
            channel = channel[0]
        if role in member.roles:
            self.remove_role(guild, member, role, channel)
        else:
            self.add_role(guild, member, role, channel)

    def remove_role(self, guild: discord.Guild, member: discord.Member, role: discord.Role, channel: discord.TextChannel):
        embed = discord.Embed(colour = 0x7289da)
        embed.add_field(name = '**Roles Updated**', value = f"Role **'{role}'** removed from: {member.mention}", inline = False)
        asyncio.ensure_future(channel.send(embed = embed, delete_after = 5))
        asyncio.ensure_future(member.remove_roles(role))
        self.sql_execute('delete.sql', guild.id, member.id, role.id)

    def add_role(self, guild: discord.Guild, member: discord.Member, role: discord.Role, channel: discord.TextChannel):
        role_name = str(role.name).casefold()
        duration = int(json_roles[role_name]['expiry'])
        expiry = time.time() + duration * 3600
        embed = discord.Embed(colour = 0x7289da)
        embed.add_field(name = "**Roles Updated**", value = f"Role **'{role.name}'** added to: {member.mention}", inline = False)
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
            print(e)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        guild = before.guild
        if guild.id == 253612214148136981:
            before_set = set(before.roles)
            after_set = set(after.roles)
            if not after_set == before_set:
                diff = after_set.symmetric_difference(before_set)
                role = diff.pop()
                self.listener_check_roles(guild, after, role)

    def listener_check_roles(self, guild: discord.Guild, member: discord.Member, role: discord.Role):
        if role in member.roles:
            role_name = str(role.name).casefold()
            duration = int(json_roles[role_name]['expiry']) * 3600
            expiry = time.time() + duration
            cursor.execute("SELECT * FROM role_tracker where guild=? AND member=? AND role=?", (guild.id, member.id, role.id))
            data = cursor.fetchall()
            if not data:
                self.sql_execute('insert.sql', guild.id, member.id, role.id, expiry)
        else:
            self.sql_execute('delete.sql', guild.id, member.id, role.id)

    @commands.command(
        name = 'role',
        description = "Manages various status roles",
        aliases = roles
    )
    async def change_role(self, ctx):
        if ctx.invoked_with in json_roles:
            role_name = ctx.invoked_with.capitalize()
        if ctx.invoked_with in json_content['aliases']:
            role_name = json_content['aliases'][ctx.invoked_with]
        if ctx.invoked_with == 'gabaergic':
            role_name = 'GABAergic'
        role = discord.utils.get(ctx.guild.roles, name = role_name)
        self.check_member_roles(ctx.guild, ctx.author, role, ctx.channel)
        asyncio.ensure_future(ctx.message.delete())

    @commands.command(
        name = 'roles',
        description = "Lists available status roles"
    )
    async def roles(self, ctx):
        embed = discord.Embed(
            title = "Temporary Effect Roles",
            description = "``.tripping`` - For any psychedelic (LSD, mushrooms etc.)\n``.stimmed`` - For any stimulant "
                          "(Cocaine, Adderall etc.)\n``.barred`` - For any benzo (Xanax, Valium etc.)\n``.nodding`` - "
                          "For any opioid (Oxycodone, heroin etc.)\n``.drunk`` For alcohol\n``.dissod`` - For any "
                          "dissociative (Ketamine, DXM etc)\n``.rolling`` For any empathogen (MDMA, "
                          "6-APB etc)\n``.stoned`` - For cannabis\n``.delirious`` - For any deliriant (DPH, "
                          "datura etc)\n``.gabaergic`` - For GABAergics other than alcohol/benzos (Phenibut, "
                          "gabapentin etc)",
            colour = 0x7289da,
            timestamp = datetime.utcnow()
        )
        embed.set_footer(text = "Please use drugs responsibly")
        asyncio.ensure_future(ctx.send(embed = embed))


def setup(bot):
    bot.add_cog(role_tracker(bot))
