from plantix import PlantixApiClient
from plant_expert import PlantExpert
import os
from tests.plantix_test_helper import PlantixApiClientForTesting
import unittest


class PlantixApiClientIntegrationTest(unittest.TestCase):

    def _initiate_plantix_api_client(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "community.json")
        self.plantix_api_client = PlantixApiClientForTesting(file_path=self.file_path)

    def test_find_topics(self):
        """
            "beetroot" & "asparagus" never appear in this list
            as the expert "3" is not followed by anyone
        """
        self._initiate_plantix_api_client()

        result = self.plantix_api_client.find_topics(start="0", n=2)
        assert result == ('pear', 'apple')

        result = self.plantix_api_client.find_topics(start="1", n=2)
        assert result == ('pear', 'apple')

        result = self.plantix_api_client.find_topics(start="2", n=2)
        assert set(result) == set(['pear', 'apple'])

        result = self.plantix_api_client.find_topics(start="3", n=2)
        assert result == ('pear', 'apple')
