from typing import Any, List
from src.libs.CrabadaWeb2Client.types import OwnCrabForLending, Game
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy
from src.helpers.General import firstOrNone
from src.helpers.Price import weiToTus

class OwnBpReinforcement(ReinforceStrategy):
    """
    Strategy that chooses the crab with a price lower than maxPrice
    which has the highest mine point value
    """

    def query(self, game: Game) -> dict[str, Any]:
        return {
            "limit": 200, # TODO: make it an argument
            "orderBy": 'mine_point', # default 'price'
            "order": 'desc', # default 'asc'
            # 'mine_point': 81
            # "class_name": 'PRIME', # is not allowed by api
            # "pure_number": 6 # is not allowed by api
        }



    def crab(self, game: Game, list: List) -> OwnCrabForLending:

        try:
            teamMembers = self.listTeamMembers_2(game)

        except:
            teamMembers = self.listTeamMembers(game)

        try:

            for crab in list:

                if crab['id'] not in teamMembers:
                    return crab['data']
                # elif list[1]['id'] not in teamMembers:
                #     return list[1]['data']
        except:
            return []
        return []

    def crab2(self, game: Game, list: List) -> OwnCrabForLending:

        try:
            teamMembers = self.listTeamMembers_2(game)

        except:
            teamMembers = self.listTeamMembers(game)

        try:

            for crab in list:

                if crab['id'] not in teamMembers:
                    return crab['data']
                # elif list[1]['id'] not in teamMembers:
                #     return list[1]['data']
        except:
            return []
        return []

    def _getCrab1(self, crabIDs) -> OwnCrabForLending:
        """
        Fetch and return a reinforcement crab using the strategy set in
        query1() and crab1(). If no crab can be found, return None.
        """
        crabsForLending = self.web2Client.listOwnCrabsForLendingAvailable(crabIDs)
        crab = self.crab(self.game, crabsForLending)
        return crab

    def _getCrab2(self, crabIDs) -> OwnCrabForLending:
        """
        Fetch and return a reinforcement crab using the strategy set in
        query2() and crab2(). If no crab can be found, return None.
        """
        crabsForLending = self.web2Client.listOwnCrabsForLendingAvailable(crabIDs)
        crab = self.crab2(self.game, crabsForLending)
        return crab

    def listTeamMembers(self, game: Game) -> List[int]:

        teamMemberIds = []
        for teams in game['defense_team_members']:
            teamMemberIds.append(teams['crabada_id'])
        return teamMemberIds

    def listTeamMembers_2(self, game: Game) -> List[int]: # TODO: correct naming for teams

        teamMemberIds = []
        mine = self.web2Client.getMine(game['game_id'])
        for teams in mine['defense_team_info']:
            teamMemberIds.append(teams['crabada_id'])
        return teamMemberIds

