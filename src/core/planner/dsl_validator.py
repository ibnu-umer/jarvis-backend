def validate_graph(graph: dict, available_actions: set):
    tg = graph["task_graph"]
    nodes = tg["nodes"]

    if tg["entry"] not in nodes:
        raise ValueError("Invalid entry node")

    
    for node_id, node in nodes.items():

        # check the action node with the avialable actions
        if node["type"] == "action":
            if node["controller"] not in available_actions:
                raise ValueError(f"Unknown controller: {node['controller']}")
