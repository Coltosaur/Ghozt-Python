from discord.ext import commands
from discord.app_commands import autocomplete
import datetime


class Timey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @autocomplete()
    async def timey(self, ctx, hour: int, minute: int):
        """Converts today's date and input hour/minute to a unix timestamp and displays in local time"""
        try:
            today = datetime.date.today()
            month = today.month
            year = today.year
            day = today.day

            unix_time = int(datetime.datetime(year, month, day, hour, minute).timestamp())
        except Exception:
            await ctx.send('enter hour and minute using 24 hour time')
            return

        result = "<t:{}> and unix timestamp: {}".format(str(unix_time), str(unix_time))
        await ctx.send(result)

    @commands.command()
    async def long_timey(self, ctx, month: int, day: int, hour: int, minute: int):
        """Converts desired month/day time to unix timestamp and displays in local time"""
        try:
            today = datetime.date.today()
            year = today.year

            unix_time = int(datetime.datetime(year, month, day, hour, minute).timestamp())
        except Exception:
            await ctx.send('usage is ^^timey M D Hr Min - numbers for each one')
            return

        result = "<t:{}> and unix timestamp: {}".format(str(unix_time), str(unix_time))
        await ctx.send(result)


async def setup(bot):
    await bot.add_cog(Timey(bot))
