import discord
import os 
#os.system("pip install git+https://github.com/openai/openai-python")
from discord.ext import commands
import aiohttp
import json 
import openai
from utils.Tools import *
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY



def updateai(guildID, data):
    with open("ai.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("ai.json", "w") as config:
        config.write(newdata)
################

def getai(guildID):
    with open("ai.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "channels": [],
            "whitelist": [],
            "whitelisted": [],
            "chatbot": None,
            "aich": None
            
        }
        updateai(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]







class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [246469891761111051]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command .", ephemeral=True)
            return False
        return True
    
    
    
    
class chatbot(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None
        
    @discord.ui.button(label="Yes", custom_id='Yes', style=discord.ButtonStyle.green)
    async def png(self, interaction, button):
        self.value = 'yes'
        self.stop()

    @discord.ui.button(label="No", custom_id='stop', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction, button):
        self.value = 'stop'
        self.stop()
        
        
        
        
class Ai(commands.Cog):

  def __init__(self, bot, *args, **kwargs):
    self.bot = bot
    self.color = 0x2f3136



                    
  @commands.cooldown(1, 20, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  @commands.hybrid_command(name="chatgpt", aliases=['cgpt', 'gpt'], description="Give you results for your query from openai")
  async def gpt(self,ctx: commands.Context, *, prompt):
    hacker = prompt.count(' ') + 100
    mbed = discord.Embed(description="Please wait while I process your request .",color=self.color)
    ok = await ctx.send(embed=mbed)
    async with aiohttp.ClientSession() as session:
        payload ={
            "model": "text-davinci-003",
            "prompt": prompt,
            "temperature": 0.8,
            "max_tokens": 4097-hacker,
            "presence_penalty":0,
            "frequency_penalty":0,
            "best_of":1            
        }
        headers={"Authorization": "Bearer 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"}
        async with session.post("https://api.openai.com/v1/completions",json=payload,headers=headers) as resp:
            response = await resp.json()
            respo = response["choices"][0]["text"]
            hacker5 = discord.Embed(
                                description=
                                f"```py\n{respo}\n```",
                                color=0x2f3136)
            hacker5.set_author(
                                name=f"{self.bot.user.name} Chat Gpt`s Response:",
                                icon_url=ctx.author.avatar.url
                                if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker5.timestamp = discord.utils.utcnow()
            hacker5.set_footer(
                                    text=f"Requested By {ctx.author}",
                                    icon_url=ctx.author.avatar.url
                                if ctx.author.avatar else ctx.author.default_avatar.url)
            await ok.edit(embed=hacker5)
            return 
        
  
  
  
  @commands.hybrid_group(name="chatbot",invoke_without_command = True,aliases=['cbot','chatbots'])
  @blacklist_check()
  @ignore_check()
  async def chatbot(self, ctx):       
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)   
        
  @commands.cooldown(1, 20, commands.BucketType.user)
  @commands.has_permissions(administrator = True)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  @chatbot.command(name="setup", help="Setup ai chatbot for your server .")
  async def setup(self, ctx: commands.Context, *, channel: discord.TextChannel):
      data = getai(ctx.guild.id)
      ch= data["chatbot"]
      ai = data["aich"]
      
      if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
          if ch is not None:
              embed = discord.Embed(
                     color=self.color,
                    description=f" | chatbot is already setuped for {ctx.guild.name} . do you want to change it to {channel.mention} ?")
              return await ctx.reply(embed=embed)
          else:
              view = chatbot(ctx)
              em = discord.Embed(description=F"Are you sure you want to setup chatbot in {channel.mention} for {ctx.guild.name} ?", color=self.color)
              msg = await ctx.reply(embed=em, view=view)
              
              await view.wait()
              if view.value == 'stop':
                  return await msg.delete()
              
              await msg.edit(embed=discord.Embed(description="Please wait...", color=self.color), view=None)
              
            #  web = await channel.create_webhook(name=f"{str(self.bot.user.name)} | ChatBot")
              
              data = getai(ctx.guild.id)
             # data["chatbot"] = web.url
              data["aich"] = channel.id
              updateai(ctx.guild.id, data)
              
              hacker = discord.Embed(
                        description=
                        f"<:GreenTick:1029990379623292938> | Successfully setuped ai chatbot in {channel.mention} for {ctx.guild.name}.",
                        color=self.color)
              await msg.edit(embed=hacker,view=None)
      else:
          hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
          hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

          await ctx.send(embed=hacker5)   
          
      
  @chatbot.command(name="reset")
  @commands.has_permissions(administrator = True)
  @commands.cooldown(1, 20, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  async def reset(self, ctx):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:   
            data = getai(ctx.guild.id)
            data["chatbot"] = None
            data["aich"] = None
            updateai(ctx.guild.id, data)
            hacker = discord.Embed(
                        description=
                        f"<:GreenTick:1029990379623292938> | Successfully reseted ai chatbot for {ctx.guild.name} .",
                        color=self.color)
            await ctx.send(embed=hacker,view=None)
        else:
          hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=self.color)
          hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

          await ctx.send(embed=hacker5)   
      
      
      
  
      

      
  @commands.cooldown(1, 20, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @blacklist_check()
  @ignore_check()
  @commands.hybrid_command(name="imagine",description="Give you images for your query from openai")
  async def image(self,ctx: commands.Context, *, prompt):
    mbed = discord.Embed(description="Please wait while I process your request .",color=self.color)
    ok = await ctx.send(embed=mbed)
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=f"512x512"
    )
    image_url = response["data"][0]["url"]
    hacker5 = discord.Embed(color=0x2f3136)
    hacker5.set_author(
                                name=f"{prompt} from {ctx.author}",
                                icon_url=ctx.author.avatar.url
                                if ctx.author.avatar else ctx.author.default_avatar.url)
    hacker5.timestamp = discord.utils.utcnow()
    hacker5.set_footer(
                                    text=f"Requested By {ctx.author}",
                                    icon_url=ctx.author.avatar.url
                                if ctx.author.avatar else ctx.author.default_avatar.url)
    hacker5.set_image(url=image_url)
    await ok.edit(embed=hacker5)
    return 


  #@commands.Cog.listener()
  async def on_message(self, message: discord.message):
        await self.bot.wait_until_ready()
        if message.guild is None:
            return
        if not message.guild.me.guild_permissions.read_messages:
            return
        if not message.guild.me.guild_permissions.read_message_history:
            return
        if not message.guild.me.guild_permissions.view_channel:
            return
        if not message.guild.me.guild_permissions.send_messages:
            return
        if message.author.bot:
            return
        else:
            data = getai(message.guild.id)
            ch = data["aich"] 
            if ch is None:
                return 
            else:
                if message.channel.id == ch:
                    prompt = message.content
                    hacker = prompt.count(' ') + 100
                    response = openai.Completion.create(
                  engine="text-davinci-003",
                   prompt=message.content,
                    max_tokens=4097-hacker,
                    temperature=0.8,
                     n=1,
                  stop=None,
                   timeout=20,
    )
                    try:
                        await message.channel.send(response.choices[0].text.strip())
                        return 
                    except:
                        pass
                        
                    
                return 