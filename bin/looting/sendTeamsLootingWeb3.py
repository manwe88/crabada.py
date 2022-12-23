#!/usr/bin/env python3
"""
Crabada script to send looting all available teams for
the given user.

Usage:
    python3 -m bin.sendTeamsLooting <userAddress>

"""

from src.bot.looting.sendTeamsLootingWeb3 import sendTeamsLooting
from src.helpers.General import secondOrNone
from src.models.User import User
from src.common.logger import logger
from sys import argv, exit

userAddress = secondOrNone(argv)
# userAddress = ''

if not userAddress:
    logger.error('Specify a user address')
    exit(1)

if not User.isRegistered(userAddress):
    logger.error('The given user address is not registered')
    exit(1)

# has put into loop according to team count
nAttackedMines = 0
# while nAttackedMines < 2:
nAttackedMines = sendTeamsLooting(userAddress, nAttackedMines)
