import discord
from discord.ext import commands
from  battletime.db import db


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="cprefix", aliases=["ChangePrefix"], brief="Changes the prefix.")
    @commands.has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        """Changes the prefix for the server.\n`Manage Server` permission required."""
        if len(new) > 10:
            await ctx.reply(
                "The prefix can not be more than 10 characters.", delete_after=10
            )

        else:
            db.execute(
                "UPDATE guild SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id
            )
            db.commit()
            embed = discord.Embed(
                title="Prefix Changed",
                description=f"Prefix has been changed to `{new}`",
            )
            await ctx.reply(embed=embed)
            
    @commands.command(name="prefix")
    async def prefix(self, ctx):
        prefix = db.field("SELECT Prefix FROM guild WHERE GuildID = ?", ctx.guild.id)
        await ctx.reply(prefix)

def setup(bot):
    bot.add_cog(Prefix(bot))