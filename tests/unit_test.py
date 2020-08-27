import unittest
import json
import os

from plant_expert import PlantExpert
from tests.plantix_test_helper import PlantixApiClientForTesting
from helper import generate_plant_experts_topic_count_dict
from depth_first_search import depth_first_search_iterative


class PlantixApiClientUnitTest(unittest.TestCase):

    def _initiate_plantix_api_client(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "community.json")
        self.plantix_api_client = PlantixApiClientForTesting(file_path=self.file_path)
        self.plantix_api_client._generate_network()

    def test_json_load(self):
        self._initiate_plantix_api_client()
        community_json = json.load(open(self.file_path))
        assert self.plantix_api_client.COMMUNITY_SERVICE == community_json

    def test_fetch(self):
        self._initiate_plantix_api_client()
        community_json = json.load(open(self.file_path))
        uid = "0"
        expert = PlantExpert(
            uid=uid,
            plants=community_json[uid][0],
            following=community_json[uid][1],
        )
        assert self.plantix_api_client.fetch("0") == expert

    def test_depth_first_search_iterative(self):
        self._initiate_plantix_api_client()

        # Node "3" is not reachable
        for expert in ["0", "1", "2"]:
            reachable_nodes = depth_first_search_iterative(
                network=self.plantix_api_client.NETWORK,
                start=expert,
            )
            assert reachable_nodes == set(["0", "1", "2"])
            assert "3" not in reachable_nodes

        # All nodes are reachable from "3"
        reachable_nodes = depth_first_search_iterative(
            network=self.plantix_api_client.NETWORK,
            start="3",
        )
        assert reachable_nodes == set(["0", "1", "2", "3"])

    def test_generate_plant_topic_count_dict(self):
        self._initiate_plantix_api_client()
        plant_topic_count_dict = generate_plant_experts_topic_count_dict(
            network=self.plantix_api_client.NETWORK,
            experts=set(["3"]),
        )
        assert plant_topic_count_dict == {"asparagus": 1, "beetroot": 1}
        plant_topic_count_dict = generate_plant_experts_topic_count_dict(
            network=self.plantix_api_client.NETWORK,
            experts=set(["2", "1"]),
        )
        assert plant_topic_count_dict == {"pear": 2, "apple": 1}


if __name__ == '__main__':
    unittest.main()
