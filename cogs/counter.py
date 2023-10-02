from discord.ext import commands


class COUNTER(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter_file = "counters.txt"

    @commands.command()
    async def count(self, ctx, name: str, new_counter: str = None):
        """
        create a new counter or add 1 to an existing counter.
        :param ctx: context of the command message
        :param name: name of the value that we want to increase counter for
        :param new_counter: is this a new counter name? only needed if new, default false
        :return: increases count of the named value by 1
        """
        if new_counter == "new":
            with open(self.counter_file, "a+") as counters:
                counters.write(name + ":1\n")
            op = self.display_current_counters()
            await ctx.send(op)
        else:
            # read and store the current counters
            current_counters = self.get_current_counters()
            # validate name with counter_names and increase count if exists
            try:
                current_counters[name] += 1
                # write all the values back to the counters file, keeping it simple
                with open(self.counter_file, "w") as counters:
                    for counter in current_counters.items():
                        counters.write(counter[0] + ":" + str(counter[1]) + "\n")
            except KeyError as e:
                await ctx.send("```{} is not currently being tracked.\nPlease add the new_counter True option if " \
                               "adding a new counter.```".format(name))
            op = self.display_current_counters()
            await ctx.send(op)

    @commands.command()
    async def current_counters(self, ctx):
        """
        lets you see all of the current counters for your guild.
        :param ctx: context of the command message
        :return: sends a message to the users' discord channel containing a
        list of all named counters
        """
        op = self.display_current_counters()
        await ctx.send(op)

    def display_current_counters(self):
        opstring = "```\n"
        with open(self.counter_file, "r") as counters:
            for counter in counters:
                counter_info = counter.split(":")
                name = counter_info[0]
                value = counter_info[1]
                opstring += "{} : {}".format(name, value)
        opstring += "```"
        return opstring

    def get_current_counters(self):
        counter_dict = {}
        with open(self.counter_file, "r") as counters:
            for counter in counters:
                counter_info = counter.split(":")
                counter_name = counter_info[0]
                value = counter_info[1]
                counter_dict[counter_name] = int(value)
        return counter_dict


async def setup(bot):
    await bot.add_cog(COUNTER(bot))
