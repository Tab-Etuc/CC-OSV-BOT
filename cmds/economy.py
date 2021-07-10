import discord
from discord.ext import commands
import os, random
from pymongo import MongoClient
from core.classes import Cog_Extension
import core.economy
from discord_webhook.webhook import DiscordWebhook, DiscordEmbed
import time, datetime
from config import *

auth_url = os.getenv("MONGODB_URI")

class Mongo(Cog_Extension):  

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def count(self, ctx):
      cluster = MongoClient(auth_url)
      db = cluster["Economy"]

      cursor = db["Bank"]
      filter = {"真人":"True"}
      user = cursor.count_documents(filter)
      webhook = DiscordWebhook(url=WEBHOOK_URL, content=f'已經有{user}位國民已開戶。')
      webhook.execute()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def top(self, ctx):
      data = []
      index = 1
      cluster = MongoClient(auth_url)
      db = cluster["Economy"]
      cursor = db["Bank"]
      mydoc = cursor.find().sort("銀行餘額",-1)
      
      for member in mydoc:
        if index > 8:
            break
        

        member_name = self.bot.get_user(member["_id"])
        member_wa_amt = member["現金"]
        member_ba_amt = member['銀行餘額']
        member_amt = 0
        member_amt += int(member_wa_amt + member_ba_amt)

        if index == 1:
            msg1 = f"**🥇 `{member_name}` -- {member_amt}**"
            data.append(msg1)

        if index == 2:
            msg2 = f"**🥈 `{member_name}` -- {member_amt}**"
            data.append(msg2)

        if index == 3:
            msg3 = f"**🥉 `{member_name}` -- {member_amt}**\n"
            data.append(msg3)

        if index >= 4:
            members = f"**{index} `{member_name}` -- {member_amt}**"
            data.append(members)
        index += 1

      msg = "\n".join(data)

      em = discord.Embed(
          title=f"頂尖 {index-1}位 最富有的國民 - 排行榜 ",
          description=f"它基於全國國民的淨資產（現金+銀行餘額）||其實還沒寫好|| \n\n{msg}",
          color=discord.Color(0x00ff00),
          timestamp=datetime.datetime.utcnow()
      )
      em.set_footer(text=f"全國 - {ctx.guild.name}")
      await ctx.send(embed=em)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def bag(self, ctx):
      await core.economy.open_account(ctx.author)
      user = ctx.author
      users = await core.economy.get_bag_data()

      try:
          bag = users[str(user.id)]["bag"]
      except:
          bag = []
      em = discord.Embed(title = f"{ctx.author}的背包")
      for item in bag:
          name = item["item"]
          amount = item["amount"]

          em.add_field(name = name, value = amount)    

      await ctx.send(embed = em)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def buy(self, ctx, item, amount = 1):
        await core.economy.open_account(ctx.author)

        res = await core.economy.buy_this(ctx.message.author,item,amount,ctx.author)
        if not res[0]:
          if res[1]==1:
              await ctx.send("並沒有這項物品。")
              return
          if res[1]==2:
              await ctx.send(f"你沒有足夠的錢購買{amount}個`{item}`。")
              return
          if res[1]==3:
              await ctx.send(f"你已經購買過`{item}`了。")
              return

        member = ctx.message.author
        await ctx.send(f"你已買了{amount}個`{item}`。")
        if "luckyclover" in str(item): 
          guild=self.bot.get_guild(833942312018771989)
          role =guild.get_role(852083684685119488)
          await member.add_roles(role)
        elif "watch" in str(item): 
          guild=self.bot.get_guild(833942312018771989)
          role =guild.get_role(852049088395476992)
          await member.add_roles(role)    
          await ctx.send("你已解鎖 <#852364573095755808> 頻道(最上方)。")      
        elif "name" in str(item): 
          guild=self.bot.get_guild(833942312018771989)
          role =guild.get_role(852084041192964096)
          await member.add_roles(role)            
        elif "BG" in str(item): 
          guild=self.bot.get_guild(833942312018771989)
          role =guild.get_role(854580418632351804)
          await member.add_roles(role)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['rb2'])
    async def rob(self, ctx,member : discord.Member): 
      if member == ctx.author:
        webhook = DiscordWebhook(url=WEBHOOK_URL, content='自己搶自己並不會憑空冒出多的錢。')
        webhook.execute(); return
      embed_ = await core.economy.loading()
      user = ctx.author
      webhook = DiscordWebhook(url=WEBHOOK_URL)  
      await core.economy.open_bank(user)
      await core.economy.open_bank(member)
      bal = await core.economy.get_bank_data(member)
      data = await core.economy.get_bank_data(user)
      timer = data[8]
      now_time = int(time.time())
      timeleft = int(now_time-timer)
      timeleft = 86400 - timeleft
      if timeleft > 0:
            typeT = '秒'
            if timeleft > 60 and timeleft < 3600:
                timeleft = timeleft // 60
                typeT = '分鐘'
            elif timeleft >=3600:
              timeleft = timeleft // 3600
              typeT= '小時'
            webhook = DiscordWebhook(url=WEBHOOK_URL, content='你仍需等待{}{}!'.format(timeleft, typeT))
            webhook.execute()
            webhook.delete(embed_)
            return

      if bal[0]<100:    

          embed3=DiscordEmbed(title="搶他也沒用:(", description="他剩沒有多少現金了。", color=ORANGE_COLOR)
          
          webhook.add_embed(embed3)
          webhook.delete(embed_)
          webhook.execute(embed3)
          return

      earning = random.randrange(0,bal[0])

      await core.economy.update_bank(ctx.author,earning)
      await core.economy.update_bank(member,-1*earning)
      await core.economy.update_set_bank(ctx.author,now_time,"Rob")
      webhook = DiscordWebhook(url=WEBHOOK_URL, content=f'{ctx.author}已搶了{member} **{earning}** 元！')
      webhook.delete(embed_)
      webhook.execute()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def 國庫(self, ctx):
      webhook = DiscordWebhook(url=WEBHOOK_URL)  
      embed_ = await core.economy.loading()

      users = await core.economy.get_國庫()
      bank_amt = int(users[1])
      當周 = int(users[0]) 
      webhook.delete(embed_)
      embed = DiscordEmbed(title="國庫")
      embed.add_embed_field(name="餘額：", value="**{}**".format(bank_amt))
      embed.add_embed_field(name="當周所得：", value="**{}**".format(當周))
      webhook.add_embed(embed)
      webhook.delete(embed_)
      webhook.execute(embed)
     

    @commands.cooldown(1, 10, commands.BucketType.user)     
    @commands.command(aliases=['p','bank','BANK','Bank','P'])
    @commands.guild_only()
    async def profile(self, ctx, regi: discord.Member = None):
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        embed_ = await core.economy.loading()
        user = ctx.author 
        user1 = user
        await core.economy.open_bank(user)
                                        
        users = await core.economy.get_bank_data(user)
        if (regi is not None and regi.bot) or ctx.author.bot:
            webhook.delete(embed_)
            webhook = DiscordWebhook(url=WEBHOOK_URL, content='該用戶是一個BOT，不能擁有一個帳戶')
            webhook.execute(); return
        elif not regi:

                avatar_url = str(user1.avatar_url)
                users = await core.economy.get_bank_data(user)
                wallet_amt = int(users[0])
                bank_amt = int(users[1])
                bank_lv = int(users[4])
                薪資 = int(users[3])
                利息 = users[5]
                new_銀行等階 = int(users[6])   
                利息等階 = int(users[7]) 
                利息等階_data = await core.economy.利息_data(利息等階)
                利息等階圖示 = 利息等階_data[0]
                利息等階名稱 = 利息等階_data[1]

                存額等階_data = await core.economy.存額_data(new_銀行等階)
                new_銀行等階圖示 = 存額等階_data[0]
                銀行等階名稱 = 存額等階_data[1]

                embed = DiscordEmbed(title="一般用戶".format(user.name), color=MAIN_COLOR)
                embed.set_author(name="{}的個人簡介".format(user.name), icon_url=avatar_url)

                embed.add_embed_field(name="金錢", value=" \n 薪資： **{}** \n\n現金餘額：**{}**    \n銀行餘額：**{}**".format(薪資,wallet_amt, bank_amt), inline=False)
                embed.add_embed_field(name="銀行存款等階：", value="[ {} ] {} \n [等級：**{}** ] \n 銀行存款額度：{}".format(new_銀行等階圖示,銀行等階名稱,new_銀行等階,bank_lv), inline=True)
                embed.add_embed_field(name="銀行會員等階", value=f"[ {利息等階圖示} ] {利息等階名稱} \n [等級：**{利息等階}** ] \n利息：**{round(利息, 2)}**", inline=True)
                embed.add_embed_field(name="一般", value=f"暱稱：`{user.nick}` \n帳號創建於：`{user.created_at.__format__('%Y年%m月%d日 %H:%M:%S')}` \n加入時間：`{user.joined_at.__format__('%Y年%m月%d日 %H:%M:%S')}` ", inline=False)
                webhook.add_embed(embed)
                webhook.delete(embed_)
                webhook.execute(); return
    
        elif regi is not None:
            regi1 = await core.economy.get_bank_data(regi)
            wallet_amt = int(regi1[0])
            bank_amt = int(regi1[1])
            bank_lv = int(regi1[4])
            薪資 = int(regi1[3])
            利息 = regi1[5]
            new_銀行等階 = int(regi1[6])  
            利息等階 = int(regi1[7]) 
            利息_data = await core.economy.利息_data(利息等階)
            利息等階圖示 = 利息_data[0]
            利息等階名稱 = 利息_data[1]
            存額_data = await core.economy.存額_data(new_銀行等階)
            new_銀行等階圖示 = 存額_data[0]
            銀行等階名稱 = 存額_data[1]
            
            embed = DiscordEmbed(title="一般用戶".format(regi.name), color=MAIN_COLOR)
            embed.set_author(name="{}的個人簡介".format(regi.name))
            embed.add_embed_field(name="金錢", value="\n 薪資： **{}** \n\n現金餘額：**{}**    \n銀行餘額：**{}**".format(薪資,wallet_amt, bank_amt), inline=False)
            embed.add_embed_field(name="銀行存款等階：", value="[ {} ] {} \n [等級：{}] \n 銀行存款額度：{}".format(new_銀行等階圖示,銀行等階名稱,new_銀行等階,bank_lv), inline=True)
            embed.add_embed_field(name="銀行會員等階", value=f"[ {利息等階圖示} ] {利息等階名稱} \n [等級：**{利息等階}** ] \n利息：**{round(利息, 2)}**", inline=True)
            embed.add_embed_field(name="一般", value=f"暱稱：`{regi.nick}` \n帳號創建於：`{regi.created_at.__format__('%Y年%m月%d日 %H:%M:%S')}` \n加入時間：`{regi.joined_at.__format__('%Y年%m月%d日 %H:%M:%S')}` ", inline=False)

            webhook.add_embed(embed)
            webhook.delete(embed_)
            webhook.execute(); return

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['pay'])
    @commands.guild_only()
    async def send(self, ctx,member : discord.Member,amount = None):  
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        embed_ = await core.economy.loading()
        await core.economy.open_bank(ctx.author)
        await core.economy.open_bank(member)
        if amount == None:
            embed=DiscordEmbed(title=":warning: 錯誤！", description="請輸入金額。", color=ORANGE_COLOR)
            webhook.add_embed(embed)
            webhook.execute()    
            webhook.delete(embed_)   
            return

        bal = await core.economy.get_bank_data(ctx.author)
        member_bal = await core.economy.get_bank_data(member)
        if amount == 'all':
            amount = bal[1]

        amount = int(amount)

        if amount > bal[1]:
            embed=DiscordEmbed(title=":warning: 錯誤！", description="你沒有足夠的餘額。", color=ORANGE_COLOR)
            webhook.add_embed(embed)
            webhook.execute()    
            webhook.delete(embed_)   
            return
        if amount < 0:
            embed=DiscordEmbed(title=":warning: 錯誤！", description="金額不可為負！", color=ORANGE_COLOR)
            webhook.add_embed(embed)
            webhook.execute()  
            webhook.delete(embed_)
            return
        if amount >= int(member_bal[4]):
            embed=DiscordEmbed(title=":warning: 錯誤！", description="你給予的金額超過了對方的存款額度！", color=ORANGE_COLOR)
            webhook.add_embed(embed)
            webhook.delete(embed_)
            webhook.execute()  
            return

        await core.economy.update_bank(ctx.author,-1*amount,"銀行餘額")
        await core.economy.update_bank(member,amount,"銀行餘額")
        embed=DiscordEmbed(title="成功執行！", description=f"{ctx.author.mention} 給了 {member} {amount} 元簡明幣。", color=MAIN_COLOR)
        webhook.add_embed(embed)
        webhook.delete(embed_)
        webhook.execute()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def payday(self, ctx):
        await ctx.send("看來你是個活在過去的老人呢！我們已經有自動予以薪資的福利了。")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=["reward"])
    @commands.has_permissions(administrator=True)
    async def 賞(self, ctx ,user : discord.User, *,amount= None):
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        amount = int(amount)
        await core.economy.open_bank(user)
        await core.economy.update_bank(user,amount,"現金")
        embed=DiscordEmbed(title="成功執行！", description=f"{ctx.author.mention} 給了 {user} {amount} 元簡明幣。", color=MAIN_COLOR)
        webhook.add_embed(embed)
        webhook.execute()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=["amerce"])
    @commands.has_permissions(administrator=True)
    async def 罰(self, ctx, member : discord.User, *,amount= None):
        webhook = DiscordWebhook(url=WEBHOOK_URL)        
        amount = int(amount)
        await core.economy.open_bank(member)
        await core.economy.update_bank(member,-1*amount,"現金")
        embed=DiscordEmbed(title="成功執行！", description=f"{ctx.author.mention} 罰了 {member} {amount} 元簡明幣。", color=MAIN_COLOR)
        webhook.add_embed(embed)
        webhook.execute()

    @commands.cooldown(1, 10, commands.BucketType.user)      
    @commands.command(aliases=["UP"])
    @commands.guild_only()
    async def up(self, ctx,mode = None, amount = None):
      embed_ = await core.economy.loading()
      webhook = DiscordWebhook(url=WEBHOOK_URL)
      user = ctx.author
      if mode is None:
        await ctx.send("請選擇欲升級之對象：`Cup 利息 [all]` 或是 `Cup 存額 [all]` (`[all]` 非必填)")
        webhook.delete(embed_)   
        return
      if mode == "存額":
          if amount is not None:
            if amount.lower() == "all" or amount.lower() == "max":
              users = await core.economy.get_bank_data(user)
              存款額度 = int(users[4])
              銀行等階 = int(users[6])
              現金 = int(users[0])
              扣錢 = 存款額度*-0.8
              if 現金+扣錢 < 0:
                  await ctx.send(f"你的現金不足{round(-1*扣錢)}，這將使你無法提升任何一銀行等階。\n你可以使用`Cwith {round(-1*扣錢)}`將現金從銀行取出。")  
                  webhook.delete(embed_)   
                  return  
              真_要扣的錢 = 0
              現金 += 扣錢  
              
              while 現金+扣錢 >= 0:
                  銀行等階 += 1
                  扣錢 = 存款額度 * -0.8   
                  存款額度 += 存款額度*1.2  
                  現金 += 扣錢  
                  真_要扣的錢 += 扣錢 

              存款額度 -= int(users[4])
              await core.economy.update_bank(user, 真_要扣的錢,"現金")
              await core.economy.update_bank(user, 存款額度 ,"存款額度")
              await core.economy.update_bank(user, 銀行等階,"銀行等階")
              NEW_users = await core.economy.get_bank_data(user)
              NEW_存款額度 = int(NEW_users[4])
              new_銀行等階 = int(NEW_users[6])   
              存額等階_data = await core.economy.存額_data(new_銀行等階)
              new_銀行等階圖示 = 存額等階_data[0]

              await ctx.send(f"{new_銀行等階圖示}：你的存款上限已上升至**{NEW_存款額度}**。")
              webhook.delete(embed_)  
              return 
            else:
              await ctx.send("請輸入`Cup 存額 [all / max]`")
              webhook.delete(embed_)   
          else:
              users = await core.economy.get_bank_data(user)
              存款額度 = int(users[4])
              銀行等階 = int(users[6])
              現金 = int(users[0])
              要扣的錢 = 存款額度*-0.8
              new_存款額度 = 存款額度*1.2 - 存款額度
              if 現金+要扣的錢 < 0:
                  await ctx.send(f"你的現金不足{round(-1*要扣的錢)}，你可以使用`Cwith {round(-1*要扣的錢)}`將現金從銀行取出。")    
                  webhook.delete(embed_)   
                  return    
              存額等階_data = await core.economy.存額_data(銀行等階)
              new_銀行等階圖示 = 存額等階_data[0]           
                          

              await core.economy.update_bank(user, 要扣的錢,"現金")
              await core.economy.update_bank(user, new_存款額度 ,"存款額度")
              await core.economy.update_bank(user, 1,"銀行等階")

              await ctx.send(f"{new_銀行等階圖示}：你的存款上限已上升**{new_存款額度}**至**{new_存款額度 + 存款額度}**。")
              webhook.delete(embed_)   
              return
      if mode.lower() == "信用卡":
        if amount is not None:
          if amount.lower() == "all" or amount.lower() == "max":          
            await ctx.send("才五等給妳升而已，一級一級慢慢升啦~~其實是我不想寫~~")
            return
          else:
              await ctx.send("請輸入`Cup 信用卡 [all / max]`")
              webhook.delete(embed_)   
        else:
          users = await core.economy.get_bank_data(user)
          現金 = int(users[0]) 
          利息等階 = int(users[7]) 
          利息= round(0.1, 1)
          NEW_利息 = int(users[5])
          要扣的錢 = (利息等階 ** 2 *500000)*-1
          data = 0
          if -1*要扣的錢 == 現金+要扣的錢:
                data += 1
          if -1*要扣的錢 < 現金:
                data += 1
          elif -1*要扣的錢 > 現金+要扣的錢:
              if data != 1:
                await ctx.send(f"你的現金不足{round(-1*要扣的錢)}，你可以使用`Cwith {round(-1*要扣的錢)}`將現金從銀行取出。")    
                webhook.delete(embed_)   
                return    
          if 利息等階 == 5:
            await ctx.send(f"目前開放的最高卡種為無限卡。")    
            webhook.delete(embed_)   
            return

          await core.economy.update_bank(user, 要扣的錢,"現金")
          await core.economy.update_bank(user,利息,"利息")
          await core.economy.update_bank(user, 1,"利息等階")
          users = await core.economy.get_bank_data(user)
          利息等階 = int(users[7]) 
          NEW_利息 = round(users[5], 3)
          利息等階_data = await core.economy.利息_data(利息等階)
          利息等階圖示 = 利息等階_data[0]
          利息等階名稱 = 利息等階_data[1]

          await ctx.send(f"你已晉升至{利息等階圖示}**{利息等階名稱}**。你的銀行利息變更為**{round(NEW_利息-1, 3)*100}%**/**每小時**")
          webhook.delete(embed_)   
          return
      else:
        await ctx.send("請輸入`Cup (存額 / 信用卡) [all / max]`")
        webhook.delete(embed_)   
             
    @commands.command(aliases=["with"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def withdraw(self, ctx, *,amount= None):
        user = ctx.author


        users = await core.economy.get_bank_data(user)

        bank_amt = users[1]

        if amount.lower() == "all" or amount.lower() == "max":
            await core.economy.update_bank(user, +1*bank_amt)
            await core.economy.update_bank(user, -1*bank_amt, "銀行餘額")
            embed=discord.Embed(title="成功執行！", description=f"{user.mention} 你取出了 {users[1]} 元 從你的銀行中。", color=MAIN_COLOR)
            await ctx.send(embed=embed)    
            return

        amount = int(amount)

        if amount > bank_amt:
            await ctx.message.delete()
            embed=discord.Embed(title=":warning: 錯誤！", description="你沒有足夠的餘額。", color=ORANGE_COLOR)
            await ctx.send(embed=embed)    
            return

        if amount < 0:
            await ctx.message.delete()
            embed=discord.Embed(title=":warning: 錯誤！", description="金額不可為負！", color=ORANGE_COLOR)
            await ctx.send(embed=embed)    
            return

        await core.economy.update_bank(user, +1 * amount)
        await core.economy.update_bank(user, -1 * amount, "銀行餘額")

        embed=discord.Embed(title="成功執行！", description=f"{user.mention} 你取出了 {amount} 元 從你的銀行中。", color=MAIN_COLOR)
        await ctx.send(embed=embed)    


    @commands.command(aliases=["dep"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def deposit(self, ctx, *,amount= None):
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        embed_ = await core.economy.loading()
        user = ctx.author


        users = await core.economy.get_bank_data(user)


        wallet_amt = users[0]

        if amount.lower() == "all" or amount.lower() == "max":
            if int(users[0]) > int(users[4]) - int(users[1]):
              webhook = DiscordWebhook(url=WEBHOOK_URL, content=f'你的銀行存款額度為**{users[4]}**，請提升銀行額度。')
              webhook.delete(embed_)
              webhook.execute(); return
            await core.economy.update_bank(user, -1*wallet_amt)
            await core.economy.update_bank(user, +1*wallet_amt, "銀行餘額")
            webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"{user.mention} 你存入了 {wallet_amt}元 至你的銀行。")
            webhook.delete(embed_)
            webhook.execute(); return
        else:
          if int(amount)+int(users[1]) > int(users[4]):
            webhook.delete(embed_)
            webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"你的銀行存款額度為**{users[4]}**，請提升銀行額度。")
            webhook.execute(); return

          amount = int(amount)

          if amount > wallet_amt:
            webhook.delete(embed_)
            webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"{user.mention} 你沒有足夠的錢，ㄏㄏ")
            webhook.execute(); return

          if amount < 0:
            webhook.delete(embed_)
            webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"{user.mention} 金額不可為負！")
            webhook.execute(); return

          await core.economy.update_bank(user, -1 * amount)
          await core.economy.update_bank(user, +1 * amount, "銀行餘額")
          users = await core.economy.get_bank_data(user)
          餘額 = users[1]
          webhook.delete(embed_)
          webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"{user.mention} 你存入了 **{amount}** 元 至你的**銀行！**\n你的銀行餘額現在有**{round(餘額)}**元！")
          webhook.execute()

    @commands.command(aliases=['SY','薪水','Salary','SALARY'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def salary(self, ctx):
        webhook = DiscordWebhook(url=WEBHOOK_URL)

        embed = DiscordEmbed(title='🏦簡明銀行公告•', color='0x00bfff', description='此處列出各公職薪資如下')
        embed.add_embed_field(name="總統", value="壹拾萬圓簡明幣", inline=True)
        embed.add_embed_field(name="副總統", value="柒萬伍仟圓簡明幣", inline=True)
        embed.add_embed_field(name="國務總理", value="柒萬伍仟圓簡明幣", inline=False)
        embed.add_embed_field(name="國務院外交部部長", value="貳萬圓簡明幣", inline=False)
        embed.add_embed_field(name="立法院院長", value="貳萬伍仟圓整", inline=False)
        embed.add_embed_field(name="省長", value="貳萬圓簡明幣", inline=False)
        embed.add_embed_field(name="市長", value="貳萬圓簡明幣", inline=False)
        embed.set_footer(text="簡明銀行支援兼創辦人•羅少希")
        webhook.add_embed(embed)
        webhook.execute()

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def shop(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0xfdf74e),description="**如欲購買物品請使用`Cbuy 物品 [數量]`**\n\n**CC-OSV SHOP - Page 1/2**\n<:__:852032874940858380> `luckyclover` - 為賭博性質的遊戲提升些許成功機率。 | **77,777** <:coin:852035374636728320>\n<:NTD:852048045695827988> `NTD` - 簡明幣🔀新台幣20$ | **1e20** <:coin:852035374636728320>\n⌚ `watch` - 可見顯示現在時間之頻道。 | **200,000** <:coin:852035374636728320>\n<:key:852056890707279892> `namecolor` - 獲取進入<#846673897079308288>的頻道鑰匙。 | **2,000,000** <:coin:852035374636728320>\n<:key:852056890707279892> `BGTutorials` - 購買Discord背景更換教學。 | **99,879** <:coin:852035374636728320> ")
        await ctx.send(embed = embed)

def setup(bot):
   bot.add_cog(Mongo(bot))
