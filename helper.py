from PlantixCommunityService import PlantixCommunityService


def generate_plant_experts_topic_count_dict(experts: set) -> dict:
    """
    This function returns dict with plant topics covered and the number of experts
    per topic among the given set of experts.

    :param network: Dict of network of plant experts with "uid" as the keys and values are the
                    corresponding PlantExpert objects.
    :param experts: Set of experts.
    :return: Dict containing plant topics(as key) covered among the experts and
             their popularity count(as value which is the number of experts
             available per topic)
    """
    network = PlantixCommunityService()
    plant_topic_count_dict = {}
    for expert_id in experts:
        expert = network.get(expert_id)
        for plant_topic in expert.plants:
            if plant_topic in plant_topic_count_dict:
                plant_topic_count_dict[plant_topic] += 1
            else:
                plant_topic_count_dict[plant_topic] = 1

    print(plant_topic_count_dict)
    return plant_topic_count_dict
