import os
os.system("pip install tasksio && pip install httpx && pip install psutil && pip install requests && pip install git+https://github.com/ItzYourHacker/Wavelink")
os.system("pip install git+https://github.com/ItzYourHacker/jishaku")
os.system("pip install git+https://github.com/Rapptz/discord-ext-menus")
#os.system("pip install git+https://github.com/Rapptz/discord.py")
from core.Astroz import Astroz
import asyncio
import jishaku, cogs
from discord.ext import commands
import discord
from discord import app_commands
import traceback
from discord.ext.commands import Context
import time
from utils.Tools import *
from discord import Webhook

os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

client = Astroz()
tree = client.tree



class Hacker(discord.ui.Modal, title='Embed Configuration'):
    tit = discord.ui.TextInput(
        label='Embed Title',
        placeholder='Embed title here',
    )

    description = discord.ui.TextInput(
        label='Embed Description',
        style=discord.TextStyle.long,
        placeholder='Embed description optional',
        required=False,
        max_length=400,
    )

    thumbnail = discord.ui.TextInput(
        label='Embed Thumbnail',
        placeholder='Embed thumbnail here optional',
        required=False,
    )

    img = discord.ui.TextInput(
        label='Embed Image',
        placeholder='Embed image here optional',
        required=False,
    )

    footer = discord.ui.TextInput(
        label='Embed footer',
        placeholder='Embed footer here optional',
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.tit.value,
                              description=self.description.value,
                              color=0x2f3136)
        if not self.thumbnail.value is None:
            embed.set_thumbnail(url=self.thumbnail.value)
        if not self.img.value is None:
            embed.set_image(url=self.img.value)
        if not self.footer.value is None:
            embed.set_footer(text=self.footer.value)
        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction,
                       error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.',
                                                ephemeral=True)

        traceback.print_tb(error.__traceback__)


@tree.command(name="embedcreate", description=f"Create A Embed")
async def _embed(interaction: discord.Interaction) -> None:
    await interaction.response.send_modal(Hacker())

@client.event
async def on_command_completion(context: Context) -> None:

    full_command_name = context.command.qualified_name
    split = full_command_name.split("\n")
    executed_command = str(split[0])
    hacker = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/1118743634221740052/kQyvWt1u1-BgWKpbYGtq2B5Q35If8RReFBUCxjDROIZCJGtFpbpQAwD-5FUMi7e8DygY")
    if not context.message.content.startswith("."):
        pcmd = f"`.{context.message.content}`"
    else:
        pcmd = f"`{context.message.content}`"
    if context.guild is not None:
        try:
            
            embed = discord.Embed(color=0x2f3136)
            embed.set_author(
                name=
                f"Executed {executed_command} Command By : {context.author}",
                icon_url=f"{context.author.avatar}")
            embed.set_thumbnail(url=f"{context.author.avatar}")
            embed.add_field(
                name="Command Name :",
                value=f"{executed_command}",
                inline=False)
            embed.add_field(
                name="Command Content :",
                value="{}".format(pcmd),
                inline=False)
            embed.add_field(
                name="Command Executed By :",
                value=
                f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name="Command Executed In :",
                value=
                f"{context.guild.name}  | ID: [{context.guild.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name=
                "Command Executed In Channel :",
                value=
                f"{context.channel.name}  | ID: [{context.channel.id}](https://discord.com/channel/{context.channel.id})",
                inline=False)
            embed.set_footer(text=f"Thank you for choosing  {client.user.name}",
                             icon_url=client.user.display_avatar.url)
            hacker.send(embed=embed)
        except:
            print('lund le lo')
    else:
        try:

            embed1 = discord.Embed(color=0x2f3136)
            embed1.set_author(
                name=
                f"Executed {executed_command} Command By : {context.author}",
                icon_url=f"{context.author.avatar}")
            embed1.set_thumbnail(url=f"{context.author.avatar}")
            embed1.add_field(
                name="Command Name :",
                value=f"{executed_command}",
                inline=False)
            embed1.add_field(
                name="Command Executed By :",
                value=
                f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed1.set_footer(text=f"Thank you for choosing  {client.user.name}",
                              icon_url=client.user.display_avatar.url)
            hacker.send(embed=embed1)
        except:
            print("lund le lo")    


@client.event
async def on_ready():     
    print("Loaded & Online!")
    print(f"Logged in as: {client.user}")
    print(f"Connected to: {len(client.guilds)} guilds")
    print(f"Connected to: {len(client.users)} users")
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print (e)

async def main():
    async with client:
        os.system("clear")
        await client.load_extension("cogs")
        await client.load_extension("jishaku")
        tkn = "OTA2MDg1NTc4OTA5NTQ4NTU0.GY8nds.JJ-k2ckUpGokqxdvbwlgJwmklthFvzqLR0qcwI"
        await client.start(tkn)

if __name__ == "__main__":
    asyncio.run(main())
