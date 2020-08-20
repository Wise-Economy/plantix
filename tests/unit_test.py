import unittest
from plantix import PlantixApiClient, PlantExpert
import json
import os


class PlantixApiClientUnitTest(unittest.TestCase):

    def _initiate_plantix_api_client(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "community.json")
        self.plantix_api_client = PlantixApiClient(file_path=self.file_path)

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

    def test_dfs(self):
        self._initiate_plantix_api_client()
        reachable_nodes = set()

        # Node "3" is not reachable
        for i in ["0", "1", "2"]:
            reachable_nodes = self.plantix_api_client.dfs(reachable_nodes, "1")
            assert reachable_nodes == set(["0", "1", "2"])
            assert "3" not in reachable_nodes

        # All nodes are reachable from "3"
        reachable_nodes = set()
        reachable_nodes = self.plantix_api_client.dfs(reachable_nodes, "3")
        print(reachable_nodes)
        assert reachable_nodes == set(["0", "1", "2", "3"])

    def test_generate_plant_topic_count_dict(self):
        self._initiate_plantix_api_client()
        plant_topic_count_dict = self.plantix_api_client.generate_plant_topic_count_dict(
            experts=set(["3"]),
        )
        assert plant_topic_count_dict == {"asparagus": 1, "beetroot": 1}
        plant_topic_count_dict = self.plantix_api_client.generate_plant_topic_count_dict(
            experts=set(["2", "1"]),
        )
        assert plant_topic_count_dict == {"pear": 2, "apple": 1}


if __name__ == '__main__':
    unittest.main()
