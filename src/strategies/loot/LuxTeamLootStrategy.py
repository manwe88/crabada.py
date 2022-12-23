from typing import Any, List
from src.libs.CrabadaWeb2Client.types import Game, Team
from src.strategies.loot.LootStrategy import LootStrategy
from src.helpers.General import firstOrNone, secondOrNone, thirdOrNone, fourthOrNone
import time


class LuxTeamLootStrategy(LootStrategy):
    """
    Looting strategy that chooses the mine with the lowest
    defense points.

    Takes the list of attackable mines from the web2 endpoints,
    which means it is SLOW and will be unlikely to ever succeed
    """

    def query(self, team: Team) -> dict[str, Any]:
        return {
            "can_loot": 1,
            "status": "open",
            "looter_address": team["owner"],
            "limit": self.minesToFetch,
            "orderBy": 'game_id',
            "order": 'desc',
        }

    def mine(self, team: Team, list: List[Game]) -> Game:
        attackableMines = [m for m in list if m['faction'] == 'ORE']
        if len(attackableMines) == 0:
            return None
        # sortedAttackableMines = sorted(attackableMines, key=lambda m: (m['defense_point'], m['defense_mine_point']))
        sortedAttackableMines = attackableMines

        return fourthOrNone(sortedAttackableMines)