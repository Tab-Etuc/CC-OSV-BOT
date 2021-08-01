import random
import asyncio
from discord.ext import commands
from Commands.games import tictactoe, wumpus, minesweeper, 2048
from core.classes import Cog_Extension
from discord import Embed
from discord_components import DiscordComponents, Button, ButtonStyle
from asyncio import TimeoutError, sleep
from random import choice
from config import *
import core.economy
import json




class Game(Cog_Extension):

    @commands.command(name="老虎機", aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        emojis = "🍏🍎🍐🍊🍋🍌🍉🍇🍓🍈🍒🍑🥭🍍🥝🍅🥑"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)
        
        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if a == b == c:
            await ctx.send(f"{slotmachine} 一連線，你贏了！你賺到了**100,000,000元簡明幣** 🎉")
            await core.economy.update_bank(ctx.author,100000000,"現金")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 二連線，你贏了！🎉 你賺到了**1,000,000元簡明幣**")
            await core.economy.update_bank(ctx.author,1000000,"現金")
        else:
            await ctx.send(f"{slotmachine} 沒有連線的，你輸了 😢")



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='toss', aliases=['flip'])
    async def cointoss(self, ctx):
        embed = Embed(
            color=0xF5F5F5,
            title=f"🪙 {ctx.author.name} 擲硬幣🪙",
            description="點擊按紐選擇正面或反面！",
        )

        menu_components = [
            [
                Button(style=ButtonStyle.grey, label="正面"),
                Button(style=ButtonStyle.grey, label="反面"),
            ]
        ]
        heads_components = [
            [
                Button(style=ButtonStyle.green, label="正面", disabled=True),
                Button(style=ButtonStyle.red, label="反面", disabled=True),
            ],
            Button(style=ButtonStyle.blue, label="再玩一次?", disabled=False),
        ]
        tails_components = [
            [
                Button(style=ButtonStyle.red, label="正面", disabled=True),
                Button(style=ButtonStyle.green, label="反面", disabled=True),
            ],
            Button(style=ButtonStyle.blue, label="再玩一次?", disabled=False),
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
                embed=Embed(color=0xED564E, title="時間到!", description="沒有人回應。 ☹️"),
                components=[
                    Button(style=ButtonStyle.red, label="已超時!", disabled=True)
                ],
            )
            return

        await res.respond(
            type=7,
            embed=Embed(
                color=0xF5F5F5,
                title=f"🪙 {ctx.author.name}擲硬幣 🪙",
                description=f"你選擇了 **{res.component.label.lower()}**!",
            ),
            components=menu_components,
        )

        game_choice = choice(["正面", "反面"])
        await sleep(1)

        if game_choice == res.component.label:
            embed = Embed(
                color=0x65DD65,
                title=f"🪙 {ctx.author.name}擲硬幣 🪙",
                description=f"你選擇了 **{res.component.label.lower()}**!\n\n> **你贏了！**你賺到了100,000簡明幣。",
            )
            await core.economy.update_bank(ctx.author,100000,"現金")
        else:
            embed = Embed(
                color=0xED564E,
                title=f"🪙 {ctx.author.name}擲硬幣 🪙",
                description=f"你選擇了 **{res.component.label.lower()}**!\n\n> 你輸了:(",
            )
            

        await msg.edit(
            embed=embed,
            components=tails_components if game_choice == "反面" else heads_components,
        )

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=10)
        except TimeoutError:
            await msg.delete()
            del self.session_message[ctx.author.id]
            return

        await res.respond(type=6)
        if res.component.label == "再玩一次?":
            self.session_message[ctx.author.id] = msg
            await self.cointoss(ctx)



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='numgame', aliases=['nungame','num', 'NUNGAME'])
    async def numgame(self, ctx):
      await core.economy.open_bank(ctx.author)
      await ctx.send('猜一個數字在壹到壹佰之間。')

      answer = random.randint(1, 100)
      guessnumber = 0

      def guess_check(m):
          return m.content.isdigit() and m.author == ctx.message.author
          
      while guessnumber < 6:
          guessnumber = guessnumber + 1

          try:
              guess = await self.bot.wait_for('message', check=guess_check, timeout=10.0)
          except asyncio.TimeoutError:
              fmt = '你花了太久時間了。答案是{}。'
              await ctx.send(fmt.format(answer))
              break
          else:
              if int(guess.content) == answer:
                  reward = {1: 10000000, 2: 9900000, 3: 8750000, 4: 7600000, 5: 6450000, 6: 3300000}

                  fmt = "你答對了！你僅猜測了{}個答案。作為獎勵，你得到{}簡明幣"
                  a = reward[guessnumber]
                  await core.economy.update_bank(ctx.author,a)
                  await ctx.send(fmt.format(guessnumber,a)) 
                  
              if guessnumber != 6:
                  if int(guess.content) < answer:
                      await ctx.send('`答案再高點...`')
                  if int(guess.content) > answer:
                      await ctx.send('`答案再低點...`')

              if guessnumber == 6 and int(guess.content) != answer:
                      fmt = '你在六個數字內沒有猜測到答案。答案是 {}。'
                      await ctx.send(fmt.format(answer))

          if int(guess.content) == answer:
              break
          
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='roulette', aliases=['輪盤','RL'])
    async def roulette(self, ctx):

        answer = None
        while answer not in ('是', '否'):
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            await webhook.send(
                    '你確定要這麼做嗎？如果你失手，那麼你所有的錢都會消失。 （是或否）', 
                    username = '˚₊ ࣪« 中央銀行 » ࣪ ˖', 
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
                        '你花了太久時間回答。', 
                        username = '˚₊ ࣪« 中央銀行 » ࣪ ˖', 
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

            if answer == '是':
                await ctx.send(core.economy.roulette(ctx.message.author))
            elif answer == '否':  
                webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                await webhook.send(
                        '好喔= =', 
                        username = '˚₊ ࣪« 中央銀行 » ࣪ ˖', 
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
                        '請輸入“是”或“否”', 
                        username = '˚₊ ࣪« 中央銀行 » ࣪ ˖', 
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
    @commands.command(aliases=['DICE', 'Dice'])
    async def dice(self, ctx, count=None):
        if count == None:
            await ctx.send("請輸入欲賭之骰子點數。")
            return
        try:
            count = int(count)
        except:
            await ctx.send('數字輸入錯誤，請輸入欲賭之骰子點數。')
        else:
            num = random.randint(1, 6)
            if num == count:
                await ctx.send(f'骰出的數字為`{num}`，你贏了！你獲得了1,000,000元簡明幣')
                await core.economy.update_bank(ctx.author,1000000)
            else:
                await ctx.send(f'骰出的數字為`{num}`,你輸了！')

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='2048')
    async def 2048(self, ctx):
        """Play 2048 game"""
        await 2048.play(ctx, self.bot)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=["8ball","8BALL"])
    async def eight_ball(self, ctx, ques=""):
        """Magic 8Ball"""
        if ques=="":
            await ctx.send("`用法：C8ball+(問題)`")
        else:
            choices = [
            '可以肯定，這是。', '很明顯。', '毫無疑問。', '當然是。',
            '正如我所看到的，是的。', '最有可能的。', '前景良好。', '是的', '跡象表明，是的。',
            '問句太模糊，再試一次。', '稍後再問。', '最好不要告訴你。', '現在無法預測。', '不要指望它。', '我的回復是沒有。', '我的消息人士說不。', '展望不是那麼好。', '非常可疑。'
            ]
            await ctx.send(f":8ball: 說： ||{random.choice(choices)}||(<<請點開)")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='minesweeper', aliases=['ms'])
    async def minesweeper(self, ctx, columns = None, rows = None, bombs = None):
        await minesweeper.play(ctx, columns, rows, bombs)
        
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='rps', aliases=['rockpaperscissors'])
    async def rps(self, ctx):
        def check_win(p, b):
            if p=='🌑':
                return False if b=='📄' else True
            if p=='📄':
                return False if b=='✂' else True
            # p=='✂'
            return False if b=='🌑' else True

        async with ctx.typing():
            reactions = ['🌑', '📄', '✂']
            game_message = await ctx.send("**剪刀、石頭、布**\n請選擇：", delete_after=15.0)
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction, user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) == '🌑' or '📄' or '✂')
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("時間到！:stopwatch:")
        else:
            await ctx.send(f"**:man_in_tuxedo_tone1:\t{reaction.emoji}\n:robot:\t{bot_emoji}**")
            # if conds
            if str(reaction.emoji) == bot_emoji:
                await ctx.send("**平手！:ribbon:**")
            elif check_win(str(reaction.emoji), bot_emoji):
                await ctx.send("**你贏了 :sparkles:**你獲得了10,000,000！")
                await core.economy.update_bank(ctx.author,10000000)
            else:
                await ctx.send("**我贏了 :robot:**")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='tictactoe', aliases=['ttt'])
    async def ttt(self, ctx):
        await tictactoe.play_game(self.bot, ctx, chance_for_error=0.2) # Win Plausible

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='wumpus', aliases=['WUMPUS', 'Wumpus'])
    async def _wumpus(self, ctx):
        await wumpus.play(self.bot, ctx)

def setup(bot):
    DiscordComponents(bot)
    bot.add_cog(Game(bot))