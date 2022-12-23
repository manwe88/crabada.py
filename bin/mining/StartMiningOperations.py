"""
Crabada script to send mining all available teams for
the given user.

Usage:
    python -m bin.mining.StartMiningOperations <userAddress>

"""
import time
import sys
from src.bot.mining.sendTeamsMining import sendTeamsMining
from src.bot.mining.closeMines import closeMines
from src.bot.mining.reinforceDefenseFromSelf import reinforceDefense
from src.helpers.General import secondOrNone
from src.models.User import User
from src.models.OwnedCrab import OwnedCrabs
from src.common.logger_1 import logger
from sys import argv, exit
from src.helpers.Dates import countdown
from time import time
from src.common.clients import crabadaWeb2Client

userAddress = secondOrNone(argv)
teams = 0

if not userAddress:
    logger.error('Specify a user address')
    exit(1)

User = User(userAddress)
OwnedCrabs = OwnedCrabs()
# reinforcedCrabs = {}
reinforcedGames = {}
closedGames = {}

if not User.isRegistered(userAddress):
    logger.error('The given user address is not registered')
    exit(1)

timeOfTx = 0
nSentTeams = 4
while True:
    try:

        nClosedGames = 0
        closedTeams = []
        nClosedGames, closedTeams, message, closedGames = closeMines(userAddress, nClosedGames, closedTeams,
                                                                     closedGames)
        if message != '':
            print(message)

        #################################
        # Get Time of Previous Mine Sent
        #################################
        try:
            openMines = crabadaWeb2Client.listMyOpenMinesDesc(userAddress)
            timeOfTx = openMines[0]['start_time']
        except:
            pass
        startedTeams = []
        if int(time() - timeOfTx) > User.mineInterval() or (nSentTeams < 4):
            if int(time() - timeOfTx) > User.mineInterval():
                nSentTeams = 0
            nSentTeams, startedTeams, timeOfTx = sendTeamsMining(userAddress, nSentTeams, startedTeams, timeOfTx, User)

        else:
            print(f'{User.mineInterval() / 60} min not passed since previous mine sent!')

        nReinforced = 0
        nReinforced, reinforcedGames = reinforceDefense(userAddress, OwnedCrabs, reinforcedGames, nReinforced)
        countdown(15)

    except KeyboardInterrupt:
        sys.exit(1)
    except:
        logger.error('Connection Error, continuing iteration...')
        continue
