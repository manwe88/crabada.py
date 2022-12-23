"""
Reinforce function from own inventory
"""

from web3.main import Web3
from src.common.exceptions import CrabBorrowPriceTooHigh
from src.common.logger_1 import logger
from src.common.txLogger_1 import txLogger, logTx
from src.helpers.Reinforce import minerCanReinforce, underOneMinuteToReinforce
# from src.helpers.sms import sendSms
from time import time, sleep
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from src.models.User import User
from src.common.config import CrabsForLending
from src.strategies.StrategyFactory import getBestReinforcementDefence, getOwnReinforcementDefence
from src.helpers.Mines import getRemainingTimeFormatted
from src.helpers.Dates import getPrettySeconds


def reinforceDefense(userAddress: Address, OwnedCrabs, reinforcedGames, nReinforced):
    """
    Check if any of the teams of the user that are mining can be
    reinforced, and do so if this is the case; return the
    number of borrowed reinforcements.
    
    TODO: find a way to print remaining time for renting crabs when just starting this code
    / look at process info of a game and also its crab info
    TODO: add crabRemainingTime type to types.py
    TODO: change reeinforcement strategy if bp difference is lower than 5
    """

    user = User(userAddress)
    openMines = crabadaWeb2Client.listMyOpenMines(userAddress)
    availableCrabs = crabadaWeb2Client.listOwnCrabsForLendingChecker()
    # availableCrabs = []
    reinforceableMines = [m for m in openMines if minerCanReinforce(m)]
    if not reinforceableMines:
        logger.info('No mines to reinforce for user ' + str(userAddress))
        nextCrabtoReinforce = OwnedCrabs.getRemainingTimeForRent()
        for crab in CrabsForLending:
            logger.info(f"Next crab {crab} will be available in {getPrettySeconds(nextCrabtoReinforce.get(crab))}")
        return nReinforced, reinforcedGames

    # Reinforce the mines
    nBorrowedReinforcements = 0
    for mine in reinforceableMines:

        # Find best reinforcement crab to borrow
        mineId = mine['game_id']
        if mineId in reinforcedGames.keys():
            if int(time() - reinforcedGames[mineId]) > 90:
                del reinforcedGames[mineId]
            else:
                continue

        maxPrice = user.config['maxPriceToReinforceInTus']
        strategyName = user.getTeamConfig(mine['team_id']).get('reinforceDefenceStrategyName')
        crab = []
        if availableCrabs:
            try:
                crab = getOwnReinforcementDefence(userAddress, mine, availableCrabs, maxPrice)
            except:
                logger.warning(f"Could not get crab info to reinforce {mineId}")
                continue

        if not crab and underOneMinuteToReinforce(mine):
            txReceipt = 0
            while txReceipt != 1:
                try:
                    crab = getBestReinforcementDefence(userAddress, mine, maxPrice)
                except CrabBorrowPriceTooHigh:
                    if crab:
                        logger.warning(
                            f"Price of crab is {Web3.fromWei(crab['price'], 'ether')} TUS which exceeds the user limit of {maxPrice} [strategyName={strategyName}]")
                        continue
                    else:
                        logger.warning(
                            f"Could not find an affordable crab where user limit is {maxPrice} [strategyName={strategyName}]")
                        break
                if not crab:
                    logger.warning(
                        f"2nd ERROR/Could not find an affordable crab where user limit is {maxPrice} [strategyName={strategyName}]")
                    break
                # Borrow the crab
                crabId = crab['crabada_id']
                price = crab['price']

                # dont use crab if it is used within 30 seconds
                # if crabId in reinforcedCrabs.keys():
                #     if (reinforcedCrabs[crabId] - time()) > 30:
                #         del reinforcedCrabs[crabId]
                #     else:
                #         continue
                logger.info(
                    f"Borrowing crab {crabId} for mine {mineId} at {price} TUS... [strategy={strategyName}, BP={crab['battle_point']}, MP={crab['mine_point']}]")

                try:
                    crabadaWeb3Client_ = crabadaWeb3Client(userAddress)
                    txHash = crabadaWeb3Client_.reinforceDefense(mineId, crabId, price)
                    txLogger.info(txHash)
                    txReceipt = crabadaWeb3Client_.getTransactionReceipt(txHash)
                    rentTime = time()
                    logTx(txReceipt)
                except:
                    break
                if txReceipt['status'] != 1:
                    # sendSms(f'Crabada: ERROR reinforcing > {txHash}')
                    logger.error(f'Error reinforcing mine {mineId}')
                    sleep(1)
                    break  # keeps looping after reinforcing correctly, so put break here TODO: remove break
                else:
                    txReceipt = 1
                    nBorrowedReinforcements += 1
                    logger.info(f"Mine {mineId} reinforced correctly")
                    reinforcedGames[mineId] = rentTime
                    sleep(1)
            continue

        if not crab:
            nextCrabtoReinforce = OwnedCrabs.getRemainingTimeForRent()
            for crab in CrabsForLending:
                logger.warning(
                    f"Next crab {crab} will be available in {getPrettySeconds(nextCrabtoReinforce.get(crab))}")
            continue

        crabId = crab['crabada_id']

        if crabId in OwnedCrabs.crabs.keys():
            if (int(time() - OwnedCrabs.crabs[crabId]) < 1700) and OwnedCrabs.crabs[crabId] != 0:
                continue

        if crabId in CrabsForLending:
            price = 0
        else:
            price = crab['price']
        logger.info(
            f"Borrowing crab {crabId} for mine {mineId} at {price} TUS... [strategy={strategyName}, BP={crab['battle_point']}, MP={crab['mine_point']}]")
        # Borrow the crab
        try:
            crabadaWeb3Client_ = crabadaWeb3Client(userAddress)
            txHash = crabadaWeb3Client_.reinforceDefense(mineId, crabId, price)
            txLogger.info(txHash)
            txReceipt = crabadaWeb3Client_.getTransactionReceipt(txHash)
            # Register crab's rent time and remove it from available list
            rentTime = time()
            if crabId in CrabsForLending and txReceipt['status'] == 1:
                OwnedCrabs.crabs[crabId] = rentTime
                availableCrabs.remove(crabId)
            logTx(txReceipt)
        except:
            continue
        if txReceipt['status'] != 1:
            # sendSms(f'Crabada: ERROR reinforcing > {txHash}')
            logger.error(f'Error reinforcing mine {mineId}')
            sleep(1)
        else:
            nBorrowedReinforcements += 1
            logger.info(f"Mine {mineId} reinforced correctly")
            reinforcedGames[mineId] = rentTime
            sleep(1)

    return nBorrowedReinforcements, reinforcedGames
