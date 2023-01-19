import os
import openai
from dotenv import load_dotenv
import discord
from discord import app_commands



openai.api_key = os.getenv("OPENAI_API_KEY")
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)



# every message on the server (in channels it can see) passes through here.
@client.event
async def on_message(message: discord.Message):
    # ignore messages from itself
    if message.author == client.user:
        return
    
    if message.author.bot:
        return

    if isinstance(message.channel, discord.channel.DMChannel):
        return
    
    if message.channel.type == discord.ChannelType.public_thread:
        return
    
    if message.channel.type == discord.ChannelType.forum:
        return
    
    if message.content == '.pawsync':
        await tree.sync()
        await message.channel.send("Syncing!", reference=message)


# Responds to a users wish
@tree.command(
    name = 'wish',
    description = 'Tell your wish to the Monkey Paw...'
)
async def make_wish(context, prompt: str):
    if isinstance(context.channel, discord.channel.DMChannel):
        await context.response.send_message("I do not reply to DMs.")
        return
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="You are a monkey paw, you grant wishes from people but with an unfortunate twist. When presented with a wish, you grant it in a way that is probably not the way the user hoped.\n\nMy wish is... " + prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.28,
        presence_penalty=0
    )
    await context.response.send_message("Your wish: " + prompt + "\n\n" + response.choices[0].text)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing, 
            name="with your /wish"
        )
    )
    

client.run(TOKEN)