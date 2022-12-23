"""
Crabada script to send mining all available teams for
the given user.

Usage:
    python -m bin.mining.CloseAndStartMine_Swimmer <userAddress>

"""
import time
import sys
from src.helpers.General import secondOrNone
from src.models.User import User
from src.common.txLogger_1 import txLogger, logTx
from src.common.logger_1 import logger
from sys import argv, exit
from src.helpers.Dates import countdown
from time import time
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from time import sleep

# TODO: Find crabada location
# TODO 2: check crabada location when adding to team
# TODO 3: write crabada ids to .env and take team and crab ids from .env

userAddress = secondOrNone(argv)
# userAddress = ''

if not userAddress:
    logger.error('Specify a user address')
    exit(1)

if not User.isRegistered(userAddress):
    logger.error('The given user address is not registered')
    exit(1)


crabadaWeb3CLient_ = crabadaWeb3Client(userAddress)
teamPairs = [{11111: [11111, 11111, 11111]}, {11111: [11111, 11111, 11111]}, {11111: [11111, 11111, 11111]}]


"""
Change this list according to intended adding
"""
teamIds = []
teamList = []
for id in teamIds:
    for item in teamPairs:
        if id == list(item.keys())[0]:
            teamList.append(item)

for team in teamList:
    teamId = list(team.keys())[0]
    crabadaIds = team.get(teamId)
    for pos in range(0, 3):
        crabadaId = crabadaIds[pos]
        txHash = crabadaWeb3CLient_.addCrabadaToTeam(teamId, pos, crabadaId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3CLient_.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt['status'] != 1:
            logger.error(f'Error adding crabada {crabadaId} to the team {teamId}')
        else:
            logger.info(f'Crab {crabadaId} added to the team {teamId} correctly')
