import discord
from discord.ext import commands
import random
import json
from discord.ext import commands, tasks
from discord import Webhook

class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [246469891761111051]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command .", ephemeral=True)
            return False
        return True
    
    
    
    
class PngOrGif(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None
        
    @discord.ui.button(label="PNG", custom_id='png', style=discord.ButtonStyle.green)
    async def png(self, interaction, button):
        self.value = 'png'
        self.stop()

    @discord.ui.button(label="GIF", custom_id='gif', style=discord.ButtonStyle.green)
    async def gif(self, interaction, button):
        self.value = 'gif'
        self.stop()

    @discord.ui.button(label="MIX", custom_id='mix', style=discord.ButtonStyle.green)
    async def mix(self, interaction, button):
        self.value = 'mix'
        self.stop()

    @discord.ui.button(label="STOP", custom_id='stop', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction, button):
        self.value = 'stop'
        self.stop()


async def autopfp(self, web, type):
    if len(self.bot.users) < 1000:
        u = random.sample(self.bot.users, len(self.bot.users))
    else:
        u = random.sample(self.bot.users, 1000)
    c = 1
    ch = discord.SyncWebhook.from_url(web)
    for i in u:
        if i.avatar and c <= 10:
          if type != 'mix':
            if type in i.avatar.url:
                try:
                    return ch.send(i.avatar.url)
                except:
                    return
                c += 1
          else:
                try:
                    return ch.send(i.avatar.url)
                except:
                    return
                c += 1
                
                
                
class AutoPfp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2f3136
        self.autopfp_task.start()
                                 
    @tasks.loop(minutes=5)
    async def autopfp_task(self):
        await self.bot.wait_until_ready()
        with open('pfp.json', 'r') as f:
            data = json.load(f) 
        for guild in self.bot.guilds:
            if guild.id in data:               
                await autopfp(self, data[guild.id]['link'], data[guild.id]['type'])
            return
                
                     
        
    @commands.group(
        invoke_without_command=True, description="Shows The help menu for pfp"
    )
    async def pfp(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=246469891761111051)
        hacker = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=self.color,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}pfp`\n" 
                                                  f"Shows The help menu for pfp\n\n" 
                                                  f"`{prefix}pfp auto enable <channel>`\n" 
                                                  f"Sends pfp automatically in every 5 minutes\n\n"
                                                  f"`{prefix}pfp auto disable`\n"
                                                  f"Stops sending pfp\n\n"
                                                  f"`{prefix}pfp random <number>`\n" 
                                                  f"Sends random pfps\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by {hacker}" ,  icon_url=pfp)
        await ctx.send(embed=listem)
        
        







    @pfp.group(invoke_without_command=True, description="Shows The help menu for pfp auto")
    async def auto(self, ctx):
        prefix = ctx.prefix
        xd = discord.utils.get(self.bot.users, id=246469891761111051)
        hacker = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0x7aaaff,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}pfp auto`\n" 
                                                  f"Shows The help menu for pfp auto\n\n" 
                                                  f"`{prefix}pfp auto enable <channel>`\n" 
                                                  f"Sends pfp automatically every 2 mins\n\n"
                                                  f"`{prefix}pfp auto disable`\n"
                                                  f"Stops sending pfp\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by {hacker}" ,  icon_url=pfp)
        await ctx.send(embed=listem)
        
       
    @auto.command()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx: commands.Context, *, channel: discord.TextChannel):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
             with open('pfp.json', 'r') as f:
                 data = json.load(f)  
             if str(ctx.guild.id) in data:
                 embed = discord.Embed(
                     color=self.color,
                    description=f" | Auto pfp is already enabled in {ctx.guild.get_channel(data[str(ctx.guild.id)]['channel']).mention} for {ctx.guild.name} .")
                 return await ctx.reply(embed=embed)
             else:
                 view = PngOrGif(ctx)
                 em = discord.Embed(description="Which type of pfp you want?\n", color=self.color)
                 msg = await ctx.reply(embed=em, view=view)
                 await view.wait()
                 if view.value == 'stop':
                     return await msg.delete()
                 web = await channel.create_webhook(name=f"{str(self.bot.user.name)} | Autopfp")
                 await msg.edit(embed=discord.Embed(description="Please wait...", color=self.color), view=None)
                 data[str(ctx.guild.id)] = {
                          'link': web.url,
                          'type': view.value,
                          'channel': channel.id
                           } 
                 with open("pfp.json", "w") as f: 
                     json.dump(data, f, indent=4) 
                 hacker = discord.Embed(
                        description=
                        f"From Now 5-10 profile pictures will be send in every 5 minutes in {channel.mention} .",
                        color=self.color)
                 await msg.edit(embed=hacker,view=None)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)
            
            

                 
                 
                 
                              
    @auto.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx: commands.Context): 
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
             with open('pfp.json', 'r') as f:
                 data = json.load(f)  
             if str(ctx.guild.id) not in data:
                 embed = discord.Embed(
                     color=self.color,
                    description=f" | Auto pfp is not setupped in {ctx.guild.name} .")
                 return await ctx.reply(embed=embed)
             else:
                 msg = data[str(ctx.guild.id)]["link"]
                 discord.SyncWebhook.from_url(msg).delete()
                 del data[str(ctx.guild.id)]
                 with open("pfp.json", "w") as f:
                     json.dump(data, f, indent=4)
                      
                 hacker = discord.Embed(
                        description=
                        f"<:GreenTick:1018174649198202990> | Successfully disabled auto pfp in {ctx.guild.name} .",
                        color=self.color)
                 await ctx.send(embed=hacker)   
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)
            
            
            
    @pfp.command()
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def random(self, ctx: commands.Context, *, number):
        if number.isdigit():
            number = int(number)
        else:
            return await ctx.reply("Please provide a valid number .")
        if abs(number) > 20:
            return await ctx.reply("The limit is only for 20 profile pictures .")
        view = PngOrGif(ctx)
        em = discord.Embed(description="Which type of pfp you want?\n", color=self.color)
        init = await ctx.reply(embed=em, view=view)
        await view.wait()
        if view.value == 'stop':
            return await init.delete()
        if view.value == 'mix':
            await init.delete()
            u = random.sample(self.bot.users, 10000)
            c = 1
            for i in u:
                if i.avatar and c <= abs(number):
                        await ctx.send(i.avatar.url)
                        c += 1
        if view.value == 'png':
            await init.delete()
            u = random.sample(self.bot.users, 10000)
            c = 1
            for i in u:
                if i.avatar and c <= abs(number):
                    if 'png' in i.avatar.url:
                        await ctx.send(i.avatar.url)
                        c += 1
        if view.value == 'gif':
            await init.delete()
            u = random.sample(self.bot.users, 10000)
            c = 1
            for i in u:
                if i.avatar and c <= abs(number):
                    if 'gif' in i.avatar.url:
                        await ctx.send(i.avatar.url)
                        c += 1
                        
            