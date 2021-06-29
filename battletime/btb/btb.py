import discord
import traceback
import discord
from glob import glob
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from ..db import db
from battletime import __version__
from pathlib import Path

STDOUTCH = 855328768276430878

def custom_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guild WHERE GuildID = ?", message.guild.id)
    return commands.when_mentioned_or(prefix)(bot, message)


class Battletime(commands.Bot):
    def __init__(self):
        self.exts = [p.stem for p in Path(".").glob("./battletime/btb/exts/*.py")]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)
        self._acticity = discord.Activity(type=discord.ActivityType.listening, name="@BattleTime help")
        self.hg = STDOUTCH
        
        super().__init__(
            command_prefix=custom_prefix, 
            case_insensitive=True, 
            intents=discord.Intents.all(),
            activity=discord.Activity(
                status=discord.Status.dnd,
                name=f"{self._acticity} - {__version__}"
            ),
        )
        
    def setup(self):
        print("Running setup...")
        for ext in self.exts:
            self.load_extension(f"battletime.btb.exts.{ext}")
            print(f" `{ext}` extension loaded.")
            
    
    def run(self):
        self.setup()
        
        
        with open("./btdata/secrets/token.txt", mode="r", encoding="utf-8") as f:
            token = f.read()
            
        print(f"Running bot")
        super().run(token, reconnect=True)
        
    async def close(self):
        print("Shutting down...")
        self.scheduler.shutdown()
        await self.hg.send(f"Shutting down Battletime v{__version__}.")
        await super().close()
            
        
    async def on_connect(self):
            print(f" Bot connected. DWSP latency: {self.latency * 1000:,.0f} ms")

    async def on_disconnect(self):
        print(f" Bot disconnected.")
        
    async def on_error(self, err: str, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        traceback.print_exc()
        
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or isinstance(message.channel, discord.DMChannel):
            return

        await self.process_commands(message)

    async def process_commands(self, message: discord.Message) -> None:
        ctx = await self.get_context(message, cls=commands.Context)

        if ctx.command is None:
            return

        await self.invoke(ctx)