from typing import Dict, Text as String

from plant_expert import PlantExpert


def depth_first_search_recursive(network: Dict[str, PlantExpert], reachable_nodes: set, start: String) -> set:
    """
    Run the depth first search algorithm to identify all
    the reachable nodes in a graph from the given start "expert" node.

    This is a recursive DFS implementation. The memory implications may
    be bad as python doesn't do "tail call optimization".

    :param network: Dict of network of plant experts with "uid" as the keys and values are the
                    corresponding PlantExpert objects.
    :param reachable_nodes: Set of all nodes reachable from the start
            Initial value will be set() -> empty set.
    :param start: uid of the expert "Node" from which the depth first search starts.
    :return: Set of nodes that are reachable from start node.
    """
    if start not in reachable_nodes:
        expert = network.get(start)
        reachable_nodes.add(start)
        for neighbour in expert.following:
            depth_first_search_recursive(reachable_nodes, neighbour)

    return reachable_nodes


def depth_first_search_iterative(network: Dict[str, PlantExpert], start: String) -> set:
    """
    Run the depth first search algorithm to identify all
    the reachable nodes in a graph from the given start "expert" node.

    This is a iterative DFS algorithm.

    :param network: Dict of network of plant experts with "uid" as the keys and values are the
                    corresponding PlantExpert objects.
    :param start: uid of the expert "Node" from which the depth first search starts.
    :return: Set of nodes that are reachable from start node.
    """

    list_ = []
    reachable_nodes = set()
    list_.append(start)
    while list_:
        try:
            current_expert_node = list_.pop()
            if current_expert_node not in reachable_nodes:
                reachable_nodes.add(current_expert_node)
                expert = network.get(current_expert_node)
                for following_expert_node in expert.following:
                    list_.append(following_expert_node)
        except TypeError:
            x = 1
            y = 2
    return reachable_nodes
