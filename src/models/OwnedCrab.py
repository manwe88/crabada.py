from __future__ import annotations
from typing import List
from src.common.config import CrabsForLending
from src.common.exceptions import UserException
from src.models.Model import Model
from time import time


class OwnedCrabs(Model):
    """
    User's crabs to be used in rent, printing their remaining time
    for next rent if necessary
    TODO: If reinforcement code stopped and started again, it does not give remaining time for crabs previously rented
    so find a way to print them too.
    TODO: implement user specific crabs for lending from its own inventory
    TODO: give better names
    """

    config: List = None

    def __init__(self):
        self.config = OwnedCrabs.getCrabConfig()
        self.crabs = OwnedCrabs.getConfigCrabs(self.config)
        self.rem = {}
        # if not self.config:
        #     raise UserException("Crab ids not registered")

    def getRemainingTimeForRent(self):

        for crab in CrabsForLending:
            remaining = abs(1800 - int(time() - self.crabs.get(crab)))
            if remaining > 1800:
                self.rem[crab] = 0
            else:
                self.rem[crab] = remaining
        return self.rem

    @staticmethod
    def getCrabConfig():
        return CrabsForLending

    @staticmethod
    def getConfigCrabs(crabs):

        res = {}
        for crab in crabs:
            res[crab] = 0
        return res
