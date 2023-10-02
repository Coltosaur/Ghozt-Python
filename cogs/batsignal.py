from discord.ext import commands
from discord import Member, File


class BATSIGNAL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bat_signal_file = "BatSignal_For_Games.png"

    @commands.command()
    async def signal(self, ctx, members: commands.Greedy[Member], *, reason=None):
        """
        command that signals for games, format <@mentions> <reason>.
        :param ctx: context for the message
        :param members: each user mention to be signaled
        :param reason: why we're being signaled
        :return:
        """
        # signaled = ", ".join(x.name for x in members)
        await ctx.send(file=File(self.bat_signal_file))


async def setup(bot):
    await bot.add_cog(BATSIGNAL(bot))
