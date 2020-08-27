from typing import Text as String

from PlantixCommunityService import PlantixCommunityService


def depth_first_search_recursive(reachable_nodes: set, start: String) -> set:
    """
    Run the depth first search algorithm to identify all
    the reachable nodes in a graph from the given start "expert" node.

    This is a recursive DFS implementation. The memory implications may
    be bad as python doesn't do "tail call optimization".

    :param reachable_nodes: Set of all nodes reachable from the start
            Initial value will be set() -> empty set.
    :param start: uid of the expert "Node" from which the depth first search starts.
    :return: Set of nodes that are reachable from start node.
    """
    network = PlantixCommunityService()
    if start not in reachable_nodes:
        expert = network.get(start)
        reachable_nodes.add(start)
        for neighbour in expert.following:
            depth_first_search_recursive(reachable_nodes, neighbour)

    return reachable_nodes


def depth_first_search_iterative(start: String) -> set:
    """
    Run the depth first search algorithm to identify all
    the reachable nodes in a graph from the given start "expert" node.

    This is a iterative DFS algorithm.

    :param start: uid of the expert "Node" from which the depth first search starts.
    :return: Set of nodes that are reachable from start node.
    """

    stack = [start]
    reachable_nodes = set()
    network = PlantixCommunityService()
    while stack:
        current_expert_node = stack.pop()
        if current_expert_node not in reachable_nodes:
            reachable_nodes.add(current_expert_node)
            expert = network.get(current_expert_node)
            for following_expert_node in expert.following:
                stack.append(following_expert_node)
    return reachable_nodes
