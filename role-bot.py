"""

Requirements:
- add option to provide roles for user if their provided token matched.
- specific role can set password
"""


import discord
from dotenv import dotenv_values
from discord.ext import commands

bot = discord.Bot()
config = dotenv_values(".env")
password = "test123"


guild_ids=[
    config['MY_SERVER'],
]

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=guild_ids)
async def hello(ctx,message:str):
    
    await ctx.respond(f"Hello! You just messaged me this {message}")


@bot.slash_command(guild_ids=guild_ids)
@bot.command()
@commands.has_permissions(administrator=True)
async def add_role(ctx,member: discord.Member,token:str, role: discord.Role):
    try:
        if str(token)==password:
            await member.add_roles(role)
            await ctx.respond(f"{role.mention} has been assigned to you {member.mention}!")
            await ctx.send(f"{role.mention} has been assigned to you {member.mention}! :D")
        else:
            await ctx.respond(f"Invalid token for role {role.mention} by {member.mention} :(")
    except Exception as e:
        await ctx.send(f'Failed to add role: {e}')

@bot.slash_command(guild_ids=guild_ids)
@bot.command()
@commands.has_permissions(adminstrator=True)
async def create_token_for_role(ctx,your_role:discord.Role,token:str,role:discord.Role):
    source_role = 

bot.run(config['TOKEN'])
