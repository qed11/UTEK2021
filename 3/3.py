import json
import heapq
from dataclasses import dataclass, field

class Node(object):
    
    def __init__(self, name, accessible, coordinates, neighbours):
        self.name = name 
        self.accessible = accessible
        self.coordinates = coordinates
        self.neighbours = neighbours
    
    @classmethod
    def from_dict(cls, inp_dict):
        return cls(inp_dict["Name"], inp_dict["Accessible"], inp_dict["Coordinates"], inp_dict["Neighbours"])

class Path(object):

    def __init__(self):
        pass

    def acc_r_(self):
        pass

class Graph(object):
    '''using linked list rep'''
    def __init__(self, nodes):
        self.nodes = nodes
        self.node_dict = {node.name:node for node in nodes}

    @classmethod
    def from_json(cls, path2json):
        node_list = []
        with open(path2json, "r") as f:
            graph_dist = json.load(f)
        for node in graph_dist["Nodes"]:
            node_list.append(Node.from_dict(node))
        
        return cls(node_list)

class tempQueue():
    def __init__(self):
        self.q = []
        self.q_dict = {}
    
    def put(self, thing):
        ''' thing: [distance, node]'''
        self.q.append(thing)
        self.q_dict[thing[1].name] = thing
        self.q.sort(key=lambda x: x[0])
    
    def get(self):
        return self.q.pop()
    
    def change_dist(self, name, new_dist):
        self.q_dict[name][0] = new_dist
        self.q.sort(key=lambda x: x[0])
    
    def empty(self):
        return not bool(len(self.q))

def Dijkstra(graph, start, end):

    dist = {} # dictionary of distances from start
    prev = {} # dictionary of best path, probably need to change
    
    dist[start.name] = 0 # distance from start to start = 0
    Q = tempQueue() # creating priority queue TODO
    for node in graph.nodes:
        if node.name != start.name:
            dist[node.name] = float("inf")
            prev[node.name] = None
        Q.put([dist[node.name], node])

    while not Q.empty():
        curr = Q.get()
        curr_dist, curr_node = curr[0], curr[1]
        
        for neighbour in curr_node.neighbours:
            alt = dist[curr_node.name] + neighbour["Distance"]

            if alt < dist[neighbour["Name"]]:
                dist[neighbour["Name"]] = alt
                prev[neighbour["Name"]] = curr_node
                Q.change_dist(neighbour["Name"], alt)  

    return dist, prev

def findpath_acc(inputfile, inputjson):

    graph = Graph.from_json(inputjson)

    with open(inputfile, "r") as f:
        for line in f.readlines():
            line = line.strip()
            start_name, end_name = line.split(",")
            print("Starting at: {} Ending at {}".format(start_name, end_name))
            dist, prev = Dijkstra(graph, graph.node_dict[start_name], graph.node_dict[end_name])
            
            '''
            for key, value in prev.items():
                try:
                    print(key, value.name)
                except:
                    #print(key, None)
                    pass
            '''
            print(dist)
            try:
                pathlist = [end_name]
                curr = end_name
                while prev[curr].name != start_name:
                    pathlist.append(prev[curr].name)
                    curr = prev[curr].name
                if prev[curr].name == start_name:
                    pathlist.append(start_name)
                print(pathlist, dist[end_name])
            except:
                print("xd no path found")


if __name__ == "__main__":
    findpath_acc("3.in", "3.json")