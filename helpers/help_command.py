"""
This containes the configuration for the help command.
"""

from discord.ext import commands


def getHelpCommand() -> commands.HelpCommand:
    """
    Get the help command configuration.

    Returns:
        commands.HelpCommand: The help command configuration.
    """
    help_command = commands.DefaultHelpCommand(
        dm_help=True,
        paginator=commands.Paginator(prefix="```", suffix="```"),
    )

    return help_command
