from plantix import PlantixApiClient
import json


class PlantixApiClientForTesting(PlantixApiClient):

    def __init__(self, file_path=None):
        if file_path is not None:
            self.COMMUNITY_SERVICE = json.load(open(file_path))


