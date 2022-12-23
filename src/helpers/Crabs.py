
from src.common.config import CrabsForLending
from time import time

def getRemainingTimeForRent(OwnedCrabs):

    remainingTimes = []
    for crab in CrabsForLending:
        remaining = 1800 - int(time() - OwnedCrabs.crabs.get(crab))
        remainingTimes.append(remaining)
    return remainingTimes
