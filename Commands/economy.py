#匯入模組
import discord
from discord.ext import commands
import os, random, math, time, datetime, asyncio
from pymongo import MongoClient
from Core.classes import Cog_Extension
import Core.economy
from config import *
from Core.economy import *
import requests



auth_url = os.getenv('MONGODB_URI') #匯入MongoDB之資料庫連結
cluster = MongoClient(auth_url)
db = cluster['Economy']
cursor = db['Bank']

class Economy(Cog_Extension):  

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=['count'.casefold()])
    async def _count(self, ctx):
      filter = {'真人':'True'}

      user = cursor.count_documents(filter)
      webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
      await webhook.send(
        f'已經有{user}位國民已開戶。', 
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



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=['top'.casefold()])
    async def _top(self, ctx):
      data = []
      index = 1

      mydoc = cursor.find().sort('銀行餘額',-1)
      
      for member in mydoc:
        if index > 8:
            break
        
        member_name = self.bot.get_user(member['_id'])
        member_amt = member['銀行餘額']
        member_amt2 = member['現金']
        tatal = member_amt + member_amt2

        if index == 1:
            msg1 = f'**🥇 `{member_name}` -- {tatal}**'
            data.append(msg1)

        if index == 2:
            msg2 = f'**🥈 `{member_name}` -- {tatal}**'
            data.append(msg2)

        if index == 3:
            msg3 = f'**🥉 `{member_name}` -- {tatal}**\n'
            data.append(msg3)

        if index >= 4:
            members = f'**{index} `{member_name}` -- {tatal}**'
            data.append(members)
        index += 1

      msg = '\n'.join(data)

      embed = discord.Embed(
          title=f'頂尖 {index-1}位 最富有的國民 - 排行榜 ',
          description=f'它基於全國國民的淨資產（現金+銀行餘額）||其實還沒寫好，只有銀行餘額|| \n\n{msg}',
          color=MAIN_COLOR,
          timestamp=datetime.datetime.utcnow()
      )
      embed.set_footer(text=f'全國 - {ctx.guild.name}')

      webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
      
      await webhook.send(
          embed=embed,
          username = '˚₊ ࣪« 中央銀行 » ࣪ ˖', 
          avatar_url = 'https://imgur.com/csEpNAa.png', 
          allowed_mentions=discord.AllowedMentions(
              everyone=False, 
              users=False, 
              roles=False, 
              replied_user=False
              )
      )
      await webhook.delete()



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['bag'.casefold()])
    async def _bag(self, ctx):
      await Core.economy.open_account(ctx.author)
      users = await Core.economy.get_bag_data()

      try:
          bag = users[str(ctx.author.id)]['bag']
      except:
          bag = []

      embed = discord.Embed(
        title = f'{ctx.author}的背包',
        color = MAIN_COLOR
      )
      for item in bag:
          name = item['item']
          amount = item['amount']

          embed.add_field(
            name = name, 
            value = amount
          )    
      webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")

      await webhook.send(
        embed=embed, 
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



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['buy'.casefold()])
    async def _buy(self, ctx, item, amount = 1):
        await Core.economy.open_account(ctx.author)
        res = await Core.economy.buy_this(
          ctx.message.author,
          item,
          amount,
          ctx.author
        )

        if not res[0]: #自訂報錯
          if res[1]==1: #當沒有這項物品
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            embed = discord.Embed(
                title = ':warning: 錯誤！', 
                description = f'{ctx.author.mention} 並沒有這項物品：`{item}`', 
                color = ORANGE_COLOR
            )
            await webhook.send(
                embed = embed, 
                username = '˚₊ ࣪« 中央銀行 » ࣪ ˖', 
                avatar_url = 'https://imgur.com/csEpNAa.png', 
                allowed_mentions=discord.AllowedMentions(
                  everyone = False, 
                  users = False, 
                  roles = False, 
                  replied_user = False
                )
            )
            await webhook.delete(); return

          if res[1]==2: #當餘額不足
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            embed=discord.Embed(
                title = ':warning: 錯誤！', 
                description = f'{ctx.author.mention} 你沒有足夠的錢購買{amount}個`{item}`。', 
                color=ORANGE_COLOR
            )
            await webhook.send(
                embed = embed, 
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

          if res[1]==3: #當已買過此商品
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            embed = discord.Embed(
                title = ':warning: 錯誤！', 
                description = f'{ctx.author.mention} 你已經購買過`{item}`了。', 
                color = ORANGE_COLOR
            )
            await webhook.send(
                embed = embed, 
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

        webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
        embed = discord.Embed(
            title = '<a:V_:858154997640331274> 成功執行！', 
            description = f'{ctx.author.mention} 你剛買了{amount}個`{item}`。', 
            color = MAIN_COLOR
        )
        await webhook.send(
            embed = embed, 
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

        
        #購買物品後給予身分組
        guild = self.bot.get_guild(833942312018771989)
        if 'luckyclover' in str(item): 
            role = guild.get_role(852083684685119488)
        elif 'watch' in str(item): 
            role = guild.get_role(852049088395476992)
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            await webhook.send(
                f'{ctx.author.mention} `你已解鎖 <#852364573095755808> 頻道(最上方)。`', 
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
        elif 'name' in str(item): 
            role =guild.get_role(852084041192964096)  
        elif 'BG' in str(item): 
            role =guild.get_role(854580418632351804)
        await ctx.message.author.add_roles(role)   #添加身分組       



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=['rb'.casefold(), 'rob'.casefold()])
    async def _rob(self, ctx,member : discord.Member): 
      if member == ctx.author: #當member = 使用者本人
        webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
        embed=discord.Embed(
            title = ':warning: 錯誤！', 
            description = f'{ctx.author.mention} `自己搶自己並不會憑空冒出多的錢。`', 
            color=ORANGE_COLOR
        )
        await webhook.send(
          embed = embed, 
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

      embed_ = await Core.economy.loading(ctx)  #發送Loading訊息
      
      await Core.economy.open_bank(ctx.author)
      await Core.economy.open_bank(member)
      bal = await Core.economy.get_bank_data(member)
      data = await Core.economy.get_bank_data(ctx.author)
      timeleft = int(time.time()-data[8])
      timeleft = 86400 - timeleft

      
      if timeleft > 0:  #給予時間單位，小於60-->秒，60~3599-->分鐘，大於3600-->小時
            typeT = '秒'
            if timeleft > 60 and timeleft < 3600:
                timeleft = timeleft // 60
                typeT = '分鐘'

            elif timeleft >=3600:
              timeleft = timeleft // 3600
              typeT= '小時'
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            embed=discord.Embed(
                title = ':warning: 錯誤！', 
                description = f'{ctx.author.mention} 你仍需等待{timeleft}{typeT}！', 
                color = ORANGE_COLOR
            )
            await webhook.send(
                embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook


      if bal[0]<100:    #當現金小於100，則報錯
          webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
          embed=discord.Embed(
              title = ':warning: 錯誤！', 
              description = f'{ctx.author.mention} 搶他也沒用 <:E38:847443949441646592>\n {member}剩沒有多少現金了。', 
              color = ORANGE_COLOR
          )
          await webhook.send(
              embed = embed, 
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
          await embed_[0].delete() #刪除loading訊息
          await embed_[1].delete(); return #刪除先前創建之Webhook

          

      earning = random.randrange(0, bal[0])

      await Core.economy.update_bank(ctx.author, earning)
      await Core.economy.update_bank(member, -1*earning)
      await Core.economy.update_set_bank(ctx.author, data[8], 'Rob')
      webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
      embed=discord.Embed(
          title = '<a:V_:858154997640331274> 成功執行！',
          description = f'{ctx.author}已搶了{member} **{earning}** 元！', 
          color = MAIN_COLOR
      )
      await webhook.send(
          embed = embed, 
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
      await embed_[0].delete
      await embed_[1].delete(); return #刪除先前創建之Webhook



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def 國庫(self, ctx):
      embed_ = await Core.economy.loading(ctx)  #發送Loading訊息
      users = await Core.economy.get_國庫()

      embed = discord.Embed(
          title = '國庫'
      )
      embed.add_field(
          name = '餘額：', 
          value = f'**{int(users[1])}**',
          inline=True
      )
      embed.add_field(
          name = '當周所得：', 
          value = f'**{int(users[0]) }**',
          inline=True
      )
      webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
      await webhook.send(
          embed = embed, 
          username = '˚₊ ࣪« 中央銀行 » ࣪ ˖', 
          avatar_url = 'https://imgur.com/csEpNAa.png', 
          allowed_mentions = discord.AllowedMentions(
              everyone = False, 
              users = False, 
              roles = False, 
              replied_user = False
          )
      )
      await embed_[0].delete() #刪除loading訊息 
      await embed_[1].delete() #刪除先前創建之Webhook
     


    @commands.cooldown(1, 10, commands.BucketType.user)     
    @commands.command(aliases=['bank'.casefold(), 'profile'.casefold(), 'p'])
    @commands.guild_only()
    async def _profile(self, ctx, regi: discord.Member = None):
        embed_ = await Core.economy.loading(ctx)  #發送Loading訊息        
                                        
        if (regi is not None and regi.bot) or ctx.author.bot: #偵測用戶提及之(regi)是否為BOT
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            embed = discord.Embed(
                    title = ':warning: 錯誤！', 
                    description = f'{ctx.author.mention} 該用戶是一個BOT，不能擁有一個帳戶', 
                    color = ORANGE_COLOR
            )
            await webhook.send(
                    embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook

        elif not regi: #沒有提及人，即查看自己
                await Core.economy.open_bank(ctx.author)
                users = await Core.economy.get_bank_data(ctx.author)
                利息等階_data = await Core.economy.利息_data(int(users[7]))
                存額等階_data = await Core.economy.存額_data(int(users[6]))

                embed = discord.Embed(
                        title = '一般用戶', 
                        color = MAIN_COLOR
                )
                embed.set_author(
                        name = f'{ctx.author.name}的個人簡介', 
                        icon_url = str(ctx.author.avatar_url)
                )
                embed.add_field(
                        name = '金錢', 
                        value = f' \n 薪資： **{int(users[3])}** \n\n現金餘額：**{int(users[0])}**    \n銀行餘額：**{int(users[1])}**', 
                        inline = False
                )
                embed.add_field(
                        name = '銀行存款等階：', 
                        value = f'[ {存額等階_data[0]} ] {存額等階_data[1]} \n [等級：**{int(users[6])}** ] \n 銀行存款額度：{int(users[4])}', 
                        inline = True
                )
                embed.add_field(
                        name = '銀行會員等階', 
                        value = f'[ {利息等階_data[0]} ] {利息等階_data[1]} \n [等級：**{int(users[7]) }** ] \n利息：**{round(users[5], 2)}**', 
                        inline = True
                )
                embed.add_field(
                        name = '一般', 
                        value = f"暱稱：`{ctx.author.nick}` \n帳號創建於：`{ctx.author.created_at.__format__('%Y年%m月%d日 %H:%M:%S')}` \n加入時間：`{ctx.author.joined_at.__format__('%Y年%m月%d日 %H:%M:%S')}` ", 
                        inline = False
                )
                
                webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                await webhook.send(
                        embed = embed, 
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
                await embed_[0].delete() #刪除loading訊息
                await embed_[1].delete(); return #刪除先前創建之Webhook
    
        elif regi is not None: #有提及人
            await Core.economy.open_bank(regi)
            regi1 = await Core.economy.get_bank_data(regi)
            利息_data = await Core.economy.利息_data(int(regi1[7]) )
            存額_data = await Core.economy.存額_data(int(regi1[6]))
            
            embed = discord.Embed(
                    title = '一般用戶', 
                    color = MAIN_COLOR
            )
            embed.set_author(
                    name = f'{regi.name}的個人簡介'
            )
            embed.add_field(
                    name = '金錢', 
                    value = f'\n 薪資： **{int(regi1[3])}** \n\n現金餘額：**{int(regi1[0])}**    \n銀行餘額：**{int(regi1[1])}**', 
                    inline = False
            )
            embed.add_field(
                    name = '銀行存款等階：', 
                    value = f'[ {存額_data[0]} ] {存額_data[1]} \n [等級：{int(regi1[6])}] \n 銀行存款額度：{int(regi1[4])}', 
                    inline = True
            )
            embed.add_field(
                    name = '銀行會員等階', 
                    value = f'[ {利息_data[0]} ] {利息_data[1]} \n [等級：**{int(regi1[7]) }** ] \n利息：**{round(regi1[5], 2)}**', 
                    inline = True
            )
            embed.add_field(
                    name = '一般', 
                    value = f"暱稱：`{regi.nick}` \n帳號創建於：`{regi.created_at.__format__('%Y年%m月%d日 %H:%M:%S')}` \n加入時間：`{regi.joined_at.__format__('%Y年%m月%d日 %H:%M:%S')}` ", 
                    inline = False
            )

            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")

            await webhook.send(
                    embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['pay'.casefold()])
    @commands.guild_only()
    async def _pay(self, ctx,member : discord.Member,amount = None):  
        embed_ = await Core.economy.loading(ctx)  #發送Loading訊息
        await Core.economy.open_bank(ctx.author)
        await Core.economy.open_bank(member)

        if amount == None: #未輸入金額
            embed=discord.Embed(title=':warning: 錯誤！', description=f'{ctx.author.mention} 請輸入金額。', color=ORANGE_COLOR)
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            await webhook.send(
                        embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook

        bal = await Core.economy.get_bank_data(ctx.author)
        member_bal = await Core.economy.get_bank_data(member)

        if amount == 'all':
            amount = bal[1]

        amount = int(amount)

        if amount > bal[1]: #判斷餘額是否足夠
            embed=discord.Embed(title=':warning: 錯誤！', description=f'{ctx.author.mention} 你沒有足夠的餘額。', color=ORANGE_COLOR)
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")

            await webhook.send(
                        embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook

        if amount < 0: #判斷使用者是否輸入負數
            embed=discord.Embed(title=':warning: 錯誤！', description=f'{ctx.author.mention} 金額不可為負！', color=ORANGE_COLOR)
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")

            await webhook.send(
                        embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook

        if amount >= int(member_bal[4]): #判斷使用者輸入金額是否大於對方存額
            embed=discord.Embed(title=':warning: 錯誤！', description=f'{ctx.author.mention} 你給予的金額超過了對方的存款額度！', color=ORANGE_COLOR)
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")

            await webhook.send(
                        embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook

        await Core.economy.update_bank(ctx.author,-1*amount,'銀行餘額')
        await Core.economy.update_bank(member,amount,'銀行餘額')
        embed=discord.Embed(title='<a:V_:858154997640331274> 成功執行！', description=f'{ctx.author.mention} 給了 {member} {amount} 元簡明幣。', color=MAIN_COLOR)
        webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")

        await webhook.send(
                        embed = embed, 
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
        await embed_[0].delete() #刪除loading訊息
        await embed_[1].delete() #刪除先前創建之Webhook



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['payday'.casefold()])
    async def _payday(self, ctx):
        webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
        await webhook.send(
                f'{ctx.author.mention} 看來你是個活在過去的老人呢！我們已經有自動予以薪資的福利了。', 
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



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['reward'.casefold()])
    @commands.has_permissions(administrator=True)
    async def 賞(self, ctx ,user : discord.User, *,amount= None):
        await Core.economy.open_bank(user)
        await Core.economy.update_bank(user, int(amount), '現金')
        embed = discord.Embed(
                title = '<a:V_:858154997640331274> 成功執行！', 
                description = f'{ctx.author.mention} 給了 {user} {amount} 元簡明幣。', 
                color = MAIN_COLOR
        )
        webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
        await webhook.send(
                embed = embed, 
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



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['amerce'.casefold()])
    @commands.has_permissions(administrator=True)
    async def 罰(self, ctx, member : discord.User, *,amount= None):
        await Core.economy.open_bank(member)
        await Core.economy.update_bank(member, int(-1*amount), '現金')
        embed=discord.Embed(
                title = '成功執行！', 
                description = f'{ctx.author.mention} 罰了 {member} {amount} 元簡明幣。', 
                color = MAIN_COLOR
        )
        webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
        await webhook.send(
                embed=embed, 
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



    @commands.cooldown(1, 10, commands.BucketType.user)      
    @commands.command(aliases=['up'.casefold()])
    @commands.guild_only()
    async def _up(self, ctx,mode = None, mode_all = None):
        embed_ = await Core.economy.loading(ctx)  #發送Loading訊息

        if mode is None: #當使用者沒有輸入欲升級之模式
            embed = discord.Embed(
                    title = ':warning: 錯誤！', 
                    description = f'{ctx.author.mention}\n請選擇欲升級之對象：`Cup 利息 [all]` 或是 `Cup 存額 [all]` (`[all]` 非必填)', 
                    color = ORANGE_COLOR
            )
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            await webhook.send(
                    embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook

        if mode == '存額' or mode == '存款額度' or mode == '銀行存額': #當模式為存額 or 近似之文字
            if mode_all is not None: #當使用者於mode_all 格 有輸入文字
                if mode_all.lower() == 'all' or mode_all.lower() == 'max': #當上述文字為[ all / max ]
                    users = await Core.economy.get_bank_data(ctx.author)
                    存款額度 = int(users[4])
                    銀行等階 = int(users[6])
                    現金 = int(users[0])
                    扣錢 = math.floor(存款額度*-0.8)
                    if 現金+扣錢 < 0:
                        if int(users[1]) +扣錢 >= 0:
                            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                            embed=discord.Embed(
                                    title = ':warning: 錯誤！', 
                                    description = f'{ctx.author.mention} 你的現金不足{round(-1*扣錢)}，這將使你無法提升任何一銀行等階。\n你可以使用`Cwith {round(-1*扣錢)}`將現金從銀行取出。', 
                                    color = ORANGE_COLOR
                            )
                            await webhook.send(embed = embed, 
                                    username = '˚₊ ࣪« 中央銀行 » ࣪ ˖', 
                                    avatar_url = 'https://imgur.com/csEpNAa.png', 
                                    allowed_mentions = discord.AllowedMentions(
                                            everyone = False, 
                                            users=False, 
                                            roles=False, 
                                            replied_user = False
                                    )
                            )
                            await webhook.delete()
                            await embed_[0].delete() #刪除loading訊息
                            await embed_[1].delete(); return #刪除先前創建之Webhook

                        else:
                            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                            embed=discord.Embed(
                                    title = ':warning: 錯誤！', 
                                    description = f'{ctx.author.mention} 你的現金不足{round(-1*扣錢)}，這將使你無法提升任何一銀行等階。', 
                                    color = ORANGE_COLOR
                            )
                            await webhook.send(
                                    embed = embed, 
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
                            await embed_[0].delete() #刪除loading訊息
                            await embed_[1].delete(); return #刪除先前創建之Webhook
                    
                    while 現金+扣錢 >= 0:  #使用while迴圈計算，當使用者餘額不足時停止
                        銀行等階 += 1
                        扣錢 = math.floor(存款額度 * -0.8)
                        存款額度 += math.floor(存款額度*1.2)
                        現金 += 扣錢  

                    await Core.economy.update_set_bank(
                            ctx.author, 
                            現金
                    )
                    await Core.economy.update_set_bank(
                            ctx.author, 
                            存款額度, 
                            '存款額度'
                    )
                    await Core.economy.update_set_bank(
                            ctx.author, 
                            銀行等階, 
                            '銀行等階'
                    )
                    users = await Core.economy.get_bank_data(ctx.author)
                    存額等階_data = await Core.economy.存額_data(int(users[6]))
                    webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                    embed=discord.Embed(
                            title = '<a:V_:858154997640331274> 成功執行！', 
                            description = f'{ctx.author.mention}\n{存額等階_data[0]}：你的存款上限已上升至**{int(users[4])}**。', 
                            color = MAIN_COLOR
                    )
                    await webhook.send(
                            embed = embed, 
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
                    await embed_[0].delete() #刪除loading訊息
                    await embed_[1].delete(); return #刪除先前創建之Webhook

                else: #當使用者於mode_all輸入之文字非[ all / max]時報錯
                    webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                    embed=discord.Embed(title=':warning: 錯誤！', description=f'{ctx.author.mention} 請輸入`Cup 存額 [all / max]`', color=ORANGE_COLOR)
                    await webhook.send(
                            embed = embed, 
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
                    await embed_[0].delete() #刪除loading訊息
                    await embed_[1].delete() #刪除先前創建之Webhook

            else: #當使用者僅輸入Cup 存額
                users = await Core.economy.get_bank_data(ctx.author)
                存款額度 = int(users[4])
                銀行等階 = int(users[6])
                現金 = int(users[0])
                要扣的錢 = math.floor(存款額度*-0.8)
                new_存款額度 = math.floor(存款額度*1.2 - 存款額度)

                if 現金+要扣的錢 < 0:
                        if int(users[1]) + 要扣的錢 >= 0: #當使用者的銀行餘額足夠升級，然現金不足
                            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                            embed = discord.Embed(
                                    title = ':warning: 錯誤！', 
                                    description = f'{ctx.author.mention} 你的現金不足{-1*要扣的錢}。', 
                                    color = ORANGE_COLOR
                            )
                            await webhook.send(
                                    embed = embed, 
                                    username = '˚₊ ࣪« 中央銀行 » ࣪ ˖', 
                                    avatar_url = 'https://imgur.com/csEpNAa.png', 
                                    allowed_mentions = discord.AllowedMentions(
                                            everyone = False, 
                                            users = False, 
                                            roles = False, 
                                            replied_user = False
                                    ), 
                                    wait = True
                            )
                            message = await ctx.send("提示：你可以點擊下方表情符號 <a:V_:858154997640331274> ——使用銀行餘額進行升級。")
                            await webhook.delete()
                            await embed_[0].delete() #刪除loading訊息
                            await embed_[1].delete() #刪除先前創建之Webhook
                            await message.add_reaction("<a:V_:858154997640331274>")
                            def check(reaction, user):
                                return user == ctx.author and str(reaction.emoji) in ["<a:V_:858154997640331274>"]

                            while True:
                                try:
                                    reaction, user = await self.bot.wait_for(
                                            "reaction_add", 
                                            timeout=15, 
                                            check=check
                                    )

                                    if str(reaction.emoji) == "<a:V_:858154997640331274>": #當使用者點擊表情符號
                                        embed_ = await Core.economy.loading(ctx)  #發送Loading訊息
                                        await message.remove_reaction(
                                            reaction, 
                                            user
                                        )       

                                        存額等階_data = await Core.economy.存額_data(銀行等階)
                                        銀行等階圖示 = 存額等階_data[0]      

                                        await Core.economy.update_bank(
                                                ctx.author, 
                                                要扣的錢, 
                                                '銀行餘額'
                                        )
                                        await Core.economy.update_bank(
                                                ctx.author, 
                                                new_存款額度 , 
                                                '存款額度'
                                        )
                                        await Core.economy.update_bank(
                                                ctx.author, 
                                                1, '銀行等階'
                                        )
                                        await message.edit(f'{ctx.author.mention}\n {銀行等階圖示}：你的存款上限已上升**{new_存款額度}**至**{new_存款額度 + 存款額度}**。')
                                        await embed_[0].delete() #刪除loading訊息
                                        await embed_[1].delete(); return #刪除先前創建之Webhook

                                    else: #timeout --> 刪除表情符號
                                        await message.remove_reaction(reaction, user); return

                                except asyncio.TimeoutError:
                                    await message.edit(f'{ctx.author.mention}\n 指令已超時:(')
                                    break
                            return
                        else:
                            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                            embed=discord.Embed(
                                    title = ':warning: 錯誤！', 
                                    description = f'{ctx.author.mention} 你的現金不足{-1*要扣的錢}。', 
                                    color = ORANGE_COLOR
                            )
                            await webhook.send(
                                    embed = embed, 
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
                            await embed_[0].delete() #刪除loading訊息
                            await embed_[1].delete(); return #刪除先前創建之Webhook

            存額等階_data = await Core.economy.存額_data(銀行等階)
            銀行等階圖示 = 存額等階_data[0]           

            await Core.economy.update_bank(
                    ctx.author, 
                    要扣的錢, 
                    '現金'
            )
            await Core.economy.update_bank(
                    ctx.author, 
                    new_存款額度 , 
                    '存款額度'
            )
            await Core.economy.update_bank(
                    ctx.author, 
                    1, 
                    '銀行等階'
            )
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            embed=discord.Embed(
                    title = '<a:V_:858154997640331274> 成功執行！', 
                    description = f'{ctx.author.mention}\n {銀行等階圖示}：你的存款上限已上升**{new_存款額度}**至**{new_存款額度 + 存款額度}**。', 
                    color = MAIN_COLOR
            )
            await webhook.send(
                    embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook

        if mode == '信用卡' or mode == '利息': #當模式為 信用卡 or 利息
            if mode_all is not None:
                if mode_all.lower() == 'all' or mode_all.lower() == 'max':          
                    await ctx.send('才五等給妳升而已，一級一級慢慢升啦\n~~其實是我不想寫~~'); return

                else: #當mode_all 非 Cup 信用卡 [all /max]
                    embed=discord.Embed(
                            title = ':warning: 錯誤！', 
                            description = f'{ctx.author.mention} 請輸入`Cup 信用卡`', 
                            color = ORANGE_COLOR
                    )
                    webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                    await webhook.send(
                            embed = embed, 
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
                    await embed_[0].delete() #刪除loading訊息
                    await embed_[1].delete() #刪除先前創建之Webhook

            else:
                    users = await Core.economy.get_bank_data(ctx.author)
                    現金 = int(users[0]) 
                    利息等階 = int(users[7]) 
                    NEW_利息 = int(users[5])
                    要扣的錢 = (利息等階 ** 10 *500000)*-1
                    

                    if  現金+要扣的錢 >= 0:
                        if int(users[1]) + 要扣的錢 > 0:
                            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                            embed=discord.Embed(
                                    title = ':warning: 錯誤！', 
                                    description = f'{ctx.author.mention} 你的現金不足{-1*要扣的錢}。你可以使用`Cwith {-1*要扣的錢}`將現金從銀行取出。', 
                                    color = ORANGE_COLOR
                            )
                            await webhook.send(
                                    embed = embed, 
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
                            embed=discord.Embed(title=':warning: 錯誤！', description=f'{ctx.author.mention} 你的現金不足{要扣的錢}，這將使你無法提升任何一銀行等階。', color=ORANGE_COLOR)
                            await webhook.send(
                                    embed = embed, 
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
                        await embed_[0].delete() #刪除loading訊息
                        await embed_[1].delete(); return #刪除先前創建之Webhook    

                    if 利息等階 == 5:
                        webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                        embed=discord.Embed(title=':warning: 錯誤！', description=f'{ctx.author.mention} 目前開放的最高卡種為無限卡。', color=ORANGE_COLOR)
                        await webhook.send(
                                embed = embed, 
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
                        await embed_[0].delete() #刪除loading訊息
                        await embed_[1].delete(); return #刪除先前創建之Webhook
                    
                    await Core.economy.update_bank(ctx.author, 要扣的錢,'現金')
                    await Core.economy.update_bank(ctx.author,0.1,'利息')
                    await Core.economy.update_bank(ctx.author, 1,'利息等階')
                    users = await Core.economy.get_bank_data(ctx.author)
                    利息等階 = int(users[7]) 
                    NEW_利息 = math.ceil(users[5], 3)
                    利息等階_data = await Core.economy.利息_data(利息等階)
                    webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                    embed=discord.Embed(title='<a:V_:858154997640331274> 成功執行！', description=f'{ctx.author.mention} 你已晉升至{利息等階_data[0]}**{利息等階_data[1]}**。你的銀行利息變更為**{math.floor(NEW_利息-1, 2)*100}%**/**每小時**', color=MAIN_COLOR)
                    await webhook.send(
                                embed = embed, 
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
                    await embed_[0].delete() #刪除loading訊息
                    await embed_[1].delete(); return #刪除先前創建之Webhook

        else:
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            embed=discord.Embed(title=':warning: 錯誤！', description=f'{ctx.author.mention} 請輸入`Cup (存額 / 信用卡) [all / max]`', color=ORANGE_COLOR)
            await webhook.send(
                    embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook



    @commands.command(aliases=['with'.casefold(), 'withdraw'.casefold()])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def _withdraw(self, ctx, *,amount= None):
        users = await Core.economy.get_bank_data(ctx.author)
        embed_ = await Core.economy.loading(ctx)  #發送Loading訊息

        if amount.lower() == 'all' or amount.lower() == 'max':
            await Core.economy.update_bank(
                    ctx.author, 
                    +1*int(users[1])
            )
            await Core.economy.update_bank(
                    ctx.author, 
                    -1*int(users[1]), 
                    '銀行餘額'
            )
            embed=discord.Embed(
                    title = '<a:V_:858154997640331274> 成功執行！', 
                    description = f'{ctx.author.mention} 你取出了 {users[1]} 元 從你的銀行中。', 
                    color = MAIN_COLOR
            )
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete() #刪除先前創建之Webhook
            await webhook.send(
                        embed = embed, 
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

        if int(amount) > users[1]: #判斷使用者輸入之金額是否大於其餘額
            embed = discord.Embed(
                    title = ':warning: 錯誤！', 
                    description = f'{ctx.author.mention} 你沒有足夠的餘額。', 
                    color = ORANGE_COLOR
            )
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            await webhook.send(
                        embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook

        if int(amount) < 0: #判斷使用者輸入之金額是否為負數
            embed=discord.Embed(
                    title = ':warning: 錯誤！', 
                    description = f'{ctx.author.mention} 金額不可為負！', 
                    color = ORANGE_COLOR
            )
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete() #刪除先前創建之Webhook
            await webhook.send(
                        embed = embed, 
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

        await Core.economy.update_bank(
                ctx.author, 
                +1 * int(amount)
        )
        await Core.economy.update_bank(
                ctx.author, 
                -1 * int(amount), 
                '銀行餘額'
        )

        embed = discord.Embed(
                title = '<a:V_:858154997640331274> 成功執行！', 
                description = f'{ctx.author.mention} 你取出了 {amount} 元 從你的銀行中。', 
                color = MAIN_COLOR
        )
        webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
        await webhook.send(
                        embed = embed, 
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
        await embed_[0].delete() #刪除loading訊息
        await embed_[1].delete() #刪除先前創建之Webhook
        



    @commands.command(aliases=['dep'.casefold(), 'deposit'.casefold()])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def _deposit(self, ctx, *,amount= None):
        embed_ = await Core.economy.loading(ctx)  #發送Loading訊息

        users = await Core.economy.get_bank_data(ctx.author)

        if amount.lower() == 'all' or amount.lower() == 'max':
            if int(users[0]) > int(users[4]) - int(users[1]):
                webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                embed = discord.Embed(
                        title = ':warning: 錯誤！', 
                        description = f'{ctx.author.mention} 你的銀行存款額度為**{users[4]}**，請提升銀行額度。', 
                        color = ORANGE_COLOR
                )
                await webhook.send(
                        embed = embed, 
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
                await embed_[0].delete() #刪除loading訊息
                await embed_[1].delete(); return #刪除先前創建之Webhook
              
            await Core.economy.update_bank(ctx.author, -1*int(users[0]))
            await Core.economy.update_bank(ctx.author, +1*int(users[0]), '銀行餘額')
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            embed=discord.Embed(
                    title = ':warning: 錯誤！', 
                    description = f'{ctx.author.mention} 你存入了 {users[0]}元 至你的銀行。', 
                    color = ORANGE_COLOR
            )
            await webhook.send(
                        embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete(); return #刪除先前創建之Webhook
            

        else:
            if int(amount)+int(users[1]) > int(users[4]):
                webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                embed=discord.Embed(
                        title = ':warning: 錯誤！', 
                        description = f'{ctx.author.mention} 你的銀行存款額度為**{users[4]}**，請提升銀行額度。', 
                        color = ORANGE_COLOR
                )
                await webhook.send(
                            embed = embed, 
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
                await embed_[0].delete() #刪除loading訊息
                await embed_[1].delete(); return #刪除先前創建之Webhook
            

            if int(amount) > users[0]:
                webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                embed=discord.Embed(
                        title = ':warning: 錯誤！', 
                        description = f'{ctx.author.mention} 你沒有足夠的錢，ㄏㄏ', 
                        color = ORANGE_COLOR
                )
                await webhook.send(
                            embed = embed, 
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
                await embed_[0].delete() #刪除loading訊息
                await embed_[1].delete(); return #刪除先前創建之Webhook

            if int(amount) < 0:
                webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
                embed=discord.Embed(
                        title = ':warning: 錯誤！', 
                        description = f'{ctx.author.mention} 金額不可為負！', 
                        color = ORANGE_COLOR
                )
                await webhook.send(
                            embed = embed, 
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
                await embed_[0].delete() #刪除loading訊息
                await embed_[1].delete(); return #刪除先前創建之Webhook

            await Core.economy.update_bank(
                    ctx.author, 
                    -1 * int(amount)
            )
            await Core.economy.update_bank(
                    ctx.author, 
                    +1 * int(amount), 
                    '銀行餘額'
            )
            users = await Core.economy.get_bank_data(ctx.author)
            webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
            embed=discord.Embed(
                    title = '<a:V_:858154997640331274> 成功執行！', 
                    description = f'{ctx.author.mention} 你存入了 **{math.floor(amount)}** 元 至你的**銀行！**\n你的銀行餘額現在有**{math.floor(users[1])}**元！', 
                    color = MAIN_COLOR
            )
            await webhook.send(
                            embed = embed, 
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
            await embed_[0].delete() #刪除loading訊息
            await embed_[1].delete() #刪除先前創建之Webhook



    @commands.command(aliases=['sy'.casefold(), 'salary'.casefold(), '薪水',])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def _salary(self, ctx):
        embed = discord.Embed(
            title = '🏦中央銀行•', 
            colour = discord.Colour(0x00bfff), 
            description = '此處列出各公職薪資如下'
        )
        embed.add_field(
            name = '總統', 
            value = '44萬8800圓簡明幣', 
            inline = True
        )
        embed.add_field(
            name = '副總統', 
            value = '33萬6700圓簡明幣', 
            inline =True
        )
        embed.add_field(
            name = '黨主席', 
            value = '25萬4000簡明幣', 
            inline = False
        )                
        embed.add_field(
            name = '國務院財政部', 
            value = '19萬6320圓簡明幣', 
            inline = False
        )
        embed.add_field(
            name = '國務院外交部部長', 
            value = '17萬9520圓簡明幣', 
            inline = False
        )
        embed.add_field(
            name = '大法官', 
            value = '19萬5000圓簡明幣', 
            inline = False
        )                        
        embed.add_field(
            name = '立法委員', 
            value = '19萬0500圓簡明幣', 
            inline = False
        )
        embed.set_footer(
            text = f'中央銀行支援兼創辦人•羅少希\n由{ctx.author}請求的鏈接✨'
        )

        webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")

        await webhook.send(
                        embed = embed, 
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



    @commands.command(aliases=['shop'.casefold()])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def _shop(self, ctx):
        embed=discord.Embed(
            title = '簡明市廛', 
            description = '如欲購買物品請使用`Cbuy [物品名稱/物品標號] `\n\n· · - ┈┈━━ ˚ . ✿ . ˚ ━━┈┈ - · ·', 
            color = PINK_COLOR
        )
        embed.add_field(
            name = '1  <:bal:867668445645373480>77,777•四葉幸運草' , 
            value = '>>> •獲得身分組： <@&852083684685119488> \n •為賭博性質的遊戲提升些許成功機率。', 
            inline = False
        )
        embed.add_field(
            name = '2  <:bal:867668445645373480>1e20•新臺幣', 
            value = '>>> •獲得身分組：無 \n •簡明幣🔀新台幣20$', 
            inline = False
        )
        embed.add_field(
            name = "3  <:bal:867668445645373480>200,000•手錶⌚", 
            value = ">>> •獲得身分組：<@&852049088395476992>\n •可見<#852364573095755808>與<#852346393141182484>頻道。", 
            inline = False
        )
        embed.add_field(
            name = "4  <:bal:867668445645373480>2,000,000•替換名稱顏色鑰匙<:key:852056890707279892>", 
            value = ">>> •獲得身分組：<@&852084041192964096>\n•開啟<#846673897079308288>頻道。可於此處替換名稱顏色。", 
            inline = False
        )
        embed.add_field(
            name = "5  <:bal:867668445645373480>99,879•Discord背景模板更換教學", 
            value = ">>> •獲得身分組：<@&854580418632351804> \n•開啟<#854578071990829056>頻道。可於此處查看更換Discord背景之教學。", 
            inline=False
        )
        embed.set_footer(
            text = f'由{ctx.author}請求的鏈接✨'
        )
        webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
        await webhook.send(
            embed = embed, 
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



    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def 為了紀年2018年的我而特別留下來的指令(self, ctx):
        request_data = {
        "content": 'idk <:idiot:469889163215372298>',
        "username": 'test',
        "avatar_url": 'https://i.imgur.com/Q7pSrjt.png',
        }
        requests.post(
          url = 'https://discord.com/api/webhooks/859633422498398288/5JVnexiCnP3BIk-kLPuAk4xDqadplNzgv-85zyS25poVDjhFjPwXz1CX0SDkbUlkcSwb', 
          data = request_data
        )

def setup(bot):
   bot.add_cog(Economy(bot))