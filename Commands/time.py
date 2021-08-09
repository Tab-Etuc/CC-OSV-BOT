import asyncio
from discord.ext import commands
from datetime import datetime, timezone, timedelta
tz = timezone(timedelta(hours=+8))

class Time(commands.Cog):
  def __init__(self,bot, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.bot = bot

    async def interval():
      await self.bot.wait_until_ready()
      while not self.bot.is_closed():
        now2 = datetime.now(tz).strftime("📅次年●%m月%d日●")
        now = datetime.now(tz).strftime("🕠現在時刻： %H 點")
        channel = self.bot.get_channel(852346393141182484) # ID des Channels
        channel2 = self.bot.get_channel(852364573095755808)
        time = datetime.now(tz).strftime('[%Y-%m-%d] [%H:%M]')
        print(f'已於：{time} 更換頻道時間。')
        await channel.edit(name=now) # Füge hier den ersten Channel Namen ein zu dem gewechselt werden soll.
        await asyncio.sleep(1)
        await channel2.edit(name=now2) # Füge hier den ersten Channel Namen ein zu dem gewechselt werden soll.        
        await asyncio.sleep(310) # Hier die sleep dauer // Nicht unter 300 [Discord - RateLimit]
    self.bg_task = self.bot.loop.create_task(interval())

def setup(bot):
   bot.add_cog(Time(bot))