"""
This file is for handling the loading of the core cogs
"""

import os
import sys
import importlib
import logging
import traceback
from discord.ext import commands
from helpers.logs import TerminalColors


def getClassName(filename: str, logger: logging.Logger) -> str:
    """
    Get the class name from the filename.
    """
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("class"):
                return line.split(" ")[1].split("(")[0]

    logger.warning(
        "Could not find class name in file %s%s%s",
        TerminalColors.RED_BOLD,
        filename,
        TerminalColors.RESET_COLOR,
    )
    sys.exit(1)


async def loadCoreCogs(bot: commands.Bot, directory: str) -> None:
    """
    Iterate through the commands folder and load all commands.
    """

    for file in os.listdir(directory):
        # if the file is a directory
        if os.path.isdir(f"{directory}/{file}"):
            try:
                # get the class from the module
                for sub_file in os.listdir(f"{directory}/{file}"):
                    logger = logging.getLogger(
                        f"discord.{directory}.{sub_file}.cog.loader"
                    )
                    if sub_file.endswith(".py"):
                        class_name = getClassName(
                            f"{directory}/{file}/{sub_file}", logger
                        )
                        module_name = f"{directory}.{file}.{sub_file[:-3]}"
                        module = importlib.import_module(module_name)
                        class_ = getattr(module, class_name)
                        await bot.add_cog(class_(bot))
                        logger.info(
                            "Loaded core cog %s%s%s",
                            TerminalColors.GREEN_BOLD,
                            module_name,
                            TerminalColors.RESET_COLOR,
                        )
            except ImportError as import_error:
                logger.warning(
                    "Could not load core cog %s%s%s - Exception: %s",
                    TerminalColors.RED_BOLD,
                    sub_file,
                    TerminalColors.RESET_COLOR,
                    import_error,
                )
                logger.warning(traceback.format_exc())

        if file.endswith(".py"):
            logger = logging.getLogger(f"discord.{directory}.cog.loader")
            try:
                class_name = getClassName(f"{directory}/{file}", logger)
                module_name = f"{directory}.{file[:-3]}"
                module = importlib.import_module(module_name)
                class_ = getattr(module, class_name)
                await bot.add_cog(class_(bot))
                logger.info(
                    "Loaded core cog %s%s%s",
                    TerminalColors.GREEN_BOLD,
                    module_name,
                    TerminalColors.RESET_COLOR,
                )
            except ImportError as import_error:
                logger.warning(
                    "Could not load %s cog %s%s%s - Exception: %s",
                    directory,
                    TerminalColors.RED_BOLD,
                    file,
                    TerminalColors.RESET_COLOR,
                    import_error,
                )
                logger.warning(traceback.format_exc())
