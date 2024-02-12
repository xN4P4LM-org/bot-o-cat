"""
This contains operations to read environment variables and return them to the caller.
"""

import sys
import os
import logging

logger = logging.getLogger("discord.env")

def getEnvVar(var_name: str, _value: str | None = None) -> str:
    """
    Get an environment variable.

    Arguments:
        var_name: The name of the environment variable to get.

    Returns:
        str | bool: The value of the environment variable if it exists,
        False otherwise.
    """
    try:
        return os.environ[var_name]
    except KeyError as key_error:

        if _value is not None:
            logger.warning(
                "Environment variable %s not found: - Using default value: %s",
                var_name,
                _value
                )
            return _value

        logger.error(
            "Environment variable %s not found: %s - EXITING",
            var_name,
            key_error)
        sys.exit(1)
