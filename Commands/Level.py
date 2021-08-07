import discord
from discord.ext import commands
from Systems.levelsys import levelling
from Systems.levelsys import vac_api
from config import *
from Core.classes import Cog_Extension

class Level(Cog_Extension):

    # Rank Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addxp(self, ctx, xpamount=None, member=None):
        if member is None:
            user = f"<@!{ctx.author.id}>"
        else:
            user = member
        userget = user.replace('!', '')
        stats = levelling.find_one({"guildid": ctx.guild.id, "tag": userget})
        if xpamount:
            xp = stats["xp"]
            levelling.update_one({"guildid": ctx.guild.id, "tag": userget}, {"$set": {"xp": xp + int(xpamount)}})
            embed = discord.Embed(
                    title=":white_check_mark: **已增加XP！**",
                    description=f"已增加`{xpamount}xp` 給： {userget}"
            )
            await ctx.channel.send(embed=embed)
        elif xpamount is None:
            embed3 = discord.Embed(title=":x: **錯誤！**",
                                   description="請確認輸入的值是否為整數。")
            await ctx.channel.send(embed=embed3)
        return

    @commands.command()
    async def background(self, ctx, link=None):
        await ctx.message.delete()
        if link:
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"background": f"{link}"}})
            embed = discord.Embed(title=":white_check_mark: **設定完畢！**",
                                  description="您的個人資料背景已成功設置！如果您的背景尚未更新，請嘗試新圖像。")
            embed.set_thumbnail(url=link)
            await ctx.channel.send(embed=embed)
        elif link is None:
            embed3 = discord.Embed(title=":x: **錯誤！**",
                                   description="請確保你輸入了一個鏈接。")
            await ctx.channel.send(embed=embed3)

    @commands.command()
    async def circlepic(self, ctx, value=None):
        await ctx.message.delete()
        if value == "True":
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"circle": True}})
            embed1 = discord.Embed(title=":white_check_mark: **設定完畢！**",
                                   description="個人資料圓角圖片設置為：`true`。設置為false`以返回默認值。")
            await ctx.channel.send(embed=embed1)
        elif value == "False":
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"circle": False}})
            embed2 = discord.Embed(title=":white_check_mark: **設定完畢！**",
                                   description="個人資料圓角圖片設置為：`false`。設置為'true`將其更改為圓角。")
            await ctx.channel.send(embed=embed2)
        elif value is None:
            embed3 = discord.Embed(title=":x: **錯誤！**",
                                   description="請確保輸入： `True` 或 `False`.")
            await ctx.channel.send(embed=embed3)
        else:
            embed4 = discord.Embed(title = ":x: **錯誤**",
                                    description="請確保輸入： `True` 或 `False`."
            )
            await ctx.channel.send(embed=embed4)

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def doublexp(self, ctx, *, role=None):
        stats = levelling.find_one({"server": ctx.guild.id})
        if stats is None:
            newserver = {"server": ctx.guild.id, "double_xp_role": " "}
            levelling.insert_one(newserver)
        else:
            if role is None:
                embed2 = discord.Embed(title=f":x: 錯誤！",
                                       description=f"你需要輸入一個身分組名稱",
                                       colour=RED_COLOR)
                embed2.add_field(name="範例：", value=f"`{Prefix}doublexp <rolename>`")
                await ctx.send(embed=embed2)
            elif role:
                levelling.update_one({"server": ctx.guild.id}, {"$set": {"double_xp_role": role}})
                embed = discord.Embed(title=f":white_check_mark: 設定完畢！", description=f"新的雙倍經驗值身分組為： `{role}`",
                                      colour=MAIN_COLOR)
                await ctx.send(embed=embed)


    # Leaderboard Command
    @commands.command(aliases=['lb', 'leader', 'rankings'])
    async def leaderboard(self, ctx):
        rankings = levelling.find({"guildid": ctx.guild.id}).sort("xp", -1)
        i = 1
        con = leaderboard_amount
        embed = discord.Embed(title=f":trophy: 排行榜 | Top {con}", colour=MAIN_COLOR = 0xa8e1fa)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["id"])
                tempxp = x["xp"]
                templvl = x["rank"]
                embed.add_field(name=f"#{i}: {temp.name}",
                                value=f"Level: `{templvl}`\n總共 經驗值： `{tempxp}`\n", inline=True)
                embed.set_thumbnail(url=leaderboard_image)
                i += 1
            except:
                pass
            if i == leaderboard_amount + 1:
                break
        await ctx.channel.send(embed=embed)

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def levelchannel(self, ctx, channel=None):
        stats = levelling.find_one({"server": ctx.guild.id})
        if stats is None:
            newserver = {"server": ctx.guild.id, "level_channel": " "}
            levelling.insert_one(newserver)
        else:
            if channel is None:
                embed2 = discord.Embed(title=f":x: 錯誤！",
                                       description=f"您需要輸入頻道名稱！",
                                       colour=RED_COLOR)
                embed2.add_field(name="範例:", value=f"`{Prefix}levelchannel <channelname>`\n\n*** 請勿輸入 # 或任何 -'s! ({Prefix}levelchannel test-channel)***")
                await ctx.send(embed=embed2)
            elif channel:
                levelling.update_one({"server": ctx.guild.id}, {"$set": {"level_channel": channel}})
                embed = discord.Embed(title=f":white_check_mark: 設定完畢！",
                                      description=f"頻道變更為: `{channel}`",
                                      colour=MAIN_COLOR)
                await ctx.send(embed=embed)


    # Rank Command
    @commands.command(aliases=['r', 'level', 'l', 'stats', 'xp', 'progress'])
    async def rank(self, ctx, member=None):
        if member is None:
            user = f"<@!{ctx.author.id}>"
        else:
            user = member
        userget = user.replace('!', '')
        stats = levelling.find_one({"guildid": ctx.message.guild.id, "tag": userget})
        if stats is None:
            embed = discord.Embed(description=":x: 找不到此數據！",
                                  colour=RED_COLOR)
            await ctx.channel.send(embed=embed)
        else:
            xp = stats["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((xp_per_level / 2 * (lvl ** 2)) + (xp_per_level / 2 * lvl)):
                    break
                lvl += 1
            xp -= ((xp_per_level / 2 * (lvl - 1) ** 2) + (xp_per_level / 2 * (lvl - 1)))
            rankings = levelling.find({"guildid": ctx.guild.id}).sort("xp", -1)
            for x in rankings:
                rank += 1
                if stats["id"] == x["id"]:
                    break
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id},
                                 {'$set': {"pfp": f"{ctx.author.avatar_url}", "name": f"{ctx.author}"}})
            stats2 = levelling.find_one({"guildid": ctx.message.guild.id, "tag": userget})
            background = stats2["background"]
            circle = stats2["circle"]
            xpcolour = stats2["xp_colour"]
            member = ctx.author
            gen_card = await vac_api.rank_card(
                username=str(stats2['name']),
                avatar=stats['pfp'],
                level=int(lvl),
                rank=int(rank),
                current_xp=int(xp),
                next_level_xp=int(xp_per_level * 2 * ((1 / 2) * lvl)),
                previous_level_xp=0,
                xp_color=str(xpcolour),
                custom_background=str(background),
                is_boosting=bool(member.premium_since),
                circle_avatar=circle
            )
            embed = discord.Embed(colour=MAIN_COLOR)
            embed.set_image(url=gen_card.url)
            await ctx.send(embed=embed)      

    # Rank Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removexp(self, ctx, xpamount=None, member=None):
        if member is None:
            user = f"<@!{ctx.author.id}>"
        else:
            user = member
        userget = user.replace('!', '')
        stats = levelling.find_one({"guildid": ctx.guild.id, "tag": userget})
        if xpamount:
            xp = stats["xp"]
            levelling.update_one({"guildid": ctx.guild.id, "tag": userget}, {"$set": {"xp": xp - int(xpamount)}})
            embed = discord.Embed(title=":white_check_mark: **執行完畢!**",
                                  description=f"已移除 `{xpamount}xp` 從： {userget}")
            await ctx.channel.send(embed=embed)
        elif xpamount is None:
            embed3 = discord.Embed(title=":x: **錯誤！**",
                                   description="請確保輸入整數。")
            await ctx.channel.send(embed=embed3)
        return                                

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx, user=None):
        if user:
            userget = user.replace('!', '')
            levelling.delete_one({"guildid": ctx.guild.id, "tag": userget})
            embed = discord.Embed(title=f":white_check_mark: 重置用戶", description=f"{user}",
                                  colour=MAIN_COLOR)
            print(f"{userget} was reset!")
            await ctx.send(embed=embed)
        else:
            embed2 = discord.Embed(title=f":x: 錯誤",
                                   description=f"無法執行! `{user}` 不存在，或者你沒有提及用戶！",
                                   colour=RED_COLOR)
            embed2.add_field(name="範例:", value=f"`{Prefix}reset` {ctx.message.author.mention}")
            await ctx.send(embed=embed2)

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, addorremove=None, levels=None, *, rolez=None):
        stats = levelling.find_one({"server": ctx.guild.id})
        if stats is None:
            newserver = {"server": ctx.guild.id, f"role": " ", "level": 0}
            levelling.insert_one(newserver)
        if addorremove is None:

            embed2 = discord.Embed(title=f":x: 錯誤",
                                   description=f"您需要定義是否要添加或刪除身分組！",
                                   colour=RED_COLOR)
            embed2.add_field(name="範例:", value=f"`{prefix}role <add|remove> <level> <rolename>`")
            await ctx.send(embed=embed2)
        else:
            if addorremove == "add":
                if levels is None:
                    embed2 = discord.Embed(title=f":x: 錯誤",
                                           description=f"您需要定義用戶將解鎖身分組的級別！",
                                           colour=RED_COLOR)
                    embed2.add_field(name="範例:", value=f"`{prefix}role <add|remove> <level> <rolename>`")
                    await ctx.send(embed=embed2)
                    return
                else:
                    roles.append(str(rolez))
                    if rolez is None:
                        embed2 = discord.Embed(title=f":x: 錯誤",
                                               description=f"您需要定義用戶解鎖的身分組！",
                                               colour=RED_COLOR)
                        embed2.add_field(name="範例", value=f"`{prefix}role <add|remove> <level> <rolename>`")
                        await ctx.send(embed=embed2)
                        return
                    else:
                        level.append(int(levels))

                        levelling.update_one({"server": ctx.guild.id}, {"$set": {f"role": roles, "level": level}})
                        embed = discord.Embed(title=f":white_check_mark: 設定完畢！",
                                              description=f"以新增身分組`{rolez}`在等級: `{levels}`",
                                              colour=MAIN_COLOR)
                        await ctx.send(embed=embed)
            elif addorremove == "remove":
                if rolez is None:
                    embed2 = discord.Embed(title=f":x: 錯誤",
                                           description=f"您需要定義身分組名稱!",
                                           colour=RED_COLOR)
                    embed2.add_field(name="範例", value=f"`{prefix}role <add|remove> <levele> <rolename>`")
                    await ctx.send(embed=embed2)
                    return
                else:
                    roles.remove(str(rolez))
                    if levels is None:
                        embed2 = discord.Embed(title=f":x: 錯誤",
                                               description=f"您需要定義用戶解鎖身分組的級別！",
                                               colour=RED_COLOR)
                        embed2.add_field(name="範例", value=f"`{prefix}role <add|remove> <rolename> <level>`")
                        await ctx.send(embed=embed2)
                        return
                    else:
                        level.remove(int(levels))
                        stats = levelling.find_one({"server": ctx.guild.id})
                        levelling.update_one({"server": ctx.guild.id}, {"$set": {"role": roles, "level": level}})
                        await ctx.send(f"{addorremove} and {rolez} and {levels}")
                        embed = discord.Embed(title=f":white_check_mark: 設定完畢！",
                                              description=f"已移除身分組： `{rolez}` 在等級: `{levels}`",
                                              colour=MAIN_COLOR)
                        await ctx.send(embed=embed)
                return            

    @commands.command()
    async def xpcolour(self, ctx, colour=None):
        await ctx.message.delete()
        if colour:
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp_colour": f"{colour}"}})
            embed = discord.Embed(title=":white_check_mark: **設定完畢！**",
                                  description=f"你的經驗值顏色已更改。如果你輸入 `{Prefix}rank` 然後沒有任何改變，請嘗試新的十六進制編碼(hex)。\n**範例**:\n*#0000FF* = *藍*")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/812895798496591882/825363205853151252/ML_1.png")
            await ctx.send(embed=embed)
        elif colour is None:
            embed = discord.Embed(title=":x: **錯誤!**",
                                  description="請確保有輸入十六進制代碼(hex)！")
            await ctx.send(embed=embed)
            return                      

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def xppermessage(self, ctx, xp=None):
        stats = levelling.find_one({"server": ctx.guild.id})
        if stats is None:
            newserver = {"server": ctx.guild.id, "xp_per_message": 10}
            levelling.insert_one(newserver)
        else:
            if xp is None:
                embed2 = discord.Embed(title=f":x: 錯誤",
                                       description=f"你需要輸入XP的數量！",
                                       colour=RED_COLOR)
                embed2.add_field(name="範例", value=f"`{Prefix}xppermessage <amount>`")
                await ctx.send(embed=embed2)
            elif xp:
                levelling.update_one({"server": ctx.guild.id}, {"$set": {"xp_per_message": int(xp)}})
                embed = discord.Embed(title=f":white_check_mark: 設定完畢！", description=f"現在每條消息XP：`{xp}`",
                                      colour=MAIN_COLOR)
                await ctx.send(embed=embed)            

def setup(bot):
    bot.add_cog(Level(bot))











