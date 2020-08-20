import os
import json

from typing import List, Text as String
from dataclasses import dataclass


@dataclass
class PlantExpert(object):
    """Represents a plantix community expert.
    
    Each expert has a unique id, a list of plants
    they can give advice on and a list of other
    expert uid-s they follow.
    """	
    uid: String
    plants: List[String]
    following: List[String]


class PlantixApiClient(object):
    """SDK for our Plantix Community API.
    """

    COMMUNITY_SERVICE = json.load(open(
        os.path.join(os.path.dirname(__file__), "community.json")
    ))

    def __init__(self, file_path=None):
        if file_path is not None:
            self.COMMUNITY_SERVICE = json.load(open(file_path))

    def fetch(self, uid: String) -> PlantExpert:
        """Fetch a plant expert by uid.
        
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

        reachable_experts_from_start = self.fetch(start).following
        plant_topic_count_dict = {}
        for expert_id in reachable_experts_from_start:
            expert = self.fetch(expert_id)
            expert_neighbors = expert.following

            # Update the plant_topic counter
            _update_plant_topic_count_dict(expert, plant_topic_count_dict)

            # Append experts to reachable experts if not present.
            for expert_neighbor in expert_neighbors:
                if expert_neighbor not in reachable_experts_from_start:
                    reachable_experts_from_start.append(expert_neighbor)

        # get the top n available plant topics from the dict
        top_n_plant_topics = sorted(
            plant_topic_count_dict,
            key=plant_topic_count_dict.get,
            reverse=True,
        )[:n]
        return tuple(top_n_plant_topics)


def _update_plant_topic_count_dict(expert, plant_topic_count_dict):
    for plant_topic in expert.plants:
        if plant_topic in plant_topic_count_dict:
            plant_topic_count_dict[plant_topic] += 1
        else:
            plant_topic_count_dict[plant_topic] = 1


if __name__ == '__main__':
    print(PlantixApiClient().find_topics(start="0", n=3))