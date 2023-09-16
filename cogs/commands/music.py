import discord
import os
import wavelink
from discord.ext import commands
import datetime
from wavelink.ext import spotify
import re
import typing
import requests
import random 
from discord import app_commands
import urllib
from utils.Tools import *
import asyncio 
from discord.ui import Button, View,button


URL_REG = re.compile(r'https?://(?:www\.)?.+')




async def setfilter(player: wavelink.Player, filter):
    filter = filter.lower()
    if filter == "reset":
        await player.set_filter(wavelink.Filter())
        if player.volume == 500:
            await player.set_volume(100)
    elif filter == "lofi":
        await player.set_filter(wavelink.Filter(player._filter, timescale=wavelink.Timescale(speed =  0.7500000238418579, pitch = 0.800000011920929, rate = 1)))
    elif filter == "nightcore":
        await player.set_filter(wavelink.Filter(player._filter, timescale=wavelink.Timescale(speed = 1.2999999523162842, pitch = 1.2999999523163953, rate = 1)))
    elif filter == "8d":
        await player.set_filter(wavelink.Filter(player._filter, rotation=wavelink.Rotation(speed=0.29999))) 
    elif filter == "damon":
        await player.set_filter(wavelink.Filter(player._filter, timescale=wavelink.Timescale(speed =  0.6899999521238, pitch = 0.7999990000011920929, rate = 1)))
    elif filter == "daycore":
        await player.set_filter(wavelink.Filter(player._filter, timescale=wavelink.Timescale(speed =  0.8999999523162842, pitch = 0.9999999523162842, rate = 1)))
    elif filter == "bassboost":
        bands = [(0, 0.2), (1, 0.15), (2, 0.1), (3, 0.05), (4, 0.0),
                 (5, -0.05), (6, -0.1), (7, -0.1), (8, -0.1), (9, -0.1),
                 (10, -0.1), (11, -0.1), (12, -0.1), (13, -0.1), (14, -0.1)]
        await player.set_filter(wavelink.Filter(player._filter, equalizer=wavelink.Equalizer(name="MyOwnFilter", bands=bands)))
        
    elif filter == "121":
        await player.set_filter(wavelink.Filter(player._filter, equalizer=wavelink.Equalizer(name = 'CustomEqualizer', bands=[(0, 1), (1, 1),(2, 1),(3, 1),(4, 1),(4, 1),(5, 1),(6, 1),(7, 1),(8, 1),(9, 1),(10, 1),(11, 1),(12, 1),(13, 1),(14, 1),(15, 1)])))
        await player.set_volume(500)
    elif filter == "slowmode":
        await player.set_filter(wavelink.Filter(player._filter, timescale=wavelink.Timescale(speed = 0.8)))

class filters(discord.ui.Select):
    def __init__(self, bot, ctx: commands.Context, vc: wavelink.Player):
        options = []
        x = ["lofi", "nightcore", "daycore","bassboost", "8d", "damon", "121", "reset"]
        for i in x:
            options.append(discord.SelectOption(label=f"{i.capitalize()}",emoji="<a:premium:1101138017864912996>",description=f"Enables {i.capitalize()} Filter",value=i))
        super().__init__(placeholder="Select Filter",
            row=1,
            min_values=1,
            max_values=1,
            options=options,
        )
        self.ctx = ctx
        self.vc = vc
        self.bot = bot
        
    async def interaction_check(self, interaction: discord.Interaction):
        c = False
        for i in self.ctx.guild.me.voice.channel.members:
            if i.id == interaction.user.id:
                c = True
                break
        if c:
            return True
        else:
            await interaction.response.send_message(f"Um, Looks like you are not in the voice channel .", ephemeral=True)
            return False
        
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "reset":
            self.vc.filterr = "None"
            
        else:
            self.vc.filterr = self.values[0].title()
        await setfilter(self.vc, self.values[0])
        em = discord.Embed(color=0x2f3136)
        em.set_footer(text=f"| Enabled {self.values[0].capitalize()} filter for current player .", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=em, ephemeral=True)
        await interaction.message.edit(view=self.view)




