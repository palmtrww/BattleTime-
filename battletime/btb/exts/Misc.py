import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="ping")
    async def _ping(self, ctx):
        embed = discord.Embed(
            title=f"```{round(self.bot.latency * 1000)}ms```"
        )
        await ctx.reply(embed=embed)
        
def setup(bot):
    bot.add_cog(Misc(bot))