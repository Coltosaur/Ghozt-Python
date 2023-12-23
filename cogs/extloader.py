import traceback

from discord.ext import commands
from bot import check_if_bot_owner


class EXTLOADER(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(check_if_bot_owner)
    async def load(self, ctx, extension_name: str):
        """Loads an extension."""
        try:
            await self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        except Exception as e:
            print(traceback.format_exc())
        await ctx.send("{} loaded.".format(extension_name))

    @commands.command(hidden=True)
    @commands.check(check_if_bot_owner)
    async def unload(self, ctx, extension_name: str):
        """Unloads an extension."""
        try:
            await self.bot.unload_extension(extension_name)
            await ctx.send("{} unloaded.".format(extension_name))
        except Exception as e:
            print(traceback.format_exc())


async def setup(bot):
    await bot.add_cog(EXTLOADER(bot))
