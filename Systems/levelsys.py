# Imports
import asyncio
import discord
from discord.ext import commands
from pymongo import MongoClient
import vacefron
import os
from dotenv import load_dotenv
from config import *

# Loads the .env file and gets the required information
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')


cluster = MongoClient(MONGODB_URI)
levelling = cluster['discord']['levelling']

vac_api = vacefron.Client()
Prefix = 'C'

class levelsys(commands.Cog):


    @commands.Cog.listener()
    async def on_message(self, ctx):
        stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
        serverstats = levelling.find_one({"server": ctx.guild.id})
        if not ctx.author.bot:
            if stats is None:
                member = ctx.author
                user = f"<@{member.id}>"
                newuser = {"guildid": ctx.guild.id, "id": ctx.author.id, "tag": user, "xp": serverstats["xp_per_message"], "rank": 1, "background": " ", "circle": False, "xp_colour": "#ffffff", "name": f"{ctx.author}", "pfp": f"{ctx.author.avatar_url}"}
                levelling.insert_one(newuser)
            else:
                if Prefix in ctx.content:
                    stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
                    xp = stats["xp"]
                    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp": xp}})
                else:
                    stats = levelling.find_one({"server": ctx.guild.id})
                    if stats is None:
                        return
                    else:
                        user = ctx.author
                        role = discord.utils.get(ctx.guild.roles, name=serverstats["double_xp_role"])
                    if role in user.roles:
                        stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
                        xp = stats["xp"] + serverstats['xp_per_message'] * 2
                        levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp": xp}})
                    else:
                        stats = levelling.find_one({"guildid": ctx.guild.id, "id": ctx.author.id})
                        xp = stats["xp"] + serverstats['xp_per_message']
                        levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp": xp}})
                lvl = 0
                while True:
                    if xp < ((xp_per_level / 2 * (lvl ** 2)) + (xp_per_level / 2 * lvl)):
                        break
                    lvl += 1
                xp -= ((xp_per_level / 2 * ((lvl - 1) ** 2)) + (xp_per_level / 2 * (lvl - 1)))
                if stats["xp"] < 0:
                    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp": 0}})
                if stats["rank"] != lvl:
                    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"rank": lvl + 1}})
                    embed2 = discord.Embed(title=f":tada: **LEVEL UP!**",
                                           description=f"{ctx.author.mention} 剛才升到了等級： **{lvl}**",
                                           colour=MAIN_COLOR)
                    xp = stats["xp"]
                    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id},
                                         {"$set": {"rank": lvl, "xp": xp + serverstats['xp_per_message'] * 2}})
                    embed2.add_field(name="下個等級：",
                                     value=f"`{int(xp_per_level * 2 * ((1 / 2) * lvl))}xp`")
                    embed2.set_thumbnail(url=ctx.author.avatar_url)
                    member = ctx.author
                    channel = discord.utils.get(member.guild.channels, name=serverstats["level_channel"])
                    msg = await channel.send(embed=embed2)
                    level_roles = serverstats["role"]
                    level_roles_num = serverstats["level"]
                    for i in range(len(level_roles)):
                        if lvl == level_roles_num[i]:
                            await ctx.author.add_roles(
                                discord.utils.get(ctx.author.guild.roles, name=level_roles[i]))
                            embed = discord.Embed(title=":tada: **LEVEL UP**",
                                                  description=f"{ctx.author.mention} 剛才升到了等級： **{lvl}**",
                                                  colour=MAIN_COLOR)
                            embed.add_field(name="下個等級：",
                                            value=f"`{int(xp_per_level * 2 * ((1 / 2) * lvl))}xp`")
                            embed.add_field(name="身分組解鎖", value=f"`{level_roles[i]}`")
                            embed.set_thumbnail(url=ctx.author.avatar_url)
                            await msg.edit(embed=embed)
                        for i in range(len(level_roles)):
                            if lvl == level_roles_num[i]:
                                await ctx.author.add_roles(
                                    discord.utils.get(ctx.author.guild.roles, name=level_roles[i]))
                                embed = discord.Embed(title=":tada: **LEVEL UP**",
                                                      description=f"{ctx.author.mention} 剛才升到了等級： **{lvl}**",
                                                      colour=MAIN_COLOR)
                                embed.add_field(name="下個等級：",
                                                 value=f"`{int(xp_per_level * 2 * ((1 / 2) * lvl))}xp`")
                                embed.add_field(name="身分組解鎖", value=f"`{level_roles[i]}`")
                                embed.set_thumbnail(url=ctx.author.avatar_url)
                                await msg.edit(embed=embed)


def setup(client):
    client.add_cog(levelsys(client))

# End Of Level System
