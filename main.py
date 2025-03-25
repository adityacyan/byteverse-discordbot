import discord
from discord.ext import commands
import os
from webserver import keep_alive

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to track users who have used the command
user_team_creation = {}

@bot.event
async def on_ready():
    print(f'{bot.user} is online and ready!')

@bot.command()
async def createteam(ctx, role_name: str, *members: discord.Member):
    allowed_roles = ['organiser-2025', 'core-2025']
    if any(role.name.lower() in allowed_roles for role in ctx.author.roles):
        pass
    else:
        if ctx.author.id in user_team_creation:
            await ctx.send("❌ You have already created a team. You can't create another one.")
            return

    if len(members) > 4:
        await ctx.send("❌ You can only add up to 4 members.")
        return

    guild = ctx.guild
    role = await guild.create_role(name=role_name, color=discord.Color.from_str('#00a1e7'), reason="Creating a team")
    await ctx.send(f"✅ Role `{role_name}` created with a custom blue color (#00a1e7).")

    for member in members:
        await member.add_roles(role)
    await ctx.send(f"✅ Assigned `{role_name}` to {', '.join([member.name for member in members])}")

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        role: discord.PermissionOverwrite(view_channel=True)
    }
    channel = await guild.create_text_channel(role_name, overwrites=overwrites)
    await ctx.send(f"✅ Created private channel: #{channel.name}")

    if not any(role.name.lower() in allowed_roles for role in ctx.author.roles):
        user_team_creation[ctx.author.id] = role_name

# Keep the webserver alive
keep_alive()

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
