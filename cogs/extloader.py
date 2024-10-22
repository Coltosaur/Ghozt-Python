import traceback

from os import listdir
from os.path import isfile, join
from discord.ext import commands
from bot import check_if_bot_owner
from common.constants import COGS_DIR


class ExtLoader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(check_if_bot_owner)
    async def get_extension_list(self, ctx):
        extension_list = []
        for extension in [
            f.replace(".py", "")
            for f in listdir(COGS_DIR)
            if (isfile(join(COGS_DIR, f)) and f.endswith(".py"))
        ]:
            extension_list.append(extension)
        await ctx.send("list of extensions: {}".format(extension_list))

    @commands.command(hidden=True)
    @commands.check(check_if_bot_owner)
    async def load(self, ctx, extension_name: str):
        """Loads an extension."""
        try:
            await self.bot.load_extension("cogs." + extension_name)
            await ctx.send("{} loaded.".format(extension_name))
        except Exception as e:
            print(traceback.format_exc())

    @commands.command(hidden=True)
    @commands.check(check_if_bot_owner)
    async def unload(self, ctx, extension_name: str):
        """Unloads an extension."""
        try:
            await self.bot.unload_extension("cogs." + extension_name)
            await ctx.send("{} unloaded.".format(extension_name))
        except Exception as e:
            print(traceback.format_exc())

    @commands.command(hidden=True)
    @commands.check(check_if_bot_owner)
    async def reload(self, ctx, extension_name: str):
        """Reloads an extension."""
        try:
            await self.bot.unload_extension("cogs." + extension_name)
            await ctx.send("{} unloaded.".format(extension_name))

            await self.bot.load_extension("cogs." + extension_name)
            await ctx.send("{} loaded.".format(extension_name))
        except Exception as e:
            print(traceback.format_exc())


async def setup(bot):
    await bot.add_cog(ExtLoader(bot))
