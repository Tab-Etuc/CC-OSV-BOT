import discord
from discord.ext import commands
from core.classes import Cog_Extension
import core.account
from discord_webhook.webhook import DiscordWebhook, DiscordEmbed
from discord_components import DiscordComponents, Button, ButtonStyle
from discord import Embed
import pandas as pd
import json
from config import *


async def open_account(user):

      users = await get_bank_data()

      if str(user.id) in users:
          return False
      else:
          users[str(user.id)] = {}


      with open('mainbank.json','w') as f:
          json.dump(users,f)

      return True

async def get_bank_data():
      with open('mainbank.json','r') as f:
          users = json.load(f)
      
      return users

async def buy_this(user,item_name,amount,new):
  item_name = item_name.lower()
  name_ = None
  for item in mainshop:
      name = item["name"].lower()
      if name == item_name:
          name_ = name
          price = item["price"]
          break
            
  if name_ == None:
      return [False,1]

  bal = core.account.bal(user)
  cost = price*amount
  users = await get_bank_data()

  if bal < cost:
      return [False,2]
            
  try:
    index = 0
    t = None
    for thing in users[str(new.id)]["bag"]:
        n = thing["item"]
        if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(new.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
        index+=1 
    if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(new.id)]["bag"].append(obj)
  except:
        obj = {"item":item_name , "amount" : amount}
        users[str(new.id)]["bag"] = [obj]        
            
  with open("mainbank.json","w") as f:
      json.dump(users,f)

  df = pd.read_csv('accounts.csv')
  df.loc[df["UserId"] == int(user), "Balance"] -= cost
  df.to_csv('accounts.csv', index=False)

  
  return [True,"Worked"]

mainshop = [{"name":"Card","price":3000,"description":"c"},
            {"name":"LuckyClover","price":77777,"description":"Work"},
            {"name":"NTD","price":100000000000000000000,"description":"Gaming"},
            {"name":"watch","price":200000,"description":"Sports Car"},
            {"name":"NameColor","price":2000000,"description":"Sports Car"},
            {"name":"BGTutorials","price":99879}
            
            
            ]


