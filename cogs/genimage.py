from discord.ext import commands
from io import BytesIO
from diffusion_setup import get_pipeline
from discord import File
import torch


class GenImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Initialize Stable Diffusion pipeline
        self.pipeline = get_pipeline()

    @commands.hybrid_command(
        name="generate",
        with_app_command=True,
        description="Build all the imagery, literally!",
    )
    async def generate(self, ctx: commands.Context, *, prompt: str):
        """
        command that generates an image based off of a prompt, format <prompt>.
        :param ctx: context for the message
        :param prompt: the thing the AI is supposed to draw for you
        :return:
        """
        await ctx.send(f"Generating image for: {prompt}")

        # Generate the image
        with torch.no_grad():
            image = self.pipeline(prompt=prompt, guidance_scale=7.5).images[0]

        # Convert image to BytesIO and send it
        with BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)
            await ctx.send(file=File(fp=image_binary, filename="image.png"))


async def setup(bot):
    await bot.add_cog(GenImage(bot))
