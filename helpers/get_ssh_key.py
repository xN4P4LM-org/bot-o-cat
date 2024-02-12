"""
This file is a helper file to confirm there is an ssh key available.
"""

import os
import logging
import sys

from helpers.env import getEnvVar

logger = logging.getLogger("discord.ssh.key.loader")


def getPubKey() -> str:
    """
    Get the public ssh key from the file system.

    Returns:
        str The contents of the file if it exists
    """

    logger.info("Getting public ssh key")

    root_ssh_dir = getEnvVar("DISCORD_SSH_PATH", "/root/.ssh")

    pub_key = findBestPubKey(root_ssh_dir)

    logger.info("Public ssh key found: %s", os.path.join(root_ssh_dir, pub_key))

    with open(
        os.path.join(root_ssh_dir, pub_key), "r", encoding="utf-8"
    ) as open_pub_key:
        return open_pub_key.read().strip("\n")


def findBestPubKey(key_path: str) -> str:
    """
    Get the best key for the bot to use.

    The best key order is
    1. id_ed25519.pub
    2. id_rsa.pub
    3. *.pub

    """

    private_key = findBestPrivateKey(key_path)
    public_key = private_key + ".pub"

    return public_key


def findBestPrivateKey(key_path: str) -> str:
    """
    Get the best key for the bot to use.

    The best key order is
    1. id_ed25519
    2. id_rsa
    3. *

    """
    dir_contents = os.listdir(key_path)
    matches = ["id_ed25519", "id_rsa"]
    no_match = ["config", "known_hosts", "authorized_keys"]
    private_key = searchFiles(dir_contents, matches, no_match)

    if private_key is not None:
        return private_key

    logger.critical("No ssh keys found in %s", key_path)
    sys.exit(1)


def searchFiles(
    dir_contents: list[str], search_files: list[str], no_match: list[str]
) -> str | None:
    """
    Search for the first matching file in the provided directory contents,
    and return the file if it exists.

    Arguments:
        dir_contents: The directory contents to search
        search_files: The files to search for in the order provided
    """

    for file in dir_contents:
        if file.endswith(".pub"):
            dir_contents.remove(file)
        if file in no_match:
            dir_contents.remove(file)

    if len(dir_contents) == 1:
        return dir_contents[0]

    for file in search_files:
        if file in dir_contents:
            return file

    logger.debug("No file found in %s", dir_contents)
    return None
