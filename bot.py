# bot.py
# developed by Colt Campbell 10/21/2024
import traceback
import asyncio
import discord

from os import listdir, getenv
from os.path import isfile, join
from discord.ext import commands
from dotenv import load_dotenv
from common.constants import (
    PREFIX,
    COGS_DIR,
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class GhoztBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        var_dict = {}
        load_dotenv()
        var_dict["token"] = getenv("DISCORD_TOKEN")
        var_dict["bot_owner_id"] = getenv("BOT_OWNER_ID")
        self.env_vars = var_dict

    async def setup_hook(self) -> None:
        for extension in [
            f.replace(".py", "")
            for f in listdir(COGS_DIR)
            if (isfile(join(COGS_DIR, f)) and f.endswith(".py"))
        ]:
            try:
                print(extension)
                await self.load_extension(COGS_DIR + "." + extension)
            except Exception as ex:
                print(f"Failed to load extension {extension}.")
                traceback.print_exc()
        await self.tree.sync()
        print(f"Synced Slash commands for {self.user}.")

    async def on_ready(self) -> None:
        print(f"{self.user.name} has connected to Discord")
        guilds = self.guilds
        for x in range(0, len(guilds)):
            print(f"guild name: {guilds[x].name}")
            print(f"guild id: {guilds[x].id}")

    async def on_member_join(self, member) -> None:
        await member.create_dm()
        await member.dm_channel.send(f"Hi {member.name}, welcome to {member.guild}!")

    async def on_command_error(self, ctx, error) -> None:
        if ctx.interaction:
            await ctx.reply(error, ephemeral=True)

    async def main(self) -> None:
        async with self:
            await self.start(self.env_vars["token"])


bot = GhoztBot(command_prefix=PREFIX, intents=intents)


async def check_if_bot_owner(ctx) -> bool:
    return ctx.message.author.id == int(bot.env_vars["bot_owner_id"])


if __name__ == "__main__":
    asyncio.run(bot.main())
