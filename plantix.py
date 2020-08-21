import os
import json

from typing import Text as String, Dict

from depth_first_search import depth_first_search_iterative
from helper import generate_plant_experts_count_dict
from plant_expert import PlantExpert


class PlantixApiClient(object):
    """
    SDK for our Plantix Community API.
    """

    COMMUNITY_SERVICE = json.load(open(
        os.path.join(os.path.dirname(__file__), "community.json")
    ))

    NETWORK: Dict[str, PlantExpert] = {}

    def fetch(self, uid: String) -> PlantExpert:
        """
        Fetch a plant expert by uid.
        
        @param uid: ID of the expert to fetch
        @raise KeyError: if no such uid exists
        """
        plants, following = self.COMMUNITY_SERVICE[uid]
        return PlantExpert(uid, plants, following)

    def find_topics(self, start: String, n: int) -> tuple:
        """
        Find the 'n' most covered plant topics in the network of experts reachable for the expert
        with uid=start.

        :param start: ID of the "start" expert to calculate the n
                      most covered plants in the network of experts
                      reachable for this expert.
        :param n: Number of most covered plants in the network of experts reachable for this expert.
        :return: Tuple with 'n' most covered plants in the network.
        """

        self._generate_network()

        reachable_experts = depth_first_search_iterative(
            network=self.NETWORK,
            start=start,
        )

        plant_experts_count_dict = generate_plant_experts_count_dict(
            network=self.NETWORK,
            experts=reachable_experts,
        )
        top_n_plant_topics = sorted(
            plant_experts_count_dict,
            key=plant_experts_count_dict.get,
            reverse=True,
        )[:n]
        return tuple(top_n_plant_topics)

    def _generate_network(self):
        for uid in self.COMMUNITY_SERVICE.keys():
            self.NETWORK[uid] = self.fetch(uid=uid)


if __name__ == '__main__':
    print(PlantixApiClient().find_topics(start="0", n=3))
