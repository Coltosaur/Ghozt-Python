from discord.ext import commands


class PeriodicPhrases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # List of all element symbols (1- or 2-character abbreviations)
        self.element_symbols = {
            'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
            'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br',
            'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te',
            'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm',
            'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
            'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr',
            'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
        }

        # Memoization dictionary to avoid recalculating subproblems
        self.memo = {}

    @commands.hybrid_command(name="find_phrase", with_app_command=True,
                             description="Try to find the given phrase with the abbreviations of elements in the periodic table!")
    async def find_phrase(self, ctx: commands.Context, phrase: str):
        """
        command that returns a list of elemental abbreviations to form the phrase
        :param ctx: context for the message
        :param phrase: the word or phrase we're looking for in the periodic table
        :return:
        """
        self.memo = {}  # zero out the memo for a new phrase
        combinations = self.find_all_combinations(phrase)

        if combinations:
            await ctx.send(f'Valid combinations for the phrase "{phrase}":')
            for combo in combinations:
                await ctx.send(" - ".join(combo))
        else:
            await ctx.send(f'No valid combinations found for the phrase "{phrase}".')

    def find_all_combinations(self, phrase, index=0):
        # If we reach the end of the phrase, return a valid empty list
        if index == len(phrase):
            return [[]]

        # If this subproblem has already been computed, return the cached result
        if index in self.memo:
            return self.memo[index]

        # List to store all valid combinations starting from 'index'
        valid_combinations = []

        # Try using 1 or 2 characters as element symbols
        for i in range(1, 3):
            part = phrase[index:index + i].capitalize()  # Get the substring and capitalize it
            if part in self.element_symbols:
                # Recursively find valid combinations for the remaining part of the phrase
                remaining_combinations = self.find_all_combinations(phrase, index + i)
                # Append the current symbol to each combination of the remainder
                for combo in remaining_combinations:
                    valid_combinations.append([part] + combo)

        # Store the result in the memoization dictionary
        self.memo[index] = valid_combinations
        return valid_combinations


async def setup(bot):
    await bot.add_cog(PeriodicPhrases(bot))
