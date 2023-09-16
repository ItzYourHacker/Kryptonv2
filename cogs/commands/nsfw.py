from __future__ import annotations
############MODULES#############
import discord
import requests
import datetime
from discord.ext import commands
from utils.Tools import *
from core import Cog, Astroz, Context
import aiohttp
import datetime


class Nsfw(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(name="Nsfw", invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @ignore_check()
    async def nsfw(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @nsfw.command(name="4k")
    @blacklist_check()
    @ignore_check()
    async def _4k(self, ctx):
        ok = requests.get("http://api.nekos.fun:8080/api/4k")
        data = ok.json()
        image = data["image"]
        if ctx.channel.is_nsfw() != True:
            await ctx.reply(embed=discord.Embed(
                description=
                "Please Enable The NSFW Option From Channel Setting To Continue Forward:",
                color=0x2f3136,
                timestamp=datetime.datetime.utcnow()
            ).set_image(
                url=
                "https://support.discord.com/hc/article_attachments/4580654542103/unnamed.png"
            ).set_thumbnail(url=ctx.author.display_avatar.url))
        else:
            embed = discord.Embed(color=0x2f3136,
                                  timestamp=datetime.datetime.utcnow())
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @nsfw.command(name="pussy")
    async def _pussy(self, ctx):
        ok = requests.get("http://api.nekos.fun:8080/api/pussy")
        data = ok.json()
        image = data["image"]
        if ctx.channel.is_nsfw() != True:
            await ctx.reply(embed=discord.Embed(
                description=
                "Please Enable The NSFW Option From Channel Setting To Continue Forward:",
                color=0x2f3136,
                timestamp=datetime.datetime.utcnow()
            ).set_image(
                url=
                "https://support.discord.com/hc/article_attachments/4580654542103/unnamed.png"
            ).set_thumbnail(url=ctx.author.display_avatar.url))
        else:
            embed = discord.Embed(color=0x2f3136,
                                  timestamp=datetime.datetime.utcnow())
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @nsfw.command(name="boobs")
    async def _boobs(self, ctx):
        ok = requests.get("http://api.nekos.fun:8080/api/boobs")
        data = ok.json()
        image = data["image"]
        if ctx.channel.is_nsfw() != True:
            await ctx.reply(embed=discord.Embed(
                description=
                "Please Enable The NSFW Option From Channel Setting To Continue Forward:",
                color=0x2f3136,
                timestamp=datetime.datetime.utcnow()
            ).set_image(
                url=
                "https://support.discord.com/hc/article_attachments/4580654542103/unnamed.png"
            ).set_thumbnail(url=ctx.author.display_avatar.url))
        else:
            embed = discord.Embed(color=0x2f3136,
                                  timestamp=datetime.datetime.utcnow())
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @nsfw.command(name="lewd")
    async def _lewd(self, ctx):
        ok = requests.get("http://api.nekos.fun:8080/api/lewd")
        data = ok.json()
        image = data["image"]
        if ctx.channel.is_nsfw() != True:
            await ctx.reply(embed=discord.Embed(
                description=
                "Please Enable The NSFW Option From Channel Setting To Continue Forward:",
                color=0x2f3136,
                timestamp=datetime.datetime.utcnow()
            ).set_image(
                url=
                "https://support.discord.com/hc/article_attachments/4580654542103/unnamed.png"
            ).set_thumbnail(url=ctx.author.display_avatar.url))
        else:
            embed = discord.Embed(color=0x2f3136,
                                  timestamp=datetime.datetime.utcnow())
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @nsfw.command(name="lesbian")
    async def _lesbian(self, ctx):
        ok = requests.get("http://api.nekos.fun:8080/api/lesbian")
        data = ok.json()
        image = data["image"]
        if ctx.channel.is_nsfw() != True:
            await ctx.reply(embed=discord.Embed(
                description=
                "Please Enable The NSFW Option From Channel Setting To Continue Forward:",
                color=0x2f3136,
                timestamp=datetime.datetime.utcnow()
            ).set_image(
                url=
                "https://support.discord.com/hc/article_attachments/4580654542103/unnamed.png"
            ).set_thumbnail(url=ctx.author.display_avatar.url))
        else:
            embed = discord.Embed(color=0x2f3136,
                                  timestamp=datetime.datetime.utcnow())
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @nsfw.command(name="blowjob")
    async def _blowjob(self, ctx):
        ok = requests.get("http://api.nekos.fun:8080/api/blowjob")
        data = ok.json()
        image = data["image"]
        if ctx.channel.is_nsfw() != True:
            await ctx.reply(embed=discord.Embed(
                description=
                "Please Enable The NSFW Option From Channel Setting To Continue Forward:",
                color=0x2f3136,
                timestamp=datetime.datetime.utcnow()
            ).set_image(
                url=
                "https://support.discord.com/hc/article_attachments/4580654542103/unnamed.png"
            ).set_thumbnail(url=ctx.author.display_avatar.url))
        else:
            embed = discord.Embed(color=0x2f3136,
                                  timestamp=datetime.datetime.utcnow())
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @nsfw.command(name="cum")
    async def _cum(self, ctx):
        ok = requests.get("http://api.nekos.fun:8080/api/cum")
        data = ok.json()
        image = data["image"]
        if ctx.channel.is_nsfw() != True:
            await ctx.reply(embed=discord.Embed(
                description=
                "Please Enable The NSFW Option From Channel Setting To Continue Forward:",
                color=0x2f3136,
                timestamp=datetime.datetime.utcnow()
            ).set_image(
                url=
                "https://support.discord.com/hc/article_attachments/4580654542103/unnamed.png"
            ).set_thumbnail(url=ctx.author.display_avatar.url))
        else:
            embed = discord.Embed(color=0x2f3136,
                                  timestamp=datetime.datetime.utcnow())
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @nsfw.command(name="gasm")
    async def _gasm(self, ctx):
        ok = requests.get("http://api.nekos.fun:8080/api/gasm")
        data = ok.json()
        image = data["image"]
        if ctx.channel.is_nsfw() != True:
            await ctx.reply(embed=discord.Embed(
                description=
                "Please Enable The NSFW Option From Channel Setting To Continue Forward:",
                color=0x2f3136,
                timestamp=datetime.datetime.utcnow()
            ).set_image(
                url=
                "https://support.discord.com/hc/article_attachments/4580654542103/unnamed.png"
            ).set_thumbnail(url=ctx.author.display_avatar.url))
        else:
            embed = discord.Embed(color=0x2f3136,
                                  timestamp=datetime.datetime.utcnow())
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @nsfw.command(name="hentai")
    async def _hentai(self, ctx):
        ok = requests.get("http://api.nekos.fun:8080/api/hentai")
        data = ok.json()
        image = data["image"]
        if ctx.channel.is_nsfw() != True:
            await ctx.reply(embed=discord.Embed(
                description=
                "Please Enable The NSFW Option From Channel Setting To Continue Forward:",
                color=0x2f3136,
                timestamp=datetime.datetime.utcnow()
            ).set_image(
                url=
                "https://support.discord.com/hc/article_attachments/4580654542103/unnamed.png"
            ).set_thumbnail(url=ctx.author.display_avatar.url))
        else:
            embed = discord.Embed(color=0x2f3136,
                                  timestamp=datetime.datetime.utcnow())
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @nsfw.command(name="anal")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def anal(self, ctx: Context):
        """To get Random Anal"""
        url = "https://nekobot.xyz/api/image"
        params = {"type": "anal"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(title="Anal", timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="gonewild")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def gonewild(self, ctx: Context):
        """
        To get Random GoneWild
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "gonewild"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="hanal")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def hanal(self, ctx: Context):
        """To get Random Hentai Anal"""
        url = "https://nekobot.xyz/api/image"
        params = {"type": "hanal"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="holo")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def holo(self, ctx: Context):
        """
        To get Random Holo
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "holo"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="neko")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def neko(self, ctx: Context):
        """
        To get Random Neko
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "neko"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="hneko")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def hneko(self, ctx: Context):
        """
        To get Random Hneko
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "hneko"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="hkitsune")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def hkitsune(self, ctx: Context):
        """
        To get Random Hkitsune
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "hkitsune"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="kemonomimi")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def kemonomimi(self, ctx: Context):
        """
        To get Random Kemonomimi
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "kemonomimi"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="pgif")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def pgif(self, ctx: Context):
        """
        To get Random PornGif
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "pgif"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="kanna")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def kanna(self, ctx: Context):
        """
        To get Random Kanna
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "kanna"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="thigh")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def thigh(self, ctx: Context):
        """
        To get Random Thigh
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "thigh"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="hthigh")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def hthigh(self, ctx: Context):
        """
        To get Random Hentai Thigh
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "hthigh"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="paizuri")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def paizuri(self, ctx: Context):
        """
        To get Random Paizuri
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "paizuri"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="tentacle")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def tentacle(self, ctx: Context):
        """
        To get Random Tentacle Porn
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "tentacle"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="hboobs")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def hboobs(self, ctx: Context):
        """
        To get Random Hentai Boobs
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "hboobs"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="yaoi")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def yaoi(self, ctx: Context):
        """
        To get Random Yaoi
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "yaoi"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="hmidriff")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def hmidriff(self, ctx: Context):
        """
        To get Random Hmidriff
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "hmidriff"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="hass")
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def hass(self, ctx: Context):
        """
        To get Random Hentai Ass
        """
        url = "https://nekobot.xyz/api/image"
        params = {"type": "hass"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["message"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command(name="randomnsfw", aliases=["randnsfw"])
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def randomnsfw(self, ctx: Context, *, subreddit: str = None):
        """
        To get Random NSFW from subreddit.
        """
        if subreddit is None:
            subreddit = "NSFW"
        end = time() + 60
        while time() < end:
            url = f"https://memes.blademaker.tv/api/{subreddit}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    if r.status == 200:
                        res = await r.json()
                    else:
                        return
            if res["nsfw"]:
                break

        img = res["image"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)

    @nsfw.command()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    async def n(self, ctx: Context):
        """
        Best command I guess. It return random ^^
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://scathach.redsplit.org/v3/nsfw/gif/") as r:
                if r.status == 200:
                    res = await r.json()
                else:
                    return

        img = res["url"]

        em = discord.Embed(timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"{ctx.author.name}")
        em.set_image(url=img)

        await ctx.reply(embed=em)
