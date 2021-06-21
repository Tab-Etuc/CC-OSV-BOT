import discord
import requests
from discord.ext.commands import cooldown
from discord.ext import commands

from core.classes import Cog_Extension
from config import *
class NSFW(Cog_Extension):

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def hentai(self, ctx):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            response = requests.get("https://shiro.gg/api/images/nsfw/hentai")

            realResponse = response.json()

            embed = discord.Embed(
                title = "There you go!",
                color = 0xFFC0CB
            )
            embed.set_image(url = realResponse['url'])

            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("這個指令只能用在NSFW頻道。")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def thighs(self, ctx):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            response = requests.get("https://shiro.gg/api/images/nsfw/thighs")

            realResponse = response.json()

            embed = discord.Embed(
                title = "Thighs!",
                color = 0xFFC0CB
            )
            embed.set_image(url = realResponse['url'])

            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("這個指令只能用在NSFW頻道。")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def nekogif(self, ctx):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            response = requests.get("https://nekos.life/api/v2/img/nsfw_neko_gif")

            realResponse = response.json()

            embed = discord.Embed(
                title = "Gifs!",
                color = 0xFFC0CB
            )
            embed.set_image(url = realResponse['url'])

            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("這個指令只能用在NSFW頻道。")

def setup(bot):
    bot.add_cog(NSFW(bot))