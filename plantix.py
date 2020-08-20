import os
import json

from typing import List, Text as String
from dataclasses import dataclass


@dataclass
class PlantExpert(object):
    """
    Represents a plantix community expert.
    
    Each expert has a unique id, a list of plants
    they can give advice on and a list of other
    expert uid-s they follow.
    """	
    uid: String
    plants: List[String]
    following: List[String]


class PlantixApiClient(object):
    """
    SDK for our Plantix Community API.
    """

    COMMUNITY_SERVICE = json.load(open(
        os.path.join(os.path.dirname(__file__), "community.json")
    ))

    def __init__(self, file_path=None):
        if file_path is not None:
            self.COMMUNITY_SERVICE = json.load(open(file_path))

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

        reachable_experts = set()
        self.dfs(reachable_nodes=reachable_experts, start=start,)
        reachable_experts.remove(start)

        plant_topic_count_dict = self.generate_plant_topic_count_dict(
            experts=reachable_experts,
        )
        print(plant_topic_count_dict)
        top_n_plant_topics = sorted(
            plant_topic_count_dict,
            key=plant_topic_count_dict.get,
            reverse=True,
        )[:n]
        return tuple(top_n_plant_topics)

    def dfs(self, reachable_nodes: set, start: String) -> set:
        """
        Run the depth first search algorithm to identify all
        the reachable nodes in a graph from the given start "expert" node.

        :param reachable_nodes: Set of all nodes reachable from the start
                Initial value will be set() -> empty set.
        :param start: uid of the expert "Node" from which the depth first search starts.
        :return: Set of nodes that are reachable from start node.
        """
        if start not in reachable_nodes:
            expert = self.fetch(start)
            reachable_nodes.add(start)
            for neighbour in expert.following:
                self.dfs(reachable_nodes, neighbour)

        return reachable_nodes

    def generate_plant_topic_count_dict(self, experts: set) -> dict:
        """
        This function returns dict with plant topics covered and the number of experts
        per topic among the given set of experts.

        :param experts: Set of experts.
        :return: Dict containing plant topics(as key) covered among the experts and
                 their popularity count(as value which is the number of experts
                 available per topic)
        """
        plant_topic_count_dict = {}
        for expert_id in experts:
            expert = self.fetch(uid=expert_id)
            for plant_topic in expert.plants:
                if plant_topic in plant_topic_count_dict:
                    plant_topic_count_dict[plant_topic] += 1
                else:
                    plant_topic_count_dict[plant_topic] = 1
        return plant_topic_count_dict


if __name__ == '__main__':
    print(PlantixApiClient().find_topics(start="0", n=3))