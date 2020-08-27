import os
import json

from typing import Any as Json
from plant_expert import PlantExpert


class PlantixCommunityService(object):
    """Simulates the Plantix Community API in-memory and in-process.
    """
    COMMUNITY_CACHE = json.load(open(
        os.path.join(os.path.dirname(__file__), "community.json")
    ))

    def get(self, uid: str) -> Json:
        """GET https://plantix.net/community/api/experts/:uid
        """
        plants, following = self.COMMUNITY_CACHE[uid]
        return PlantExpert(uid, plants, following)
