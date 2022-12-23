"""
Send a user's available teams looting
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
# from src.helpers.Sms import sendSms
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
# from src.strategies.StrategyFactory import getBestMineToLoot
# from src.strategies.loot.LowestBpLootStrategy import LowestBpLootStrategy
# from bin.looting.getfirstMine3 import getMines
import time
from random import randbytes

def sendTeamsLooting(userAddress: Address, nAttackedMines : int ) -> int:
    """
    Send all available teams of crabs to loot.
    
    A mine game will be attacked for each available team; returns the
    number of mines attacked.

    """
    availableTeams = crabadaWeb2Client.listTeams(userAddress, {
        "is_team_available": 1,
        "limit": 20, # with new patch this is limited to 20
        "page": 1})

    # availableTeams = [{'team_id': 12646}]

    if not availableTeams:
        logger.info('No available teams to send looting for user ' + str(userAddress))
        return 0

    # Send the teams
    # nAttackedMines = 0
    for t in availableTeams:

        teamId = t['team_id']
        logger.info(f'Sending team {teamId} to loot...')

        # Find best mine to loot
        # mine = getMines()
        # mine = findMine(crabadaWeb2Client)
        # if not mine:
        #     logger.warning(f"Could not find a suitable mine to loot for team {teamId}")
        #     continue

        crabadaWeb3Client_ = crabadaWeb3Client(userAddress)

        # Find best mine to loot
        mine = crabadaWeb3Client_.getMines()
        if not mine:
            logger.warning(f"Could not find a suitable mine to loot for team {teamId}")
            continue

        # Create Certificate for attack method
        msg = str(mine[0]) + str(teamId)
        certificate = crabadaWeb3Client_.certificate(msg)

        # Send the attack tx
        start = time.time()
        txHash = crabadaWeb3Client_.attack(mine[0], teamId, certificate)
        end = time.time()
        print('Tx Send Time:', end - start, 'Mine:', mine[0])
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client_.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt['status'] != 1:
            # sendSms(f'Crabada: ERROR attacking > {txHash}')
            logger.error(f'Error attacking mine {str(mine[0])} with team {teamId}')
        else:
            nAttackedMines += 1
            logger.info(f'Team {teamId} sent succesfully')

    return nAttackedMines