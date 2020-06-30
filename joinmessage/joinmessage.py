import logging

import discord
from redbot.core import Config, commands

log = logging.getLogger("red.flare.joinmessage")

CHANNELS = [
    "general",
    "general-chat",
    "основной",
    "основной-чат",
    "generell",
    "generell-chatt",
    "כללי",
    "צ'אט-כללי",
    "allgemein",
    "generale",
    "général",
    "općenito",
    "bendra",
    "általános",
    "algemeen",
    "generelt",
    "geral",
    "informații generale",
    "ogólny",
    "yleinen",
    "allmänt",
    "allmän-chat",
    "chung",
    "genel",
    "obecné",
    "obično",
    "Генерален чат",
    "общи",
    "загальний",
    "ทั่วไป",
    "常规",
]


class JoinMessage(commands.Cog):
    """Send a message on guild join."""

    __version__ = "0.0.5"
    __author__ = "flare#0001"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad."""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}\nAuthor: {self.__author__}"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1398467138476, force_registration=True)
        self.config.register_global(message=None, toggle=False)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if not await self.config.toggle():
            return
        msg = await self.config.message()
        if msg is None:
            log.info("No message setup, please set one up via the joinmessage message command.")
            return
        channel = discord.utils.find(lambda x: x.name in CHANNELS, guild.text_channels)
        if channel is None:
            channel = (
                guild.system_channel
                if guild.system_channel is not None
                and guild.system_channel.permissions_for(guild.me).send_messages
                else next(
                    (x for x in guild.text_channels if x.permissions_for(guild.me).send_messages),
                    None,
                )
            )
            if channel is None:
                log.debug("Couldn't find a channel to send join message in {}".format(guild))
        await channel.send(msg)
        log.debug("Guild welcome message sent in {}".format(guild))

    @commands.group()
    @commands.is_owner()
    async def joinmessage(self, ctx):
        """Options for sending messages on server join."""

    @joinmessage.command(usage="type")
    async def toggle(self, ctx, _type: bool = None):
        """Toggle server join messages on or off."""
        if _type is None:
            _type = not await self.config.toggle()
        await self.config.toggle.set(_type)
        if _type:
            await ctx.send("Server join messages have been enabled.")
            return
        await ctx.send("Server join messages have been disabled.")

    @joinmessage.command()
    async def message(self, ctx, *, message: str = None):
        """Set the message to be sent on join.

        Sending no message will show the current message or help menu if
        none is set.
        """
        if message is None:
            msg = await self.config.message()
            if msg is None:
                await ctx.send_help()
                return
            await ctx.send("Your current message being sent is:\n{}".format(msg))
            return
        await self.config.message.set(message)
        await ctx.send("Your message will be sent as:\n{}".format(message))