class interface(discord.ui.View):
    def __init__(self, bot, ctx: commands.Context, panel=False, first=False, q: list=list()):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.bot = bot
        self.value = None
        self.panel = panel
        self.vc: wavelink.Player = ctx.voice_client
        self.add_item(filters(bot, ctx, self.vc))
        
        if first:
            for i in self.children:
                try:
                    if i.custom_id == "pfav":
                        continue
                except:
                    pass
                i.disabled = True
    
    async def interaction_check(self, interaction: discord.Interaction):
        c = False
        if self.ctx.guild.me.voice is None:
            return True
        for i in self.ctx.guild.me.voice.channel.members:
            if i.id == interaction.user.id:
                c = True
                break
        if c:
            return True
        else:
            await interaction.response.send_message(f"Um, Looks like you are not in the voice channel .", ephemeral=True)
            return False
 
 
    @discord.ui.button(emoji="<:Pause:1089397454513917962>", custom_id='rp', row=2, style=discord.ButtonStyle.grey)
    async def rp(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.vc
        if not vc.is_paused():
            await vc.pause()
            button.emoji = "<:resume:1089397456216801330>"
            await interaction.response.edit_message(view=self)
        else:
            await vc.resume()
            button.emoji = "<:Pause:1089397454513917962>"
            await interaction.response.edit_message(view=self)    
###############################

    @discord.ui.button(emoji="<:Skip:1089397466362810459>", custom_id='skip', row=2, style=discord.ButtonStyle.grey)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        await self.vc.stop()
        emb2 = discord.Embed(color=0x2f3136)
        emb2.set_footer(text="| Skipped the song .", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=emb2, ephemeral=True)
    
          
    @discord.ui.button(emoji="<:replay:1089397458100027422>", custom_id='loop', row=2, style=discord.ButtonStyle.gray)
    async def loop(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.vc
        try:
            loop = getattr(vc, "loop")
        
        except:
            loop = False      
        if not vc.is_playing():
            return
        if not vc:
            return  
        if loop:
            setattr(vc, "loop", False)
            em = discord.Embed(color=0x2f3136)
            em.set_footer(text="| Looping is Now disabled .", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=em, ephemeral=True)

        setattr(vc, "loop", True)
        em = discord.Embed(color=0x2f3136)
        em.set_footer(text="| Looping is now set to current song .", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=em, ephemeral=True)
      
  
    
    @discord.ui.button(emoji="<:Stop:1089397470661980261>", custom_id='stop', row=2, style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        ctx = self.ctx
       # ctx.voice_client.autoplay = False
        await self.vc.stop()
        await self.vc.disconnect()
        em = discord.Embed(color=0x2f3136)
        em.set_footer(text="| Destroyed the queue and stopped the player .", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=em, ephemeral=True)
        


   
    @discord.ui.button(emoji="<:shuffle:1089397459752587274>", custom_id='shuf', row=2, style=discord.ButtonStyle.success)
    async def shuf(self, interaction: discord.Interaction, button: discord.ui.Button):
        q = self.vc.queue
        if len(q) <= 1:
            em = discord.Embed(color=0x2f3136)
            em.set_footer(text="| The length of queue must be more than 2 for shuffle .", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=em, ephemeral=True)
            
        v = list(q.copy())
        random.shuffle(v)
        self.vc.queue.clear()
        for i in v:
            await self.vc.queue.put_wait(i)
        em = discord.Embed(color=0x2f3136)
        em.set_footer(text="| Shuffled the cuurent queue .", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=em, ephemeral=True)




def converttime(seconds):
    time = int(seconds)
    month = time // (30 * 24 * 3600)
    time = time % (24 * 3600)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    ls = []
    if month != 0:
        ls.append(f"{month}mo")
    if day != 0:
        ls.append(f"{day}d")
    if hour != 0:
        ls.append(f"{hour}h")
    if minutes != 0:
        ls.append(f"{minutes}m")
    if seconds != 0:
        ls.append(f"{seconds}s")
    return ' '.join(ls)
       
class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.color = 0x2f3136
    async def create_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host="lavalink.ordinaryender.my.eu.org",
            port=443,
            password="ordinarylavalink",
            https=True,
            spotify_client=spotify.SpotifyClient(
                client_id="9d340e339c10432e9c478742931d64e9",
                client_secret="2e23b2ab872046eca5fdf3379006f7de"))

             
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog is now ready!")
        await self.bot.loop.create_task(self.create_nodes())

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.identifier}> is now Ready!")
        

        
        
    @commands.hybrid_command(name="play",help="Plays song in your voice channel.", aliases=['p'], usage="play <query>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def play(self, ctx: commands.Context, *, query: str):
        if not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(
               color=self.color)
            embed.set_author(name="You are not connected to any of the voice channel .", icon_url=ctx.author.display_avatar.url)
            return await ctx.reply(embed=embed)     
        elif not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
        elif ctx.author.voice.channel.id != ctx.guild.me.voice.channel.id:
            if ctx.voice_client.is_playing():
                embed = discord.Embed(
                    olor=self.color)
                embed.set_author(name=f"Songs are already being played in {ctx.guild.me.voice.channel.name} .", icon_url=ctx.author.display_avatar.url)
                return await ctx.reply(embed=embed)
            else:
                await ctx.voice_client.disconnect()
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
        else:
            vc: wavelink.Player = ctx.voice_client
        if "youtube.com" in query:
            return await ctx.reply("Songs from Youtube are not supported")
        if 'https://open.spotify.com' in query:
            if vc.queue.is_empty and not vc.is_playing():
                track = await spotify.SpotifyTrack.search(query=query,
                                                          return_first=True)
                author = track.author or "None"
                await vc.play(track)
                emb = discord.Embed(description=f"\n[{track.title}](https://discord.gg/oxytech)", color=self.color).set_author(name="| Now Playing", icon_url=ctx.author.display_avatar.url)
                emb.add_field(name="Duration", value=f"[{round(track.duration / 60, 2)}](https://discord.gg/oxytech)")
                emb.add_field(name="Requester", value=f"[{str(ctx.author)}](https://discord.com/users/{ctx.author.id})")
                emb.add_field(name="Artist", value=f"[{author}](https://discord.gg/oxytech)")
                emb.set_thumbnail(url=track.thumb or "None")
                v = interface(self.bot, ctx, False, False)
                return await ctx.send(embed=emb, view=v) 
            else:
                track = await spotify.SpotifyTrack.search(query=query,
                                                          return_first=True)
                await vc.queue.put_wait(track)
                embed = discord.Embed(
                    description=
                    f'[{track.title}](https://discord.gg/Oxytech) Added To The Queue',
                    color=0x2f3136)

                embed.set_author(name="ADDED TO QUEUE",
                                 icon_url=ctx.author.display_avatar.url)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                return await ctx.send(embed=embed) 
                
                
            
        
        
            
        tracks = await wavelink.YouTubeTrack.search(query=query)
        
        self.mlist = tracks
        btn1 = Button(label="", style=discord.ButtonStyle.gray, emoji="1️⃣",row=1)
        btn2 = Button(label="", style=discord.ButtonStyle.gray, emoji="2️⃣",row=1)
        btn3 = Button(label="", style=discord.ButtonStyle.gray, emoji="3️⃣",row=1)
        btn4 = Button(label="", style=discord.ButtonStyle.gray, emoji="4️⃣",row=1)
        btn5 = Button(label="", style=discord.ButtonStyle.gray, emoji="5️⃣",row=1)
        btn6 = Button(label="", style=discord.ButtonStyle.gray, emoji="⏹️",row=2)
        async def btn1_(interaction: discord.Interaction):
          await self.damn(vc=vc, index=0, tracks=tracks, ctx=ctx)
          btn1.disabled = True
          
        async def btn2_(interaction: discord.Interaction):
          await self.damn(vc=vc, index=1, tracks=tracks, ctx=ctx)
          btn2.disabled = True
        async def btn3_(interaction: discord.Interaction):
          await self.damn(vc=vc, index=2, tracks=tracks, ctx=ctx)
          btn3.disabled = True
        async def btn4_(interaction: discord.Interaction):
          await self.damn(vc=vc, index=3, tracks=tracks, ctx=ctx)
          btn4.disabled = True
        async def btn5_(interaction: discord.Interaction):
          await self.damn(vc=vc, index=4, tracks=tracks, ctx=ctx)
          btn5.disabled = True
        async def btn6_(interaction: discord.Interaction):
          await vc.smex.delete()
        btn1.callback = btn1_
        btn2.callback = btn2_
        btn3.callback = btn3_
        btn4.callback = btn4_
        btn5.callback = btn5_
        btn6.callback = btn6_
        view = View()
        view.add_item(btn1)
        view.add_item(btn2)
        view.add_item(btn3)
        view.add_item(btn4)
        view.add_item(btn5)
        view.add_item(btn6)
        embed = discord.Embed(
            description=(
                "\n".join(f"**`[{i+1}]` | {t.title}**" for i, t in enumerate(tracks[:5]))
            ),
            color=0x2f3136
        )
        embed.set_author(name="Multiple tracks found. Please choose one of the following", icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.display_avatar.url)
        smex = await ctx.send(embed=embed, view=view)
        vc.smex = smex    
    async def damn(self, vc: wavelink.Player, index: int, tracks, ctx):
      idk:wavelink.abc.Playable = tracks[index]
      if vc.queue.is_empty and not vc.is_playing():
          await vc.play(idk)
          track = idk
          author = track.author or "None"
          emb = discord.Embed(description=f"\n[{track.title}](https://discord.gg/oxytech)", color=self.color).set_author(name="| Now Playing", icon_url=ctx.author.display_avatar.url)
         #   emb.timestamp= datetime.datetime.now() + datetime.timedelta(milliseconds=int(track.duration))
          emb.add_field(name="Duration", value=f"[{round(track.duration / 60, 2)}](https://discord.gg/oxytech)")
          emb.add_field(name="Requester", value=f"[{str(ctx.author)}](https://discord.com/users/{ctx.author.id})")
          emb.add_field(name="Artist", value=f"[{author}](https://discord.gg/oxytech)")
          emb.set_thumbnail(url=track.thumb or "None")
          v = interface(self.bot, ctx, False, False)
          await vc.smex.delete()
          await ctx.send(embed=emb, view=v) 
          return
      else:
          await vc.queue.put_wait(idk)
          embed = discord.Embed(
                    description=
                    f'[{idk.title}](https://discord.gg/Oxytech) Added To The Queue',
                    color=0x2f3136)

          embed.set_author(name="ADDED TO QUEUE",
                                 icon_url=ctx.author.display_avatar.url)
          embed.set_thumbnail(url=self.bot.user.display_avatar.url)
          await vc.smex.edit(embed=embed, view=None)
      vc.ctx = ctx
      setattr(vc, "loop", False)

                

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client
        try:
            req = track.requester
        except:
            req = player.guild.me
            
        try:
            thumb = track.thumb
        except:
            try:
                thumb = track.thumbnail
            except:
                thumb = None  
                          
        if player.loop:
            await player.play(track)
            author = track.author or "None"
            emb = discord.Embed(description=f"\n[{track.title}](https://discord.gg/oxytech)", color=self.color).set_author(name="| Now Playing", icon_url=req.display_avatar.url)
           # emb.timestamp= datetime.datetime.now() + datetime.timedelta(milliseconds=int(track.duration))
            emb.add_field(name="Duration", value=f"[{round(track.duration / 60, 2)}](https://discord.gg/oxytech)")
            emb.add_field(name="Requester", value=f"[{str(req)}](https://discord.com/users/{req.id})")
            emb.add_field(name="Artist", value=f"[{author}](https://discord.gg/oxytech)")
            emb.set_thumbnail(url=thumb)
            v = interface(self.bot, ctx, False, False)
            init = await ctx.send(embed=emb, view=v)
            return
        
        if not player.queue.is_empty:
            next_track = await vc.queue.get_wait()
            try:
                req1 = next_track.requester           
            except:
                req1 = player.guild.me
            try:
                thumb1 = next_track.thumb
            except:
                try:
                   thumb1 = next_track.thumbnail
                except:
                   thumb1 = None                  
            await vc.play(next_track)
            author1 = next_track.author or "None"
            emb = discord.Embed(description=f"\n[{next_track.title}](https://discord.gg/oxytech)", color=self.color).set_author(name="| Now Playing", icon_url=req1.display_avatar.url)
           # emb.timestamp= datetime.datetime.now() + datetime.timedelta(milliseconds=int(next_track.duration))
            emb.add_field(name="Duration", value=f"[{round(next_track.duration / 60, 2)}](https://discord.gg/oxytech)")
            emb.add_field(name="Requester", value=f"[{str(req1)}](https://discord.com/users/{req1.id})")
            emb.add_field(name="Artist", value=f"[{author1}](https://discord.gg/oxytech)")
            emb.set_thumbnail(url=thumb1)
            v = interface(self.bot, ctx, False, False)
            init = await ctx.send(embed=emb, view=v)
            return
        else:
            pass
 
            
            
    @commands.hybrid_command(name="current", aliases=['now'], description = "Gives you details of the current song")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def current(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(color=self.color)
            embed.set_author(name=f" | I am not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        
        else:
            vc: wavelink.Player = ctx.voice_client
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                    color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        
        embed = discord.Embed(
               color=self.color)
        embed.set_author(name=f" | No song is currently playing .",icon_url=ctx.author.display_avatar.url)  
        if not vc.is_playing():
            return await ctx.reply(embed=embed)
        now = vc.current
        x = datetime.datetime.now()
        try:
            requester = now.requester
        except:
            requester = vc.guild.me
        track = now
        try:
            title = track.stitle
        except:
            title = track.title
        try:
            thumb = track.sthumb
        except:
            thumb = None
        try:
            sauthor = track.sauthor
        except:
            sauthor = None
        try:
            u = track.suri
        except:
            u = "https://discord.gg/oxytech"
        if vc.queue.loop:
            loop = "Song"
        elif vc.queue.loop_all:
            loop = "Queue"
        else:
            loop = None
        total = now.length/1000
        currentt = vc.position/1000
        bar = '━'
        slider = '●'
        size = 14
        percent = currentt / total * size;
        progarr = []
        for i in range(size):
            progarr.append(bar)
        progarr[round(percent)] = slider
        x = "".join(progarr)
        total = str(datetime.timedelta(seconds=int(total)))
        try:
            total = total[:total.index(".")]
        except:
            total = total
        currentt = str(datetime.timedelta(seconds=int(currentt)))
        try:
            currentt = currentt[:currentt.index(".")]
        except:
            currentt = currentt
        x = f"[{currentt}] {x} [{total}]"
        if vc.is_paused:
            pp = "Paused"
        else:
            pp = "Resumed"
        embed = discord.Embed(description=f"[{now.title}]({u}) \nAuthor: {sauthor or now.author or 'None'}\nRequested By: {requester.mention}\n{x}", color=self.color)
        embed.set_author(name=f"Now Playing", icon_url=f"{self.bot.user.avatar.url}")
        embed.set_footer(text=f"Volume: {vc.volume}% | {pp} | Looping: {loop}", icon_url=f"{ctx.author.display_avatar.url}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="shuffle", description="Shuffles the current queue")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def shuffle(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(
                 color=self.color)
            embed.set_author(name=f" | I am not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                    color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        
        embed = discord.Embed(
              color=self.color)
        embed.set_author(name=f" | No song is currently playing .",icon_url=ctx.author.display_avatar.url)  
        if not vc.is_playing():
            return await ctx.reply(embed=embed)
        else:
            q = vc.queue
            if len(q) <= 1:
                return await ctx.reply(f"The length of queue must be more than 2 for shuffle .")
            else:        
                v = list(q.copy())
                random.shuffle(v)
                vc.queue.clear()
                for i in v:
                    await vc.queue.put_wait(i)
                return await ctx.reply(embed=discord.Embed(color=self.color).set_footer(text="| Shuffled the current queue .", icon_url=self.bot.user.avatar.url), delete_after=10)
            
            
            
    @commands.hybrid_command(name="replay", description="Replays the current song")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def replay(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(
               color=self.color)
            embed.set_author(name=f" | I am not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                    color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        
        embed = discord.Embed(
                color=self.color)
        embed.set_author(name=f" | No song is currently playing .",icon_url=ctx.author.display_avatar.url)  
        if not vc.is_playing():
            return await ctx.reply(embed=embed)
        else:
            await vc.seek(0)
            await ctx.reply(embed=discord.Embed(color=self.color).set_footer(text="| Replayed the current song .", icon_url=self.bot.user.avatar.url))
    
    @commands.hybrid_command(description = "Changes the loop setting")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def loop(self, ctx: commands.Context, option: str = None):
        if not ctx.voice_client:
            embed = discord.Embed(color=self.color)
            embed.set_author(name=f" | I am not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            
            return await ctx.reply(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                    color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        embed = discord.Embed(
               color=self.color)
        embed.set_author(name=f" | There must be a song or queue playing .",icon_url=ctx.author.display_avatar.url)  
        
        if not vc.is_playing():
            return await ctx.reply(embed=embed)
        opt = ['s', 'q', 'n', 'song', 'queue', 'none']
        if option is None:
            option = 'n'
        else:
            if option.lower() not in opt:
                return await ctx.reply("There are only 3 options for looping: None, Song or Queue .")
            option = option[0]
        if option == 'n':
            vc.queue.loop = False
            vc.queue.loop_all = False
            await ctx.reply(embed=discord.Embed(color=self.color).set_footer(text="| Now onwards nothing will be looped .", icon_url=ctx.author.display_avatar.url))
        if option == 's':
            vc.queue.loop = True
            vc.queue.loop_all = False
            self.vc.songl = self.vc.current
            await ctx.reply(embed=discord.Embed(color=self.color).set_footer(text="| The current song is set to loop .", icon_url=ctx.author.display_avatar.url))
        if option == 'q':
            vc.queue.loop = False
            vc.queue.loop_all = True
            await ctx.reply(embed=discord.Embed(color=self.color).set_footer(text="| The current queue will now be looped .", icon_url=self.bot.user.avatar.url))







    @commands.hybrid_command(name="moveto", aliases=['skipto'], description="Move the player to different position")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def moveto(self, ctx: commands.Context, index: str):
        if not ctx.voice_client:
            embed = discord.Embed(
               color=self.color)
            embed.set_author(name=f" | I am not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                  color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                 color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        xd = list(vc.queue.copy())
        if (
            (not index.isdigit()) or 
            (int(index)) < 1 or 
            (int(index) > len(xd))
        ):
            return await ctx.send(f"{ctx.author.mention} The index should be a number between 1 and {len(xd)} position!",delete_after=10)
        vc.queue.clear()
        for i in xd[int(index)-1:]:
            await vc.queue.put_wait(i)
        await vc.stop()
        emb2 = discord.Embed(color=self.color)
        emb2.set_footer(text=f"| Moved the player to song no. to {index} . ", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=emb2, mention_author=False, delete_after=10)




    @commands.hybrid_command(name="stop", description = "Stops the song")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def stop(self, ctx: commands.Context):
        
        if not ctx.voice_client:
            embed = discord.Embed(
                color=self.color)
            embed.set_author(name=f" | I am not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        
        if ctx.voice_client.is_playing():

            await ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            em = discord.Embed(color=self.color)
            em.set_footer(text="| Destroyed the queue and stopped the player .", icon_url=ctx.author.display_avatar.url)
            await ctx.reply(embed=em)
        else:
            em = discord.Embed(color=self.color)
            em.set_footer(text="| The player is already stopped .", icon_url=ctx.author.display_avatar.url)
            await ctx.reply(embed=em)


    @commands.hybrid_command(name="pause", description = "Pauses the song")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = discord.Embed(
                description=f"{ctx.author.mention} I am not connected to any of the voice channel.", color=self.color)
            return await ctx.reply(embed=embed)
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                    description=f"{ctx.author.mention} You are not connected to any of the voice channel.", color=self.color)
            else:
                embed = discord.Embed(
                    description=f"{ctx.author.mention} You are not connected to the same voice channel.", color=self.color)
            return await ctx.reply(embed=embed)
        embed = discord.Embed(
                description=f"{ctx.author.mention} There must be a song or queue playing.", color=self.color)
        if not ctx.voice_client.is_playing():
            return await ctx.reply(embed=embed)
        if ctx.voice_client.is_paused():
            embed.description = f"{ctx.author.mention} The song is already paused."
            return await ctx.reply(embed=embed)
        await ctx.voice_client.pause()
        em = discord.Embed(color=self.color)
        em.set_footer(text="| Paused the player", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="resume", aliases=["continue"], description = "Resumes the song")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = discord.Embed(
                color=self.color)
            embed.set_author(name=f" | I am not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
    
        embed = discord.Embed(
               color=self.color)
        embed.set_author(name=f" | There must be a song or queue playing .",icon_url=ctx.author.display_avatar.url) 
        if not ctx.voice_client.is_playing():
            return await ctx.reply(embed=embed)
        if not ctx.voice_client.is_paused():
            embed.set_author(name=f" | The song is not paused .",icon_url=ctx.author.display_avatar.url) 
            
            return await ctx.reply(embed=embed)
        
        await ctx.voice_client.resume()
        em = discord.Embed(color=self.color)
        em.set_footer(text="| Resumed the player .", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="skip", aliases=['next'], pass_context=True, description = "Plays the next song")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def skip(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = discord.Embed(
                color=self.color)
            embed.set_author(name=f" | I am not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        
        
        vc = ctx.voice_client
        embed = discord.Embed(
                color=self.color)
        embed.set_author(name=f" | There must be a song or queue playing .",icon_url=ctx.author.display_avatar.url)  
        if not ctx.voice_client.is_playing():
            return await ctx.reply(embed=embed)
        queue = vc.queue
        if len(queue) == 0 and vc.auto_queue.count ==0:
            await vc.stop()
            em = discord.Embed(title="Queue concluded", description=f"Enjoyed listening music with {self.bot.user.name} ? Consider inviting to your server .", color=self.color)
            em.set_footer(text="| No more songs left to play in queue .", icon_url=ctx.guild.me.display_avatar.url)
            return await ctx.reply(embed=em)
        else:
            await vc.stop()
            emb2 = discord.Embed(color=self.color)
            emb2.set_footer(text="| Skipped the song .", icon_url=ctx.author.display_avatar.url)
            await ctx.reply(embed=emb2, mention_author=False, delete_after=15)

    @commands.hybrid_command(name="disconnect", aliases=["dc"], description = "Disconnects from voice channel")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def disconnect(self, ctx: commands.Context):
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                    color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                    color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        if not ctx.voice_client:
            embed = discord.Embed(
              color=self.color)
            embed.set_author(name=f" | Already disconnected from the voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        
        await ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        em = discord.Embed(color=self.color)
        em.set_footer(text="| Destroyed the queue and left the voice channel .", icon_url=ctx.author.display_avatar.url)
        
        await ctx.reply(embed=em)
       

    @commands.hybrid_command(name="seek", description = "Changes the position of song")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def seek(self, ctx: commands.Context, time):
        if not ctx.voice_client:
            embed = discord.Embed(
                color=self.color)
            embed.set_author(name=f" | I am not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        embed = discord.Embed(
                description=f"{ctx.author.mention} There must be a song or queue playing.", color=self.color)
        if not ctx.voice_client.is_playing():
            return await ctx.reply(embed=embed)
        track = ctx.voice_client.current
        if (
            (not time.isdigit()) or 
            (int(time)) < 0 or 
            (int(time) > track.duration/1000)
        ):
            return await ctx.send(f"{ctx.author.mention} The time should be a number between 0 and {track.duration/1000} seconds!")
        time = int(time)
        await ctx.voice_client.seek(int(time)*1000)
        em = discord.Embed(color=self.color)
        em.set_footer(text=f"| Seeked the song to {time} seconds.!", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)
    
    @commands.hybrid_command(name = "volume", aliases=['v', 'vol'], description = "Change the bot's volume.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def volume(self, ctx: commands.Context, volume):
        if not ctx.voice_client:
            embed = discord.Embed(
                color=self.color)
            embed.set_author(name=f" | I am not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        c = False
        for i in ctx.guild.me.voice.channel.members:
            if i.id == ctx.author.id:
                c = True
                break
        if c:
            pass
        else:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
            else:
                embed = discord.Embed(
                   color=self.color)
                embed.set_author(name=f" | You are not connected to the same voice channel .",icon_url=ctx.author.display_avatar.url)  
            return await ctx.reply(embed=embed)
        if (
            (not volume.isdigit()) or 
            (int(volume)) < 0 or 
            (int(volume) > 400)
        ):
            return await ctx.send(f"{ctx.author.mention} The volume should be a number between 0 and 400 ")
        volume = int(volume)
        await ctx.voice_client.set_volume(volume)
        em = discord.Embed(color=self.color)
        em.set_footer(text=f"| Changed the volume to :{volume} .", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="connect",aliases=["join", "j"], description = "Joins a voice channel")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def join(self, ctx: commands.Context, channel: typing.Optional[discord.VoiceChannel]):
        
        if channel is None:
            if not getattr(ctx.author.voice, "channel", None):
                embed = discord.Embed(
                 color=self.color)
                embed.set_author(name=f" | You are not connected to any of the voice channel .",icon_url=ctx.author.display_avatar.url)  
                return await ctx.reply(embed=embed)
            else:
                channel = ctx.author.voice.channel
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        if player is not None:
            if player.is_connected():
                embed = discord.Embed(
                 color=self.color)
                embed.set_author(name=f" | I am already connected to a voice channel. .",icon_url=ctx.author.display_avatar.url)  
                return await ctx.reply(embed=embed)
        vc: wavelink.player = await channel.connect(cls=wavelink.Player, self_deaf=True)
        mbed=discord.Embed( color=self.color)
        
        mbed.set_footer(text=f" |  Successfully connected to {channel.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=mbed)
        
        


    @commands.hybrid_command(name="forcefix", description="Makes the bot leaves the vc forcefully")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @blacklist_check()
    @ignore_check()
    async def forcefix(self, ctx: commands.Context):
        try:
            await ctx.voice_client.disconnect()
            mbed=discord.Embed( color=self.color)
        
            mbed.set_footer(text=f" | Successfully Fixed the current player .", icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=mbed)
        except:
            mbed=discord.Embed( color=self.color)
        
            mbed.set_footer(text=f" | I am not connected to any of the voice channel .", icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=mbed)
            
##############
    @commands.group(name="bassboost",
                    invoke_without_command=True,
                    aliases=['bass'])
    @blacklist_check()
    @ignore_check()
    async def _bass(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_bass.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def boost_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   
          
        bands = [(0, 0.2), (1, 0.15), (2, 0.1), (3, 0.05), (4, 0.0),
                 (5, -0.05), (6, -0.1), (7, -0.1), (8, -0.1), (9, -0.1),
                 (10, -0.1), (11, -0.1), (12, -0.1), (13, -0.1), (14, -0.1)]
        await vc.set_filter(wavelink.Filter(
            equalizer=wavelink.Equalizer(name="MyOwnFilter", bands=bands)),
                            seek=True)
        hacker4 = discord.Embed(
            color=0x2f3136)
        hacker4.set_author(name=f" | Successfully enabled `bass boost` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)

    @_bass.command(name="disable", aliases=[("off")])
    
    @blacklist_check()
    @ignore_check()
    async def rmvboost_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        
        hacker4 = discord.Embed(
            color=0x2f3136)
        hacker4.set_author(name=f" | Successfully disabled `bass boost` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)  
        await ctx.reply(embed=hacker4)
        
        
    @commands.hybrid_group(name="filter",
                    invoke_without_command=True,
                    aliases=['filters'])
    @blacklist_check()
    @ignore_check()
    async def _filter(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_filter.group(name="lofi",
                    invoke_without_command=True,
                    aliases=['Lofi'])
    @blacklist_check()
    @ignore_check()
    async def _lofi(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_lofi.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def lofi_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed =  0.7500000238418579, pitch = 0.800000011920929, rate = 1)))
        hacker4 = discord.Embed(
            color=0x2f3136)
        hacker4.set_author(name=f" | Successfully enabled `lofi filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)


        
    @_lofi.command(name="disable", aliases=[("off")])
    
    @blacklist_check()
    @ignore_check()
    async def rmlofi_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x2f3136)
        hacker4.set_author(name=f" | Successfully disabled `lofi filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)
######################


    @_filter.group(name="nightcore",
                    invoke_without_command=True,
                    aliases=['Nightcore'])
    @blacklist_check()
    @ignore_check()
    async def _nightcore(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_nightcore.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def nighti_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed = 1.2999999523162842, pitch = 1.2999999523163953, rate = 1)))
      
        hacker4 = discord.Embed(
            color=self.color)
        hacker4.set_author(name=f" | Successfully enabled `nightcore filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)


        
    @_nightcore.command(name="disable", aliases=[("off")])
    
    @blacklist_check()
    @ignore_check()
    async def rmnightcore_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x2f3136)
        hacker4.set_author(name=f" | Successfully disabled `nightcore filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)
######################


    @_filter.group(name="8d",
                    invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    async def _8d(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_8d.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def d_commad(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, rotation=wavelink.Rotation(speed=0.29999))) 
      
        hacker4 = discord.Embed(
            color=self.color)
        hacker4.set_author(name=f" | Successfully enabled `8d filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)


        
    @_8d.command(name="disable", aliases=[("off")])
    
    @blacklist_check()
    @ignore_check()
    async def rm8d_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x2f3136)
        hacker4.set_author(name=f" | Successfully disabled `8d filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)
############################



    @_filter.group(name="damon",
                    invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    async def _damon(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_damon.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def damon_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed =  0.6899999521238, pitch = 0.7999990000011920929, rate = 1)))
      
        hacker4 = discord.Embed(
            color=self.color)
        hacker4.set_author(name=f" | Successfully enabled `damon filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)


        
    @_damon.command(name="disable", aliases=[("off")])
    
    @blacklist_check()
    @ignore_check()
    async def damoni_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x2f3136)
        hacker4.set_author(name=f" | Successfully disabled `damon filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)

######################


    @_filter.group(name="daycore",
                    invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    async def _daycore(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_daycore.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def _daycore_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed =  0.6899999521238, pitch = 0.7999990000011920929, rate = 1)))
      
        hacker4 = discord.Embed(
            color=self.color)
        hacker4.set_author(name=f" | Successfully enabled `daycore filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)


        
    @_daycore.command(name="disable", aliases=[("off")])
    
    @blacklist_check()
    @ignore_check()
    async def daycore_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x2f3136)
        hacker4.set_author(name=f" | Successfully disabled `daycore filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)
#######################


    @_filter.group(name="121",
                    invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    async def _121(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_121.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def hacker_121(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        bands = [(0, 0.2), (1, 0.15), (2, 0.1), (3, 0.05), (4, 0.0),
                 (5, -0.05), (6, -0.1), (7, -0.1), (8, -0.1), (9, -0.1),
                 (10, -0.1), (11, -0.1), (12, -0.1), (13, -0.1), (14, -0.1)]
        await vc.set_filter(wavelink.Filter(
            equalizer=wavelink.Equalizer(name="MyOwnFilter", bands=bands)),
                            seek=True)
        await vc.set_volume(500)
      
        hacker4 = discord.Embed(
            color=self.color)
        hacker4.set_author(name=f" | Successfully enabled `121 filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)


        
    @_121.command(name="disable", aliases=[("off")])
    
    @blacklist_check()
    @ignore_check()
    async def rm121_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed = 0.8)))
        hacker4 = discord.Embed(
            color=0x2f3136)
        hacker4.set_author(name=f" | Successfully disabled `121 filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)
        
######################



    @_filter.group(name="slowmode",
                    invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    async def _slowmode(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_slowmode.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def lslowmode_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, equalizer=wavelink.Equalizer(name = 'CustomEqualizer', bands=[(0, 1), (1, 1),(2, 1),(3, 1),(4, 1),(4, 1),(5, 1),(6, 1),(7, 1),(8, 1),(9, 1),(10, 1),(11, 1),(12, 1),(13, 1),(14, 1),(15, 1)])))
        await vc.set_volume(100)
      
        hacker4 = discord.Embed(
            color=self.color)
        hacker4.set_author(name=f" | Successfully enabled `slowmode filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)


        
    @_slowmode.command(name="disable", aliases=[("off")])
    
    @blacklist_check()
    @ignore_check()
    async def rmslowmode_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x2f3136)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x2f3136)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x2f3136)
        hacker4.set_author(name=f" | Successfully disabled `slowmode filter` .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)
        
        
        
        
##################







 
 
 
 
  