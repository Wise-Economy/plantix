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


if __name__ == '__main__':
    unittest.main()
