from dataclasses import dataclass
from typing import Text as String, List


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