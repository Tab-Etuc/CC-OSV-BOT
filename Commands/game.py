import random
import asyncio
from discord.ext import commands
from Commands.games import tictactoe, wumpus, minesweeper, _2048
from Core.classes import Cog_Extension
from discord import Embed
from discord_components import DiscordComponents, Button, ButtonStyle
from asyncio import TimeoutError, sleep
from random import choice
from config import *
import Core.economy
import discord




class Game(Cog_Extension):

    @commands.command(name="θθζ©", aliases=['slots'.casefold(), 'bet'.casefold(), 'slot'.casefold()])
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def _slot(self, ctx):
        emojis = "πππππππππππππ₯­ππ₯ππ₯"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)
        
        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if a == b == c:
            await ctx.send(f"{slotmachine} δΈι£η·οΌδ½ θ΄δΊοΌδ½ θ³Ίε°δΊ**100,000,000εη°‘ζεΉ£** π")
            await Core.economy.update_bank(ctx.author,100000000,"ηΎι")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} δΊι£η·οΌδ½ θ΄δΊοΌπ δ½ θ³Ίε°δΊ**1,000,000εη°‘ζεΉ£**")
            await Core.economy.update_bank(ctx.author,1000000,"ηΎι")
        else:
            await ctx.send(f"{slotmachine} ζ²ζι£η·ηοΌδ½ θΌΈδΊ π’")



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['flip'.casefold(), 'toss'.casefold(), 'cointoss'.casefold()])
    async def _cointoss(self, ctx):
        embed = Embed(
            color=0xF5F5F5,
            title=f"πͺ {ctx.author.name} ζ²η‘¬εΉ£πͺ",
            description="ι»ζζη΄ιΈζζ­£ι’ζει’οΌ",
        )

        menu_components = [
            [
                Button(style=ButtonStyle.grey, label="ζ­£ι’"),
                Button(style=ButtonStyle.grey, label="ει’"),
            ]
        ]
        heads_components = [
            [
                Button(style=ButtonStyle.green, label="ζ­£ι’", disabled=True),
                Button(style=ButtonStyle.red, label="ει’", disabled=True),
            ],
            Button(style=ButtonStyle.blue, label="εη©δΈζ¬‘?", disabled=False),
        ]
        tails_components = [
            [
                Button(style=ButtonStyle.red, label="ζ­£ι’", disabled=True),
                Button(style=ButtonStyle.green, label="ει’", disabled=True),
            ],
            Button(style=ButtonStyle.blue, label="εη©δΈζ¬‘?", disabled=False),
        ]

        if ctx.author.id in self.session_message:
            msg = self.session_message[ctx.author.id]
            await msg.edit(embed=embed, components=menu_components)
        else:
            msg = await ctx.send(embed=embed, components=menu_components)
            self.session_message[ctx.author.id] = msg

        def check(res):
            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=10)
        except TimeoutError:
            await msg.edit(
                embed=Embed(color=0xED564E, title="ζιε°!", description="ζ²ζδΊΊεζγ βΉοΈ"),
                components=[
                    Button(style=ButtonStyle.red, label="ε·²θΆζ!", disabled=True)
                ],
            )
            return

        await res.respond(
            type=7,
            embed=Embed(
                color=0xF5F5F5,
                title=f"πͺ {ctx.author.name}ζ²η‘¬εΉ£ πͺ",
                description=f"δ½ ιΈζδΊ **{res.component.label.lower()}**!",
            ),
            components=menu_components,
        )

        game_choice = choice(["ζ­£ι’", "ει’"])
        await sleep(1)

        if game_choice == res.component.label:
            embed = Embed(
                color=0x65DD65,
                title=f"πͺ {ctx.author.name}ζ²η‘¬εΉ£ πͺ",
                description=f"δ½ ιΈζδΊ **{res.component.label.lower()}**!\n\n> **δ½ θ΄δΊοΌ**δ½ θ³Ίε°δΊ100,000η°‘ζεΉ£γ",
            )
            await Core.economy.update_bank(ctx.author,100000,"ηΎι")
        else:
            embed = Embed(
                color=0xED564E,
                title=f"πͺ {ctx.author.name}ζ²η‘¬εΉ£ πͺ",
                description=f"δ½ ιΈζδΊ **{res.component.label.lower()}**!\n\n> δ½ θΌΈδΊ:(",
            )
            

        await msg.edit(
            embed=embed,
            components=tails_components if game_choice == "ει’" else heads_components,
        )

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=10)
        except TimeoutError:
            await msg.delete()
            del self.session_message[ctx.author.id]
            return

        await res.respond(type=6)
        if res.component.label == "εη©δΈζ¬‘?":
            self.session_message[ctx.author.id] = msg
            await self.cointoss(ctx)



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['nungame'.casefold(), 'num'.casefold()])
    async def _numgame(self, ctx):
      await Core.economy.open_bank(ctx.author)
      await ctx.send('ηδΈεζΈε­ε¨ε£Ήε°ε£Ήδ½°δΉιγ')

      answer = random.randint(1, 100)
      guessnumber = 0

      def guess_check(m):
          return m.content.isdigit() and m.author == ctx.message.author
          
      while guessnumber < 6:
          guessnumber = guessnumber + 1

          try:
              guess = await self.bot.wait_for('message', check=guess_check, timeout=10.0)
          except asyncio.TimeoutError:
              fmt = 'δ½ θ±δΊε€ͺδΉζιδΊγη­ζ‘ζ―{}γ'
              await ctx.send(fmt.format(answer))
              break
          else:
              if int(guess.content) == answer:
                  reward = {1: 10000000, 2: 9900000, 3: 8750000, 4: 7600000, 5: 6450000, 6: 3300000}

                  fmt = "δ½ η­ε°δΊοΌδ½ εηζΈ¬δΊ{}εη­ζ‘γδ½ηΊηε΅οΌδ½ εΎε°{}η°‘ζεΉ£"
                  a = reward[guessnumber]
                  await Core.economy.update_bank(ctx.author,a)
                  await ctx.send(fmt.format(guessnumber,a)) 
                  
              if guessnumber != 6:
                  if int(guess.content) < answer:
                      await ctx.send('`η­ζ‘ει«ι»...`')
                  if int(guess.content) > answer:
                      await ctx.send('`η­ζ‘εδ½ι»...`')

              if guessnumber == 6 and int(guess.content) != answer:
                      fmt = 'δ½ ε¨ε­εζΈε­ε§ζ²ζηζΈ¬ε°η­ζ‘γη­ζ‘ζ― {}γ'
                      await ctx.send(fmt.format(answer))

          if int(guess.content) == answer:
              break
          
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['θΌͺη€','rl'.casefold(), 'roulette'.casefold()])
    async def _roulette(self, ctx):

        answer = None
        while answer not in ('ζ―', 'ε¦'):
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            await webhook.send(
                    'δ½ η’Ίε?θ¦ιιΊΌεεοΌε¦ζδ½ ε€±ζοΌι£ιΊΌδ½ ζζηι’ι½ζζΆε€±γ οΌζ―ζε¦οΌ', 
                    username = 'Λβ ΰ£ͺΒ« δΈ­ε€?ιθ‘ Β» ΰ£ͺ Λ', 
                    avatar_url = 'https://imgur.com/csEpNAa.png', 
                    allowed_mentions = discord.AllowedMentions(
                            everyone = False, 
                            users = False, 
                            roles = False, 
                            replied_user = False
                    )
            )
            await webhook.delete()

            def check(m):
                return m.author == ctx.message.author

            try:
                answer = (await self.bot.wait_for('message', timeout=10.0, check=check))
            except asyncio.TimeoutError:
                webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                await webhook.send(
                        'δ½ θ±δΊε€ͺδΉζιεη­γ', 
                        username = 'Λβ ΰ£ͺΒ« δΈ­ε€?ιθ‘ Β» ΰ£ͺ Λ', 
                        avatar_url = 'https://imgur.com/csEpNAa.png', 
                        allowed_mentions = discord.AllowedMentions(
                                everyone = False, 
                                users = False, 
                                roles = False, 
                                replied_user = False
                        )
                )
                await webhook.delete(); return

            answer = answer.content.lower()

            if answer == 'ζ―':
                await ctx.send(Core.economy.roulette(ctx.message.author))
            elif answer == 'ε¦':  
                webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                await webhook.send(
                        'ε₯½ε= =', 
                        username = 'Λβ ΰ£ͺΒ« δΈ­ε€?ιθ‘ Β» ΰ£ͺ Λ', 
                        avatar_url = 'https://imgur.com/csEpNAa.png', 
                        allowed_mentions = discord.AllowedMentions(
                                everyone = False, 
                                users = False, 
                                roles = False, 
                                replied_user = False
                        )
                )
                await webhook.delete()
            else:
                webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                await webhook.send(
                        'θ«θΌΈε₯βζ―βζβε¦β', 
                        username = 'Λβ ΰ£ͺΒ« δΈ­ε€?ιθ‘ Β» ΰ£ͺ Λ', 
                        avatar_url = 'https://imgur.com/csEpNAa.png', 
                        allowed_mentions = discord.AllowedMentions(
                                everyone = False, 
                                users = False, 
                                roles = False, 
                                replied_user = False
                        )
                )
                await webhook.delete()
                await asyncio.sleep(0.5)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['dice'.casefold()])
    async def _dice(self, ctx, count=None):
        if count == None:
            await ctx.send("θ«θΌΈε₯ζ¬²θ³­δΉιͺ°ε­ι»ζΈγ")
            return
        try:
            count = int(count)
        except:
            await ctx.send('ζΈε­θΌΈε₯ι―θͺ€οΌθ«θΌΈε₯ζ¬²θ³­δΉιͺ°ε­ι»ζΈγ')
        else:
            num = random.randint(1, 6)
            if num == count:
                await ctx.send(f'ιͺ°εΊηζΈε­ηΊ`{num}`οΌδ½ θ΄δΊοΌδ½ η²εΎδΊ1,000,000εη°‘ζεΉ£')
                await Core.economy.update_bank(ctx.author,1000000)
            else:
                await ctx.send(f'ιͺ°εΊηζΈε­ηΊ`{num}`,δ½ θΌΈδΊοΌ')

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='2048')
    async def _2048(self, ctx):
        """Play 2048 game"""
        await _2048.play(ctx, self.bot)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=["8ball".casefold(),])
    async def eight_ball(self, ctx, ques=""):
        """Magic 8Ball"""
        if ques=="":
            await ctx.send("`η¨ζ³οΌC8ball+(ει‘)`")
        else:
            choices = [
            'ε―δ»₯θ―ε?οΌιζ―γ', 'εΎζι‘―γ', 'ζ―«η‘ηεγ', 'ηΆηΆζ―γ',
            'ζ­£ε¦ζζηε°ηοΌζ―ηγ', 'ζζε―θ½ηγ', 'εζ―θ―ε₯½γ', 'ζ―η', 'θ·‘θ±‘θ‘¨ζοΌζ―ηγ',
            'εε₯ε€ͺζ¨‘η³οΌεθ©¦δΈζ¬‘γ', 'η¨εΎεεγ', 'ζε₯½δΈθ¦εθ¨΄δ½ γ', 'ηΎε¨η‘ζ³ι ζΈ¬γ', 'δΈθ¦ζζε?γ', 'ζηεεΎ©ζ―ζ²ζγ', 'ζηζΆζ―δΊΊε£«θͺͺδΈγ', 'ε±ζδΈζ―ι£ιΊΌε₯½γ', 'ιεΈΈε―ηγ'
            ]
            await ctx.send(f":8ball: θͺͺοΌ ||{random.choice(choices)}||(<<θ«ι»ι)")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['ms'.casefold(), 'minesweeper'.casefold()])
    async def _minesweeper(self, ctx, columns = None, rows = None, bombs = None):
        await minesweeper.play(ctx, columns, rows, bombs)
        
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['rockpaperscissors'.casefold(), 'rps'.casefold()])
    async def _rps(self, ctx):
        def check_win(p, b):
            if p=='π':
                return False if b=='π' else True
            if p=='π':
                return False if b=='β' else True
            # p=='β'
            return False if b=='π' else True

        async with ctx.typing():
            reactions = ['π', 'π', 'β']
            game_message = await ctx.send("**εͺεγη³ι ­γεΈ**\nθ«ιΈζοΌ", delete_after=15.0)
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction, user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) == 'π' or 'π' or 'β')
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("ζιε°οΌ:stopwatch:")
        else:
            await ctx.send(f"**:man_in_tuxedo_tone1:\t{reaction.emoji}\n:robot:\t{bot_emoji}**")
            # if conds
            if str(reaction.emoji) == bot_emoji:
                await ctx.send("**εΉ³ζοΌ:ribbon:**")
            elif check_win(str(reaction.emoji), bot_emoji):
                await ctx.send("**δ½ θ΄δΊ :sparkles:**δ½ η²εΎδΊ10,000,000οΌ")
                await Core.economy.update_bank(ctx.author,10000000)
            else:
                await ctx.send("**ζθ΄δΊ :robot:**")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['ttt'.casefold(), 'tictactoe'.casefold()])
    async def _ttt(self, ctx):
        await tictactoe.play_game(self.bot, ctx, chance_for_error=0.2) # Win Plausible

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['wumpus'.casefold()])
    async def _wumpus(self, ctx):
        await wumpus.play(self.bot, ctx)

def setup(bot):
    DiscordComponents(bot)
    bot.add_cog(Game(bot))