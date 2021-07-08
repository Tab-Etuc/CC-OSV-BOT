from discord.ext import commands
from core.classes import Cog_Extension
import asyncio, os
from pymongo import MongoClient

auth_url = os.getenv("MONGODB_URI")

    
class Task(Cog_Extension):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    async def interval():
      await self.bot.wait_until_ready()
      while not self.bot.is_closed():
        cluster = MongoClient(auth_url)
        db = cluster["Economy"]
        cursor = db["Bank"]      
        execute = {"$set": {"銀行餘額": {"$multiply": ["$銀行餘額", "$利息"]}}}
        cursor.update_many({}, [execute])
        execute2 = {"$set": {"現金": {"$add": ["$現金", "$真實的薪資"]}}}
        db.Bank.update_many({}, [execute2])
        execute3 = {"$set": {"$銀行餘額": "$存款額度"}}
        db.Bank.update_many({"銀行餘額":{"$gt" : "$存款額度"}}, [execute3])
        db.Bank.update_one({"_id": "國庫"}, {"$inc": {"當周所得": 1100132}})

        print("已進行例行性的給予薪資")
        print("已進行例行性的給予利息")
        await asyncio.sleep(7200)
    self.bg_task = self.bot.loop.create_task(interval())

  @commands.command()
  @commands.is_owner()
  async def test(self,ctx):
      cluster = MongoClient(auth_url)
      db = cluster["Economy"]
      execute3 = {"$set": {"$銀行餘額": "$存款額度"}}
      db.Bank.update_many({}, [execute3])

  @commands.command()
  @commands.is_owner()
  async def test2(self,ctx):
    cluster = MongoClient(auth_url)
    db = cluster["Economy"]
    cursor = db["Bank"]
    execute = {"$set": {"現金": {"$multiply": ["$銀行餘額", "$利息"]}}}
    cursor.update_many({}, [execute])

  @commands.command()
  @commands.is_owner()
  async def test3(self,ctx):
        cluster = MongoClient(auth_url)
        db = cluster["Economy"]

        db.Bank.update_one({"_id": "國庫"}, {"$inc": {"當周所得": 1100132}})
  


def setup(bot):
   bot.add_cog(Task(bot))