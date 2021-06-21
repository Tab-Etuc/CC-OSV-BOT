from core.classes import Cog_Extension
import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import random
from config import *
import aiohttp
import requests

class Fun(Cog_Extension):
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def whendie(self, ctx, *, user: discord.Member = None):
        if user == None:
            user = ctx.author

        msg = await ctx.message.reply(embed=discord.Embed(title="看看你多久後會過世......", color=MAIN_COLOR))

        something = [
            f'{random.randint(0, 60)} 秒',
            f'{random.randint(1, 60)} 分鐘',
            f'{random.randint(1, 24)} 小時',
            f'{random.randint(1, 7)} 天',
            f'{random.randint(1, 4)} 週',
            f'{random.randint(1, 100)} 年'
        ]

        thingy = random.choice(something)

        if thingy == something[0]:
            funny_text = "你已經死ㄌ"
            embed_color = RED_COLOR
        if thingy == something[1]:
            funny_text = "你幾乎快死ㄌ"
            embed_color = RED_COLOR
        if thingy == something[2]:
            funny_text = "慟！幽靈正操作著Discord！"
            embed_color = RED_COLOR
        if thingy == something[3]:
            funny_text = "好吧，在你死之前你還有些時間"
            embed_color = ORANGE_COLOR
        if thingy == something[4]:
            funny_text = "你不會那麼早死"
            embed_color = ORANGE_COLOR
        if thingy == something[5]:
            funny_text = "你有很長的壽命！OwO"
            embed_color = MAIN_COLOR

        embed = discord.Embed(
            description = f"{user.mention} 剩**{thingy}**可活",
            color = embed_color,
        )
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text=funny_text)

        await msg.edit(embed=embed)
        
  @commands.command()
  async def owo(self, ctx, *, msg):

        vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

        def last_replace(s, old, new):
            li = s.rsplit(old, 1)
            return new.join(li)

        def text_to_owo(text):
            """ Converts your text to OwO """
            smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

            text = text.replace('L', 'W').replace('l', 'w')
            text = text.replace('R', 'W').replace('r', 'w')

            text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
            text = last_replace(text, '?', '? owo')
            text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

            for v in vowels:
                if 'n{}'.format(v) in text:
                    text = text.replace('n{}'.format(v), 'ny{}'.format(v))
                if 'N{}'.format(v) in text:
                    text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))

            return text

        await ctx.send(text_to_owo(msg))             


  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command(help="展示你有多可愛，我知道你很可愛！")
  async def howcute(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(
            title = "計算你多可愛......",
            color = MAIN_COLOR
        )
        msg1 = await ctx.message.reply(embed=embed)

        cute_number = random.randint(0, 100)

        if 0 <= cute_number <= 20:
            lol = "Damn,你很醜陋!"
            embed_color_uwu = RED_COLOR
        if 20 < cute_number <= 50:
            lol = "還可以。"
            embed_color_uwu = ORANGE_COLOR
        if 50 < cute_number <= 75:
            lol = "你有點可愛， UwU"
            embed_color_uwu = MAIN_COLOR
        if 75 < cute_number <= 100:
            lol = "你很可愛! ><"
            embed_color_uwu = MAIN_COLOR

        embed = discord.Embed(
            title="可愛探測器！",
            description = f"**{user.name}#{user.discriminator}** 的可愛指數是： **{cute_number}%**!",
            color = embed_color_uwu
        )
        embed.set_footer(text=lol)

        await msg1.edit(embed=embed)



  @commands.command()
  async def burn(self, ctx, user: discord.Member = None):
      if user == None:
          user = ctx.author

      burn = Image.open("images/burn.jpg")

      asset = user.avatar_url_as(size = 4096, format="png")
      data = BytesIO(await asset.read())
      profile_pic = Image.open(data)

      profile_pic = profile_pic.resize((342, 342))
      burn.paste(profile_pic, (117, 217))

      burn.save("epic_burn.jpg")

      await ctx.send(file = discord.File("epic_burn.jpg"))


  @commands.command()
  async def trash(self, ctx, user: discord.Member = None):
      if user == None:
          user = ctx.author

      trash = Image.open("images/trash.jpg")

      asset = user.avatar_url_as(size = 4096, format="png")
      data = BytesIO(await asset.read())
      profile_pic = Image.open(data)

      profile_pic = profile_pic.resize((179, 179))
      trash.paste(profile_pic, (374, 66))

      trash.save("epic_trash.jpg")

      await ctx.send(file = discord.File("epic_trash.jpg"))
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def meme(self, ctx):
        embed=discord.Embed(
            title = "哈哈!",
            color = MAIN_COLOR
        )

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def anime(self, ctx):
        response = requests.get("https://shiro.gg/api/images/neko")

        realResponse = response.json()

        embed = discord.Embed(
            title="uwu",
            color=PINK_COLOR_2
        )
        embed.set_image(url=realResponse['url'])

        await ctx.send(embed=embed)

  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command(aliases=['meow', 'cats'])
  async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(
                        title="Meow!", color=MAIN_COLOR)
                    embed.set_image(url=data['file'])

                    await ctx.message.reply(embed=embed)

  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command(aliases=['dogs'])
  async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Woof!", color=MAIN_COLOR)
                    embed.set_image(url=data['url'])

                    await ctx.message.reply(embed=embed)

  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def fox(self, ctx):
        url = "https://randomfox.ca/floof/"
        response = requests.get(url)
        fox = response.json()

        embed = discord.Embed(title="Woof!", color=MAIN_COLOR)
        embed.set_image(url=fox['image'])
        await ctx.message.reply(embed=embed)

  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def panda(self, ctx):
        url = 'https://some-random-api.ml/img/panda'
        response = requests.get(url)
        img = response.json()

        embed = discord.Embed(title="Panda 🐼", color=MAIN_COLOR)
        embed.set_image(url=img['link'])
        await ctx.message.reply(embed=embed)

  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def redpanda(self, ctx):
        url = 'https://some-random-api.ml/img/red_panda'
        response = requests.get(url)
        img = response.json()

        embed = discord.Embed(title="Red Panda", color=MAIN_COLOR)
        embed.set_image(url=img['link'])
        await ctx.message.reply(embed=embed)

  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command(aliases=['pika'])
  async def pikachu(self, ctx):
        url = 'https://some-random-api.ml/img/pikachu'
        response = requests.get(url)
        img = response.json()

        embed = discord.Embed(title="Pika!", color=MAIN_COLOR)
        embed.set_image(url=img['link'])
        await ctx.message.reply(embed=embed)

  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def comment(self, ctx, *, msg=None):
        if msg == None:
            await ctx.message.reply(embed=discord.Embed(
                title="Error!",
                description=f"Incorrect Usage! Use like this: `e!comment <text>`",
                color=RED_COLOR
            ))
            return
        url = f"https://some-random-api.ml/canvas/youtube-comment?avatar={ctx.author.avatar_url_as(format='png')}&username={ctx.author.name}&comment={msg}"
        url = url.replace(" ", "%20")
        embed = discord.Embed(title="comment", color=MAIN_COLOR)
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def wasted(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        url = f"https://some-random-api.ml/canvas/wasted?avatar={user.avatar_url_as(format='png')}"
        embed = discord.Embed(title="wasted!", color=MAIN_COLOR)
        embed.set_image(url=url)
        await ctx.message.reply(embed=embed)

def setup(bot):
   bot.add_cog(Fun(bot))