import networkx as nx
import random
import pickle


def createNetwork(file):
    return nx.read_edgelist(file, create_using=nx.Graph(), nodetype=int)


def networkPreprocessing(G, labels):
    """
        Define some labels and randomly assign them to the nodes in the network.
    """
    # Assign labels to each node
    for node in G.nodes():
        label = random.choice(labels)
        G.nodes[node]["label"] = label

    # Add random weights to the edges
    for u, v in G.edges():
        weight = random.randint(1, 100)
        G[u][v]['weight'] = weight

    # Add random weights to unconnected edges
    for u in G.nodes():
        for v in G.nodes():
            if u != v and not G.has_edge(u, v):
                weight = random.randint(1, 100)
                G.add_edge(u, v, weight=weight)


def removeEdges(G):
    # Remove edges between nodes with the same label
    for u in G.nodes():
        for v in G.nodes():
            if u != v and G.nodes[u]['label'] == G.nodes[v]['label'] and G.has_edge(u, v):
                G.remove_edge(u, v)


def createProjectNetwork(list):
    project = nx.Graph()
    project.add_edges_from(list)
    return project


def saveNetwork(G):
    pickle.dump(G, open('network_data.pkl', 'wb'))


def createRandomTeam(G, label_to_filter, team_size):
    # Initialize a subgraph
    subgraph = nx.Graph()

    nodes_with_label = [node for node, data in G.nodes(
        data=True) if 'label' in data and data['label'] == label_to_filter]

    # Randomly select team_size nodes from the list
    if len(nodes_with_label) >= team_size:
        team_nodes = random.sample(nodes_with_label, team_size)
    else:
        print("Not enough nodes with the specified label to form a team.")
        team_nodes = []

    # Add the selected team nodes to the team subgraph
    for node in team_nodes:
        subgraph.add_node(node, label=label_to_filter)

    return subgraph


def getSubgraph(G, teams):
    """
        This is a subgraph of all the people across the teams. 
    """
    all_nodes = []
    for team in teams:
        team_nodes = [node for node in team.nodes]
        all_nodes.extend(team_nodes)

    return G.subgraph(all_nodes)


def getNextBest(node, network, project_network):
    """
        This subroutine returns the best nodes in the adjacent node 
    """
    node_label = network.nodes[node]['label']
    neighbors = list(project_network.neighbors(node_label))
    list_of_selected_nodes = []
    try:
        for label in neighbors:
            labeled_neighbors = [n for n in network.neighbors(
                node) if network.nodes[n]['label'] == label]
            for u in labeled_neighbors:
                max_weight = 0
                selected_node = None
                if network[node][u]['weight'] > max_weight:
                    max_weight = network[node][u]['weight']
                    selected_node = u
            list_of_selected_nodes.append(selected_node)
        # visited_array.append(node)
    except:
        print("Node has no neighbors")

    return list_of_selected_nodes


def getCoordinator(network, project_network):

    key = random.choice(list(network.nodes))
    visited_array = []
    first_list = getNextBest(key, network, project_network)
    coordinators = set(first_list)
    labels = set([network.nodes[n]['label'] for n in first_list])
    visited_array.append(key)
    while len(coordinators) < len(project_network):
        for i in list(network.nodes):
            if i not in visited_array and network.nodes[i]['label'] not in list(labels):
                key = i
                visited_array.append(key)
                break
        new_list = getNextBest(key, network, project_network)
        labels = labels.union(set([network.nodes[n]['label'] for n in new_list])) # Update 
        coordinators = coordinators.union(set(new_list))

    return coordinators