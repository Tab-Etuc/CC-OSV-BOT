import discord
from discord import utils
from discord.ext import commands
from pymongo import MongoClient
import os

conn = MongoClient(os.getenv("MONGODB_URI"))
db = conn["CC-OSV-NQN"]

nqn = db["nqn"]

class CL3I(commands.Cog):
    def __init__(self, client):
        self.client = client
    async def getemote(self, arg):
        emoji = utils.get(self.client.emojis, name=arg.strip(":"))

        if emoji is not None:
            if emoji.animated:
                add = "a"
            else:
                add = ""
            return f"<{add}:{emoji.name}:{emoji.id}>"
        else:
            return None

    async def getinstr(self, content):
        ret = []

        spc = content.split(" ")
        cnt = content.split(":")

        if len(cnt) > 1:
            for item in spc:
                if item.count(":") > 1:
                    wr = ""
                    if item.startswith("<") and item.endswith(">"):
                        ret.append(item)
                    else:
                        cnt = 0
                        for i in item:
                            if cnt == 2:
                                aaa = wr.replace(" ", "")
                                ret.append(aaa)
                                wr = ""
                                cnt = 0
                            if i != ":":
                                wr += i
                            else:
                                if wr == "" or cnt == 1:
                                    wr += " : "
                                    cnt += 1
                                else:
                                    aaa = wr.replace(" ", "")
                                    ret.append(aaa)
                                    wr = ":"
                                    cnt = 1

                        aaa = wr.replace(" ", "")
                        ret.append(aaa)
                else:
                    ret.append(item)
        else:
            return content

        return ret
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild or not message.content:
            return
        if "cl3i" in message.content:
                ret = "好喔"
                webhooks = await message.channel.webhooks()
                webhook = utils.get(webhooks, name = "CC-OSV-NQN ")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "CC-OSV-NQN ")

                await webhook.send(ret, username = message.author.nick, avatar_url = message.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
                await message.delete()
                await webhook.delete()
        if "c襖喔"  in message.content:
                ret = "好喔"
                webhooks = await message.channel.webhooks()
                webhook = utils.get(webhooks, name = "CC-OSV-NQN ")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "CC-OSV-NQN ")

                await webhook.send(ret, username = message.author.nick, avatar_url = message.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
                await message.delete()
                await webhook.delete()
        if "CL3I"  in message.content:
                ret = "好喔"
                webhooks = await message.channel.webhooks()
                webhook = utils.get(webhooks, name = "CC-OSV-NQN ")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "CC-OSV-NQN ")

                await webhook.send(ret, username = message.author.nick, avatar_url = message.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))                  
                await message.delete() 
                await webhook.delete()
        kek = nqn.find_one({"_id": message.guild.id})
        if kek == None:
            return

        if ":" in message.content:
            msg = await self.getinstr(message.content)
            ret = ""
            em = False
            smth = message.content.split(":")
            if len(smth) > 1:
                for word in msg:
                    if word.startswith(":") and word.endswith(":") and len(word) > 1:
                        emoji = await self.getemote(word)
                        if emoji is not None:
                            em = True
                            ret += f" {emoji}"
                        else:
                            ret += f" {word}"
                    else:
                        ret += f" {word}"
            else:
                ret += msg

            if em:
                webhooks = await message.channel.webhooks()
                await message.delete()
                webhook = utils.get(webhooks, name = "CC-OSV-NQN ")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "CC-OSV-NQN ")
    
                await webhook.send(ret, username = message.author.name, avatar_url = message.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
                await webhook.delete()
                             

  

def setup(client):
    client.add_cog(CL3I(client))