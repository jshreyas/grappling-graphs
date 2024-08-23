import json
from typing import List

from sng_demo.database.models import Node, Relationship


def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)


def populate_database(db, path):
    file = open(path)
    lines = file.readlines()
    file.close()
    for line in lines:
        if len(line.strip()) != 0 and line[0] != '/':
            db.execute_query(line)

def get_transitions(db):
    command = "MATCH (n1)-[e:TRANSITION]-(n2) RETURN n1,n2,e;"
    transitions = db.execute_and_fetch(command)

    transition_objects = []
    for transition in transitions:
        data = transition['e'].properties
        data["target"] = transition['n2'].properties["id"]
        data["source"] = transition['n1'].properties["id"]
        transition_objects.append(data)
    return transition_objects

def get_frame(db, id) -> Node:
    command = f"MATCH (n:Frame) WHERE n.id={id} RETURN n;"
    frames = db.execute_and_fetch(command)
    for frame in frames:
        return frame['n'].properties

def get_frames(db) -> List[Node]:
    command = "MATCH (n:Frame) RETURN n;"
    frames = db.execute_and_fetch(command)

    frame_objects = []
    for frame in frames:
        frame_objects.append(frame['n'].properties)
    return frame_objects

def get_ggraph(db):

    data = {"links": get_transitions(db), "nodes": get_frames(db)}
    return data

def get_users(db) -> List[Node]:
    command = "MATCH (n:User) RETURN n;"
    users = db.execute_and_fetch(command)

    user_objects = []
    for user in users:
        u = user['n']
        user_objects.append(u.properties)
    return user_objects

def get_user(db, id) -> Node:
    command = f"MATCH (n:User) WHERE n.id={id} RETURN n;"
    user = db.execute_and_fetch(command)
    for uu in user:
        u = uu['n']
        return u.properties

def get_relationships(db):
    command = "MATCH (n1)-[e:FRIENDS]-(n2) RETURN n1,n2,e;"
    relationships = db.execute_and_fetch(command)

    relationship_objects = []
    for relationship in relationships:
        n1 = relationship['n1']
        n2 = relationship['n2']
        data = {"userOne": n1.properties['name'],
                "userTwo": n2.properties['name']}
        relationship_objects.append(data)

    return relationship_objects


def get_graph(db):
    command = "MATCH (n1)-[e:FRIENDS]-(n2) RETURN n1,n2,e;"
    relationships = db.execute_and_fetch(command)

    bink_objects = []
    link_objects = []
    node_objects = []
    added_nodes = []
    for relationship in relationships:
        e = relationship['e']
        print("start")
        print(e.nodes)
        print(e.id)
        n1 = relationship['n1']
        if not (n1.properties['id'] in added_nodes):
            data = {"id": n1.properties['id'], "name": n1.properties['name']}
            node_objects.append(data)
            added_nodes.append(n1.properties['id'])

        n2 = relationship['n2']
        if not (n2.properties['id'] in added_nodes):
            data = {"id": n2.properties['id'], "name": n2.properties['name']}
            node_objects.append(data)
            added_nodes.append(n2.properties['id'])
        
        link = {"source": n1.properties['id'], "target": n2.properties['id']}
        
        bink = [n1.properties['id'], n2.properties['id']]
        print(f"blah: {bink}")
        print(f"link: {link}")
        print("end")
        link_objects.append(link)
        bink_objects.append(bink)
    data = {"links": link_objects, "nodes": node_objects}
    # data = {"links": bink_objects, "nodes": node_objects}

    return data
