import base64
import binascii
import codecs
import discord
from io import BytesIO
from discord.ext import commands
from discord.ext.commands import clean_content
from discord.ext.commands.errors import BadArgument
from utils import default, http
from core.classes import Cog_Extension


async def detect_file(ctx):
    print(ctx.message.attachments)
    if ctx.message.attachments:
        file = ctx.message.attachments[0].url

        if not file.endswith(".txt"):
            raise BadArgument("只接受txt檔")
    else:
        raise
    try:
        content = await http.get(file, no_cache=True)
    except Exception:
        raise BadArgument("無效的txt檔")

    if not content:
        raise BadArgument("你提供的檔案是空的")
    return content



async def encrypt_out(ctx, convert, _input):
    if not _input:
        return await ctx.send(f"你不打算給我任何東西來編碼/解碼？ **{ctx.author.name}**")

    async with ctx.channel.typing():
        if len(_input) > 1900:
            try:
                data = BytesIO(_input.encode('utf-8'))
            except AttributeError:
                data = BytesIO(_input)

            try:
                return await ctx.send(
                    content=f"📑 **{convert}**",
                    file=discord.File(data, filename=default.timetext("Encryption"))
                )
            except discord.HTTPException:
                return await ctx.send(f"The file I returned was over 8 MB, sorry {ctx.author.name}...")

        try:
            await ctx.send(f"📑 **{convert}**```fix\n{_input.decode('UTF-8')}```")
        except AttributeError:
            await ctx.send(f"📑 **{convert}**```fix\n{_input}```")


class Encryption(Cog_Extension, name="加密"):

    @commands.cooldown(1, 10, commands.BucketType.user)     
    @commands.group(name="編碼", aliases=["encode","ENCODE"])
    async def encode(self, ctx):
        """ 所有編碼的方法。 """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @commands.group(name="解碼", aliases=["decode","DECODE"])
    async def decode(self, ctx):
        """ 所有解碼的方法。 """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @encode.command(name="base32", aliases=["b32"])
    async def encode_base32(self, ctx, *, _input: clean_content = None):
        if not _input:
            _input = await detect_file(ctx)

        await encrypt_out(
            ctx, "Text -> base32", base64.b32encode(_input.encode('UTF-8'))
        )



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @decode.command(name="base32", aliases=["b32"])
    async def decode_base32(self, ctx, *, _input: clean_content = None):
        if not _input:
            _input = await detect_file(ctx)

        try:
            await encrypt_out(ctx, "base32 -> Text", base64.b32decode(_input.encode('UTF-8')))
        except Exception:
            await ctx.send("Invalid base32...")



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @encode.command(name="base64", aliases=["b64"])
    async def encode_base64(self, ctx, *, _input: clean_content = None):
        """ Encode in base64 """
        if not _input:
            _input = await detect_file(ctx)

        await encrypt_out(
            ctx, "Text -> base64", base64.urlsafe_b64encode(_input.encode('UTF-8'))
        )



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @decode.command(name="base64", aliases=["b64"])
    async def decode_base64(self, ctx, *, _input: clean_content = None):
        """ Decode in base64 """
        if not _input:
            _input = await detect_file(ctx)

        try:
            await encrypt_out(ctx, "base64 -> Text", base64.urlsafe_b64decode(_input.encode('UTF-8')))
        except Exception:
            await ctx.send("Invalid base64...")



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @encode.command(name="rot13", aliases=["r13"])
    async def encode_rot13(self, ctx, *, _input: clean_content = None):
        """ Encode in rot13 """
        if not _input:
            _input = await detect_file(ctx)

        await encrypt_out(
            ctx, "Text -> rot13", codecs.decode(_input, 'rot_13')
        )



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @decode.command(name="rot13", aliases=["r13"])
    async def decode_rot13(self, ctx, *, _input: clean_content = None):
        """ Decode in rot13 """
        if not _input:
            _input = await detect_file(ctx)

        try:
            await encrypt_out(ctx, "rot13 -> Text", codecs.decode(_input, 'rot_13'))
        except Exception:
            await ctx.send("Invalid rot13...")



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @encode.command(name="hex")
    async def encode_hex(self, ctx, *, _input: clean_content = None):
        """ Encode in hex """
        if not _input:
            _input = await detect_file(ctx)

        await encrypt_out(
            ctx, "Text -> hex",
            binascii.hexlify(_input.encode('UTF-8'))
        )



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @decode.command(name="hex")
    async def decode_hex(self, ctx, *, _input: clean_content = None):
        """ Decode in hex """
        if not _input:
            _input = await detect_file(ctx)

        try:
            await encrypt_out(ctx, "hex -> Text", binascii.unhexlify(_input.encode('UTF-8')))
        except Exception:
            await ctx.send("無效的 hex...")



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @encode.command(name="base85", aliases=["b85"])
    async def encode_base85(self, ctx, *, _input: clean_content = None):
        """ Encode in base85 """
        if not _input:
            _input = await detect_file(ctx)

        await encrypt_out(
            ctx, "Text -> base85",
            base64.b85encode(_input.encode('UTF-8'))
        )



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @decode.command(name="base85", aliases=["b85"])
    async def decode_base85(self, ctx, *, _input: clean_content = None):
        """ Decode in base85 """
        if not _input:
            _input = await detect_file(ctx)

        try:
            await encrypt_out(ctx, "base85 -> Text", base64.b85decode(_input.encode('UTF-8')))
        except Exception:
            await ctx.send("無效的 base85...")



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @encode.command(name="ascii85", aliases=["a85"])
    async def encode_ascii85(self, ctx, *, _input: clean_content = None):
        """ Encode in ASCII85 """
        if not _input:
            _input = await detect_file(ctx)

        await encrypt_out(
            ctx, "Text -> ASCII85",
            base64.a85encode(_input.encode('UTF-8'))
        )



    @commands.cooldown(1, 10, commands.BucketType.user)     
    @decode.command(name="ascii85", aliases=["a85"])
    async def decode_ascii85(self, ctx, *, _input: clean_content = None):
        """ Decode in ASCII85 """
        if not _input:
            _input = await detect_file(ctx)

        try:
            await encrypt_out(ctx, "ASCII85 -> Text", base64.a85decode(_input.encode('UTF-8')))
        except Exception:
            await ctx.send("無效的 ASCII85...")



def setup(bot):
    bot.add_cog(Encryption(bot))