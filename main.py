import discord
from discord.ext import commands
import os
from webserver import keep_alive, update_last_ping_time
import requests
import threading

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
    allowed_roles = ['discord-team','organisers-2025', 'core']
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



    # Create private text channel and then assign the category using the "parent" parameter
    text_channel = await guild.create_text_channel(role_name, overwrites=overwrites)

    await ctx.send(f"✅ Created private text channel: #{text_channel.name}")

    # Create private voice channel and then assign the category using the "parent" parameter
    voice_channel = await guild.create_voice_channel(role_name, overwrites=overwrites)
    
    await ctx.send(f"✅ Created private voice channel: {voice_channel.name}")


    if not any(role.name.lower() in allowed_roles for role in ctx.author.roles):
        user_team_creation[ctx.author.id] = role_name

    await ctx.send("🎉 Welcome to Byteverse-2025!")

# Keep the webserver alive
keep_alive()

# Prevent Render instance from stopping
url = os.getenv('URL')  # Get URL from environment variable
interval = int(os.getenv('TIME', '30000'))  # default to 30000 ms if TIME isn't set
  # Interval in milliseconds (30 seconds)

def reload_website():
    while True:
        try:
            response = requests.get(url)
            print(f"Reloaded at {response.status_code}: {response.reason}")
            update_last_ping_time()
        except Exception as e:
            print(f"Error reloading: {str(e)}")
        threading.Event().wait(interval / 1000)

threading.Thread(target=reload_website, daemon=True).start()

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
