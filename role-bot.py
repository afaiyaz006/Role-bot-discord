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
role_wise_tokens={
    
}

guild_ids=[
    config['MY_SERVER'],
]
set_role_name=config['SET_ROLE']


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=guild_ids)
async def hello(ctx,message:str):
    
    await ctx.respond(f"Hello! You just messaged me this {message}")

def is_authorized(author:discord.Member,author_role:discord.Role):
    is_valid=author_role in author.roles
    return is_valid

@bot.slash_command(guild_ids=guild_ids)
@bot.command()
async def add_role_to(ctx,member: discord.Member,token:str, role: discord.Role):
    try:
        author_role = discord.utils.get(ctx.guild.roles, name=set_role_name)
        role_id = str(role.id)
        author = ctx.author
        role_exist = role_id in role_wise_tokens

        if role_exist and is_authorized(author,author_role):
            if token==role_wise_tokens[role_id]:
                await member.add_roles(role)
                await ctx.respond(f"{role.mention} has been assigned to you {member.mention}! :D")
            else:
                await ctx.respond(f"Invalid token :(")
        else:
            if not role_exist:
                await ctx.respond(f"Sorry role does not exists  :(")
            if not is_authorized:
                await ctx.respond(f"Sorry you are not authorized to perform this action {author.mention}")
    except Exception as e:
        await ctx.respond(f'Failed to add role: {e}')

@bot.slash_command(guild_ids=guild_ids)
@bot.command()
async def add_role(ctx,token:str, role: discord.Role):
   
    try:
        author = ctx.author
        role_id = str(role.id)
        role_exist = role_id in role_wise_tokens
        if role_exist:
            if token==role_wise_tokens[role_id]:
                await author.add_roles(role)
                await ctx.respond(f"{role.mention} has been assigned to you {author.mention}! :D")
            else:
                await ctx.respond(f"Invalid token for {role.mention} :(")
        else:
            await ctx.respond(f"token for this {role.mention} does not exist")
    except Exception as e:
        await ctx.respond(f"Could not add role {e}")
        
@bot.slash_command(guild_ids=guild_ids)
@bot.command()
async def set_token(ctx,token:str,role:discord.Role):
    try:
        author_role = discord.utils.get(ctx.guild.roles, name=set_role_name)
        author = ctx.author
        if is_authorized(author,author_role):
            role_id=str(role.id)
            if role_id not in role_wise_tokens:
                role_wise_tokens[role_id]=token
            else:
                role_wise_tokens[role_id]=token
            await ctx.respond(f"Token set for {role.mention}.\n**Token is**: ```{token}\n```")
        else:
            await ctx.respond(f"Sorry you are not authorized {author.mention}")
    except Exception as e:
        await ctx.respond(f"Unable to set your tokens :( {e}")
            
        

bot.run(config['TOKEN'])
