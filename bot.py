# bot.py
# developed by Coltergeizt, 1/20/2020
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# utility functions -------------------------------
def load_env_vars():
    # easily expandable list of environment variables
    var_dict = {}
    load_dotenv()

    var_dict['token'] = os.getenv('DISCORD_TOKEN')
    var_dict['guild'] = os.getenv('DISCORD_GUILD')
    var_dict['prefix'] = os.getenv('PREFIX')

    return var_dict
# end utility functions ----------------------------


env_vars = load_env_vars()
bot = commands.Bot(command_prefix=env_vars['prefix'])
#client = discord.Client()
url = 'mongodb://localhost:27017'
ghoztDb = 'GhoztDB'


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')
    #guild = discord.utils.get(client.guilds, name=env_vars['guild'])
    guilds = bot.guilds
    print(f'all guilds: {guilds}')
    for x in range(0, len(guilds)):
        print(f'guild name: {guilds[x].name}')
        print(f'guild id: {guilds[x].id}')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {member.guild}!'
    )


@bot.event
async def on_message(message):
    print(f'bot user: {bot.user}')
    print(f'message author: {message.author}')
    if message.author == bot.user:
        return

    if message.content.startswith(env_vars['prefix']):
        print(f'Ghozt command found in message')
    else:
        return

    #command_length = 1
    #args = message.content[len(env_vars['prefix']):].strip().split()
    #if len(args) > 2:

    coltergeizt_quotes = [
        "There are people that can afford living and there are people who can't. - 2019",
        "I'm just sitting here all alone with my Sprite and peanut butter. - 2019",
        "There's no she, there's just me. - 2019",
        "Ooooh, she's a big gurl. - 2019",
        "Yeah those lions going to the gym too much, tryin' to get those jazelles. - 2019"
    ]

    if message.content == '!#geizt quote':
        response = random.choice(coltergeizt_quotes)
        await message.channel.send(response)


if __name__ == "__main__":
    bot.run(env_vars['token'])
