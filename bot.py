# bot.py
# developed by Coltergeizt, 1/20/2020
from os import listdir, getenv
from os.path import isfile, join
import traceback
import random
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

    var_dict['token'] = getenv('DISCORD_TOKEN')
    var_dict['guild'] = getenv('DISCORD_GUILD')
    var_dict['prefix'] = getenv('PREFIX')

    return var_dict
# end utility functions ----------------------------


env_vars = load_env_vars()
cogs_dir = "cogs"
bot = commands.Bot(command_prefix=env_vars['prefix'], case_insensitive=True)
url = 'mongodb://localhost:27017'
ghoztDb = 'GhoztDB'


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')
    '''guild = discord.utils.get(client.guilds, name=env_vars['guild'])'''
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


if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except Exception as ex:
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

    bot.run(env_vars['token'])
