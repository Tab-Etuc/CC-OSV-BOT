import discord
import json, datetime
from discord.ext import commands
from core.classes import Cog_Extension
from config import *

SearchData = {
    "search_image": {
        "google": "https://i.imgur.com/bM31b3K.png",
        "wikipedia": "https://i.imgur.com/UMaBtez.png"
    },
    "search_link": {
        "google": "http://www.google.com",
        "wikipedia": "https://zh.wikipedia.org"
    },
    "search_list": [
        "google",
        "wikipedia"
    ],
    "search_name": {
        "google": {
            "en_name": "Google",
            "zh_name": "谷歌"
        },
        "wikipedia": {
            "en_name": "Wikipedia",
            "zh_name": "維基百科"
        }
    },
    "search_prefix": {
        "google": "/search?q=",
        "wikipedia": "/w/index.php?search="
    }
}

def Search(search_type, ctx, arg):
    if search_type in SearchData['search_list']:
        Picture = SearchData['search_image'][search_type]
        en_name = SearchData['search_name'][search_type]['en_name']
        zh_name = SearchData['search_name'][search_type]['zh_name']

        if arg == '':
            Link = SearchData['search_link'][search_type]
            embed=discord.Embed(title=f'{en_name} | {zh_name}', description=f'[Click me | 點我]({Link})', timestamp=datetime.datetime.now(datetime.timezone.utc))
            embed.set_author(name=f'{en_name} Website | {zh_name}主頁', icon_url=Picture)
        else:
            Link = SearchData['search_link'][search_type] + SearchData['search_prefix'][search_type] + arg
            embed=discord.Embed(title=f'{arg}', description=f'[Click me | 點我]({Link})', timestamp=datetime.datetime.now(datetime.timezone.utc))
            embed.set_author(name=f'{en_name} Search | {zh_name}搜尋', icon_url=Picture)

        embed.set_footer(text=f'由{ctx.author}請求的鏈接✨')
        return embed


class search(Cog_Extension):
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['google'.casefold()])
    async def google(self, ctx, arg:str=''):
        await ctx.send(embed=Search('google', ctx, arg))
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['wiki'.casefold(), 'wikipedia'.casefold()])
    async def wiki(self, ctx, arg:str=''):        
        await ctx.send(embed=Search('wikipedia', ctx, arg))

def setup(bot):
    bot.add_cog(search(bot))