"""
Crabada script to send mining all available teams for
the given user.

Usage:
    python -m bin.mining.CloseAndStartMine_Swimmer

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

userAddress = secondOrNone(argv)

if not userAddress:
    logger.error('Specify a user address')
    exit(1)

if not User.isRegistered(userAddress):
    logger.error('The given user address is not registered')
    exit(1)
count = 0

availableTeams = []

crabadaWeb3CLient_ = crabadaWeb3Client(userAddress)
for teamId in availableTeams:
    for pos in range(0, 3):

        txBool = False
        while not txBool:
            try:
                txHash = crabadaWeb3CLient_.removeCrabadaFromTeam(teamId, pos)
                txLogger.info(txHash)
                txReceipt = crabadaWeb3CLient_.getTransactionReceipt(txHash)
                logTx(txReceipt)
                txBool =True
                if txReceipt['status'] != 1:
                    logger.error(f'Error removing crabada from team {teamId}')
                else:
                    logger.info(f'Crab {pos} removed from team {teamId} correctly')
                    count += 1
            except:
                pass

        sleep(1)




print(count)