class Economy(Cog_Extension):
  @commands.command()
  async def shop(self, ctx):
    embed = discord.Embed(colour=discord.Colour(0xfdf74e), description="**如欲購買物品請使用`Cbuy 物品 [數量]`**\n\n**CC-OSV SHOP - Page 1/2**\n<:__:852028673363279893> `card` - 普卡，可以減免3%的稅。日後可升級 。 | **3,000** <:coin:852035374636728320>\n<:__:852032874940858380> `luckyclover` - 為賭博性質的遊戲提升些許成功機率。 | **77,777** <:coin:852035374636728320>\n<:NTD:852048045695827988> `NTD` - 簡明幣🔀新台幣20$ | **1e20** <:coin:852035374636728320>\n⌚ `watch` - 可見顯示現在時間之頻道。 | **200,000** <:coin:852035374636728320>\n<:key:852056890707279892> `namecolor` - 獲取進入<#846673897079308288>的頻道鑰匙。 | **2,000,000** <:coin:852035374636728320>\n<:key:852056890707279892> `BGTutorials` - 購買Discord背景更換教學。  | **99,879** <:coin:852035374636728320> ")

    await ctx.send(embed = embed)

  @commands.command()
  async def bag(self, ctx):
      await open_account(ctx.author)
      user = ctx.author
      users = await get_bank_data()

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

  @commands.command()
  async def buy(self, ctx, item, amount = 1):
        await open_account(ctx.author)

        res = await buy_this(ctx.message.author.id,item,amount,ctx.author)
        if not res[0]:
          if res[1]==1:
              await ctx.send("並沒有這項物品。")
              return
          if res[1]==2:
              await ctx.send(f"你沒有足夠的錢購買{amount}個`{item}`。")
              return

        member = ctx.message.author
        await ctx.send(f"你已買了{amount}個`{item}`。")
        if "card" in str(item): 
          guild=self.bot.get_guild(833942312018771989)
          role =guild.get_role(852083795015499776)
          await member.add_roles(role)
        elif "luckyclover" in str(item): 
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


  @commands.command()
  async def menu(self, ctx):
    await ctx.message.delete()
    embed = Embed(
            color=0xF5F5F5,
            title="簡明銀行介面",
            description="點擊下方按鈕進行操作",
        )

    menu_components = [
            [
                Button(style=ButtonStyle.red, label="開戶",  disabled=True),
                Button(style=ButtonStyle.green, label="領薪水(兩小時一次)"),
                Button(style=ButtonStyle.green, label="列出本國前五的富豪")
            ],
            [
                Button(style=ButtonStyle.green, label="列出本國薪資表"),
                Button(style=ButtonStyle.green, label="列出已於本銀行開戶數"),
                Button(style=ButtonStyle.green, label="顯示你的餘額"),
            ]
        ]
    end_components = [
          [
                    Button(style=ButtonStyle.green, label="再次操作？"),
          ]
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
            res = await self.bot.wait_for("button_click", check=check, timeout=20)
    except TimeoutError:
            await msg.edit(
                embed=Embed(color=0xED564E, title="時間到!", description="沒有人回應。 ☹️"),
                components=[
                    Button(style=ButtonStyle.red, label="已超時!", disabled=True)
                ],
            );return

    await res.respond(
            type=7,
            embed=Embed(
                color=0xF5F5F5,
                title="已成功執行動作。"
            ),components=end_components,
        )

    if res.component.label == "列出本國前五的富豪":
          await self.top(ctx)
    elif res.component.label == "領薪水(兩小時一次)":
          await core.account.payday(ctx.message.author.id)
    elif res.component.label == "列出已於本銀行開戶數":
          await self.count(ctx)
    elif res.component.label == "列出本國薪資表":
          await self.salary(ctx)
    elif res.component.label == "顯示你的餘額":
          await self.MenuBal(ctx)

    await msg.edit(
            embed=embed,
            components=end_components,
        )

    try:
            res = await self.bot.wait_for("button_click", check=check, timeout=20)
    except TimeoutError:
            await msg.delete()
            del self.session_message[ctx.author.id]
            return

    await res.respond(type=6)
    if res.component.label == "再次操作？":
            self.session_message[ctx.author.id] = msg
            await self.menu(ctx)

 
  @commands.command(name='top')
  async def top(self, ctx):
    leadboard = core.account.top()
    name1 = await self.bot.fetch_user(leadboard[0][0])
    name2 = await self.bot.fetch_user(leadboard[1][0])
    name3 = await self.bot.fetch_user(leadboard[2][0])
    name4 = await self.bot.fetch_user(leadboard[3][0])
    name5 = await self.bot.fetch_user(leadboard[4][0])

    fmt = '1.`{0.display_name}`: {1}2.`{2.display_name}`: {3}3.`{4.display_name}`: {5}4.`{6.display_name}`: {7}5.`{8.display_name}`: {9}'
    board = fmt.format(name1, leadboard[0][1] + '\n', name2, leadboard[1][1] + '\n', name3, leadboard[2][1] + '\n', name4, leadboard[3][1] + '\n', name5, leadboard[4][1])
    
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D')

    embed = DiscordEmbed(title="排行榜", color='0x724ded', description=board)
    webhook.add_embed(embed)
    webhook.execute()
  

  @commands.command(name='register', aliases=['reg','開戶'])
  async def register(self, ctx):       
        await ctx.send(core.account.register(ctx.message.author.id)); 
        return

  @commands.command()
  async def MenuBal(self, ctx):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D')

    embed = DiscordEmbed(title="銀行帳戶信息:", color='0xf5a623', description="你的餘額是： `{}`".format(core.account.bal(ctx.message.author.id)))
    webhook.add_embed(embed)
    webhook.execute()

  @commands.command()
  async def bank(self, ctx, regi: discord.User = None):
        if (regi is not None and regi.bot) or ctx.author.bot:
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='該用戶是BOT，不能擁有一個帳戶')
            webhook.execute(); return
        elif not regi:
            if core.account.bal(ctx.message.author.id) is None:
                webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請參照此格式 `Creg`進行開戶')
                webhook.execute(); return
            else:
                webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D')

                embed = DiscordEmbed(title="銀行帳戶信息:", color='0xf5a623', description="你的餘額是： `{}`".format(core.account.bal(ctx.message.author.id)))
                webhook.add_embed(embed)
                webhook.execute(); return
    
        elif regi is not None:
            print(regi.id)
            if core.account.bal(regi.id) is None:
                webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='該用戶不存在或尚未註冊銀行帳戶。')
                webhook.execute(); return
            else:
                webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D')

                embed = DiscordEmbed(title='銀行賬戶信息：', color='0xf5a800', description='{}的餘額是： `{}`'.format(regi.display_name, core.account.bal(regi.id)))
                webhook.add_embed(embed)
                webhook.execute(); return
                
  @commands.command(name='salary', aliases=['SY','薪水'])
  async def salary(self, ctx):
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D')

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
  async def pay(self, ctx, regi: discord.User = None, amount=None):
        if (regi is not None and regi.bot) or ctx.author.bot:
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='該用戶是BOT，不能擁有一個帳戶')
            webhook.execute(); return
        if amount is None:
          webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請使用此格式指定付款金額： `Cpay @國民名稱 金額`')
          webhook.execute(); return
        try:
            amount = int(amount)
        except ValueError:
          webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請輸入整數。 ~~TMD這判斷函式我寫了N小時~~ ')
          webhook.execute(); return
        await ctx.send(core.account.pay(ctx.message.author.id, regi.id, amount))

  @commands.command()
  async def payday(self, ctx):
        await ctx.send(core.account.payday(ctx.message.author.id))

  @commands.command()
  async def 賞(self, ctx, regi: discord.User = None, amount2=None):
        if (regi is not None and regi.bot) or ctx.author.bot:
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='該用戶是BOT，不能擁有一個帳戶')
            webhook.execute(); return
        if amount2 is None:
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請使用此格式指定賞金： `C罰 @國民名稱 金額`')
            webhook.execute(); return
        try:
            amount2 = int(amount2)
        except ValueError:
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請輸入整數。 ~~TMD這判斷函式我寫了N小時~~ ')
            webhook.execute(); return
        await ctx.send(core.account.賞(ctx.message.author.id, regi.id, amount2))

  @commands.command()
  async def rob(self, ctx, ramount=None):
        if ramount is None:
          webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請參照此格式輸入賭注的金額：`Crob 金額`。')
          webhook.execute(); return
        try:
            ramount = int(ramount)
        except ValueError:
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請輸入整數。 ~~TMD這判斷函式我寫了N小時~~ ')
            webhook.execute(); return
        await ctx.send(core.account.rob(ctx.message.author.id, ramount))

  @commands.command()
  async def srob(self, ctx):
        await ctx.send(core.account.rob(ctx.message.author.id, 3000))

  @commands.command()
  async def 罰(self, ctx, regi: discord.User = None, amount2=None):
        if (regi is not None and regi.bot) or ctx.author.bot:
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='該用戶是BOT，不能擁有一個帳戶')
            webhook.execute(); return
        if amount2 is None:
          webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請參照此格式指定罰金： `C罰 @國民名稱 金額`')
          webhook.execute(); return
        try:
            amount2 = int(amount2)
        except ValueError:
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請輸入整數。 ~~TMD這判斷函式我寫了N小時~~ ')
            webhook.execute(); return
        await ctx.send(core.account.罰(ctx.message.author.id, regi.id, amount2))

  @commands.command()
  async def count(self, ctx):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='已經有{}個國民已開戶。'.format(core.account.count()))
    webhook.execute()


def setup(bot):
  DiscordComponents(bot)
  bot.add_cog(Economy(bot))