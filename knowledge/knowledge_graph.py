import networkx as nx

kg = nx.DiGraph()

def create_relationship(kg, subject, predicate, obj):
    kg.add_node(subject)
    kg.add_node(obj)
    kg.add_edge(subject, obj, relation=predicate)