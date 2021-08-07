import discord, os, asyncio, random, Core.economy, Core.Miner
from discord.ext import commands
from Core.classes import Cog_Extension
from config import *
from pymongo import MongoClient

auth_url = os.getenv("MONGODB_URI")

class Mine_GUI():
    def __int__(self, layer, page):
        self.layer = layer
        self.page = page

    def layer_1_embed(self):
        self.layer = 1
        self.page = 1
        embed_top = discord.Embed(color=MAIN_COLOR, description="឵឵\n\n功能：")
        embed_top.set_thumbnail(url="https://cdn.discordapp.com/attachments/851788198467338242/866652093263511612/text-mining-icon-2793702_960_720.png")
        embed_top.set_author(name="水月礦場 前導介面")
        embed_top.set_image(url="https://cdn.discordapp.com/attachments/851788198467338242/866935632939712533/1.png")
        embed_top.set_footer(text="招募工人")
        embed_2 = discord.Embed(color=MAIN_COLOR)
        embed_2.set_image(url="https://cdn.discordapp.com/attachments/851788198467338242/866935313217355786/lk1.png")
        embed_2.set_footer(text="升級工人裝備")
        embed_3 = discord.Embed(color=MAIN_COLOR)
        embed_3.set_image(url="https://cdn.discordapp.com/attachments/851788198467338242/866935350478897162/-1.png")
        embed_3.set_footer(text="精煉所")
        return [embed_top, embed_2, embed_3]

class Miner():
    async def play(ctx, bot):
            Miner = "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟧🟧🟧🟥🟥"
            a = random.choice(Miner)
            b = random.choice(Miner)
            c = random.choice(Miner)
            d = random.choice(Miner)
            e = random.choice(Miner)
            board = [
                [a, b, c, d, e],
            ]
            await ctx.send(
                "如果十五秒內未收到回應，此次紀錄將被捨棄。"
            )
            
            message = await ctx.send(f"`{Miner.print_board(board)}`")
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
            await message.add_reaction("5️⃣")
            def check(reaction, user):
                return (
                    (user.id == ctx.author.id)
                    and (str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"])
                    and (reaction.message.id == message.id)
                )

            while True:
                try:
                    reaction, user = await bot.wait_for(
                        "reaction_add", check=check, timeout=15.0
                    )
                except asyncio.TimeoutError:
                    await ctx.send("已超時！:stopwatch:")
                    await message.delete()
                    return
                else:
                    try:
                        await message.remove_reaction(str(reaction.emoji), ctx.author)
                    except discord.errors.Forbidden:
                        pass
                    users = await Core.economy.get_bank_data()
                    if str(reaction.emoji) == "1️⃣":
                        月薪 = 22000
                        扣錢 = 500000
                        choose = a
                        if users[0] < 月薪:
                            await ctx.send(f"你的現金餘額不足**{扣錢}，這代表你無法雇用這名工人。")
                    elif str(reaction.emoji) == "2️⃣":
                        choose = b
                        月薪 = 50000
                        扣錢 = 100000
                        if users[0] < 月薪:
                            await ctx.send(f"你的現金餘額不足**{扣錢}，這代表你無法雇用這名工人。")                    
                    elif str(reaction.emoji) == "3️⃣":
                        choose = c
                        月薪 = 2000000
                        扣錢 = 5000000
                        if users[0] < 月薪:
                            await ctx.send(f"你的現金餘額不足**{扣錢}，這代表你無法雇用這名工人。")                    
                    elif str(reaction.emoji) == "4️⃣":
                        choose = d
                        月薪 = 88888888
                        扣錢 = 3000000000
                        if users[0] < 月薪:
                            await ctx.send(f"你的現金餘額不足**{扣錢}，這代表你無法雇用這名工人。")                    
                    elif str(reaction.emoji) == "5️⃣":
                        choose = e
                        月薪 = 8031135585
                        扣錢 = 8031135585496
                        if users[0] < 月薪:
                            await ctx.send(f"你的現金餘額不足**{扣錢}，這代表你無法雇用這名工人。")                    
                    if str(choose) == "⬜":
                        品階 = "N工人"
                    elif str(choose) == "🟩":
                        品階 = "R工人"                      
                    elif str(choose) == "🟨":
                        品階 = "SR工人"        
                    elif str(choose) == "🟧":
                        品階 = "SSR工人"        
                    elif str(choose) == "🟥":
                        品階 = "UR工人"    
                    await ctx.send(f"你已雇用了**{品階}等級**的工人，花費了**{扣錢}元**。且其月薪為**{月薪}**元")    
                    await Core.economy.update_bank(ctx.author,扣錢)
                    await Core.Miner.set.miner(ctx.author,1,品階)

    def print_board(board):
            col_width = max(len(str(word)) for row in board for word in row) + 2  # padding
            whole_thing = ""
            for row in board:
                whole_thing += "".join(str(word).ljust(col_width) for word in row) + "\n"
            return whole_thing  


class Mine(Cog_Extension):
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['m'])
    async def mine(self, ctx, commands = None):
        await Core.Miner.open_mine(ctx.author)
        await Core.economy.open_bank(ctx.author)
        if commands is None:
            embeds = Mine_GUI()
            embeds = embeds.layer_1_embed()
            for embed in embeds:
                message = await ctx.send(embed=embed, delete_after=7.0)
            reactions = ['👨', '⛏️', '🔥']
            for reaction in reactions:
                await message.add_reaction(reaction)

            def check(reaction, user):
                return user != self.bot.user and user == ctx.author and (str(reaction.emoji) == '👨' or '⛏️', '🔥')
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=7.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("已超時！:stopwatch:")
            else:
                if str(reaction.emoji) == '👨':
                    Miner(ctx, self.bot)
                elif str(reaction.emoji) == '⛏️':
                    await ctx.send("Done2")
                elif str(reaction.emoji) == '🔥':
                    await ctx.send("Done3")
                return
        if commands is not None:
            if commands.lower() == '招募':
                Miner.play(ctx, self.bot)

                
def setup(bot):
    bot.add_cog(Mine(bot))