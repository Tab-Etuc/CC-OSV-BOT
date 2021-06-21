import discord
from discord.ext import commands
from core.classes import Cog_Extension
import datetime, json, psutil
from config import *

with open('bot_info.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile) # 讀取設定檔

with open(r'./settings/message_process.json', mode='r', encoding='utf8') as MessageFile:
    MessageData = json.load(MessageFile)

class Main(Cog_Extension):
  @commands.command(aliases=['python', 'botinfo'])
  async def bot(self, ctx):
        values = psutil.virtual_memory()
        val2 = values.available * 0.001
        val3 = val2 * 0.001
        val4 = val3 * 0.001

        values2 = psutil.virtual_memory()
        value21 = values2.total
        values22 = value21 * 0.001
        values23 = values22 * 0.001
        values24 = values23 * 0.001

        embedve = discord.Embed(
            title="CC-OSV資訊", color=0x9370DB)
        embedve.add_field(
            name="延遲", value=f"延遲 - {round(self.bot.latency * 1000)}ms", inline=False)
        embedve.add_field(name='終端機統計數據', value=f'CPU使用率 {psutil.cpu_percent(1)}%'
                          f'\n(實際的CPU使用率可能有些許差異)'
                          f'\n'

                          f'\nCPU邏輯核心數 - {psutil.cpu_count()} '
                          f'\nCPU物理核心數 - {psutil.cpu_count(logical=False)}'
                          f'\n'

                          f'\nRAM 總數 - {round(values24, 2)} GB'
                          f'\n可用的 RAM 數 - {round(val4, 2)} GB')

        await ctx.send(embed=embedve)

  @commands.command(name = 'userinfo', aliases=['user', 'uinfo', 'ui'])
  async def userinfo(self, ctx, *, name=""):
        """Get user info. Ex: ~user @user"""
        if name:
            try:
                user = ctx.message.mentions[0]
            except IndexError:
                user = ctx.guild.get_member_named(name)
            try:
                if not user:
                    user = ctx.guild.get_member(int(name))
                if not user:
                    user = self.bot.get_user(int(name))
            except ValueError:
                pass
            if not user:
                await ctx.send('User not found :man_frowning_tone1:')
                return
        else:
            user = ctx.message.author

        if isinstance(user, discord.Member):
            role = user.top_role.name
            if role == "@everyone":
                role = "N/A"

        em = discord.Embed(colour=0x00CC99)
        em.add_field(name='User ID', value=f'`{user.id}`')
        if isinstance(user, discord.Member):
            if isinstance(user.activity, discord.Spotify):
                activity = "Listening " + user.activity.title
            elif user.activity is not None: 
                activity = str(user.activity.type)[13:].title() + ' ' + user.activity.name
            else:
                activity = None

            em.add_field(name='暱稱', value=f'`{user.nick}`')
            em.add_field(name='狀態', value=f'`{activity}`')
        em.add_field(name='用戶創建於：', value=f"`{user.created_at.__format__('%A, %d %B %Y @ %H:%M:%S')}`", inline=False)
        if isinstance(user, discord.Member):
            em.add_field(name='加入時間：', value=f"`{user.joined_at.__format__('%A, %d %B %Y @ %H:%M:%S')}`", inline=False)
        
        try:
            await ctx.send(embed=em)
        except Exception:
            await ctx.send("I don't have permission to send embeds here :disappointed_relieved:")
  
  @commands.command(name='sinfo', aliases=['server'])
  async def serverinfo(self, ctx, *, name:str = ""):
        """Get server info"""
        if name:
            server = None
            try:
                server = self.bot.get_guild(int(name))
                if not server:
                    return await ctx.send('Server not found :satellite_orbital:')
            except:
                for i in self.bot.guilds:
                    if i.name.lower() == name.lower():
                        server = i
                        break
                if not server:
                    return await ctx.send("Server not found :satellite_orbital: or maybe I'm not in it")
        else:
            server = ctx.guild
        # Count online members
        online = 0
        for i in server.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                online += 1
        # Count channels
        tchannel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])
        vchannel_count = len([x for x in server.channels if type(x) == discord.channel.VoiceChannel])
        # Count roles
        role_count = len(server.roles)

        # Create embed
        em = discord.Embed(color=0x00CC99)
        em.add_field(name='國名', value=f'`{server.name}`')
        em.add_field(name='總統', value=f'`煞氣TM爺爺#5692`', inline=False)
        em.add_field(name='國民數', value=f'`{server.member_count}`')
        em.add_field(name='表情符號數', value=f'`60`')
        em.add_field(name='文字頻道數', value=f'`{tchannel_count}`')
        em.add_field(name='語音頻道數', value=f'`{vchannel_count}`')
        em.add_field(name='驗證級別', value=f'`無`')
        em.add_field(name='身分組數', value=f'`{role_count}`')
        em.add_field(name='建立於', value=f"`{server.created_at.__format__('%Y 4月20號 星期二 @ %H:%M:%S')}`", inline=False)
        em.set_thumbnail(url=server.icon_url)
        em.set_footer(text='Server ID: %s' % server.id)

        try:
            await ctx.send(embed=em)
        except Exception:
            await ctx.send("I don't have permission to send embeds here :disappointed_relieved:")
  
  @commands.command()
  async def ping(self, ctx):
        ping=abs(int(self.bot.latency*1000))
        embed=discord.Embed(title=f'{ping}(ms)', color=0x73ff00, timestamp=datetime.datetime.now(datetime.timezone.utc))
        embed.set_author(name='延遲') 
        embed.set_footer(text=f'由{ctx.author}請求的鏈接')
        await ctx.send(embed=embed)
        print(f'【Bot】{ctx.author} take bot\'s ping')
        
  @commands.command()
  async def Nitro(self, ctx, style:int=1):
        await ctx.message.delete()
        if style == 1:
            embed=discord.Embed(title='**Nitro Classic**', url='https://www.youtube.com/watch?v=rTgj1HxmUbg', description='Expires in 48 hours', color=0x9089da)
            embed.set_author(name='A WILD GIFT APPEARS!')
            embed.set_thumbnail(url='https://i.imgur.com/yQyZ24F.png')
            await ctx.send(embed=embed)               
def setup(bot):
    bot.add_cog(Main(bot))