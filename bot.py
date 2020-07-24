# bot.py
# developed by Coltergeizt, 1/20/2020
import os
import random
import discord
from dotenv import load_dotenv


# utility functions -------------------------------
def load_env_vars():
    # easily expandable list of environment variables
    var_dict = {}
    load_dotenv()

    var_dict['token'] = os.getenv('DISCORD_TOKEN')
    var_dict['guild'] = os.getenv('DISCORD_GUILD')

    return var_dict
# end utility functions ----------------------------


client = discord.Client()
env_vars = load_env_vars()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=env_vars['guild'])

    print(f'{client.user} has connected to Discord')
    print(f'{guild.name}(id: {guild.id})')


@client.event
async def on_member_join(member):
    guild = discord.utils.get(client.guilds, name=env_vars['guild'])
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {guild.name}!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    coltergeizt_quotes = [
        "There are people that can afford living and there are people who can't. - 2019",
        "I'm just sitting here all alone with my Sprite and peanut butter. - 2019",
        "There's no she, there's just me. - 2019",
        "Ooooh, she's a big gurl. - 2019",
        "Yeah those lions going to the gym too much, tryin' to get those jazelles. - 2019"
    ]

    if message.content == '!geizt quote':
        response = random.choice(coltergeizt_quotes)
        await message.channel.send(response)


if __name__ == "__main__":
    client.run(env_vars['token'])
