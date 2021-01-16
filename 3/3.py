import json
import heapq
from dataclasses import dataclass, field

class Node(object):
    
    def __init__(self, name, accessible, coordinates, neighbours):
        self.name = name 
        self.accessible = accessible
        self.coordinates = coordinates
        self.neighbours = neighbours
        self.memory = []
    
    def remove_neighbour(self, neighbour_dict):
        try:
            self.neighbours.remove(neighbour_dict)
            self.memory.append(neighbour_dict)
        except ValueError:
            #print("neighbour not in this node: {}".format(neighbour_dict))
            pass
    
    def restore_neighbours(self):
        self.neighbours.extend(self.memory)
        self.memory = []
    
    @classmethod
    def from_dict(cls, inp_dict):
        return cls(inp_dict["Name"], inp_dict["Accessible"], inp_dict["Coordinates"], inp_dict["Neighbours"])

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
        self.q.sort(reverse=True, key=lambda x: x[0])
    
    def get(self):
        return self.q.pop()
    
    def change_dist(self, name, new_dist):
        self.q_dict[name][0] = new_dist
        self.q.sort(reverse=True, key=lambda x: x[0])
    
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

            # checking for accessibility and adding 5 to weight if not accessible
            if not graph.node_dict[neighbour["Name"]].accessible:
                alt += 5

            try:
                if alt < dist[neighbour["Name"]]:
                    dist[neighbour["Name"]] = alt
                    prev[neighbour["Name"]] = curr_node.name
                    Q.change_dist(neighbour["Name"], alt)
            except KeyError:
                continue

    return dist, prev

def get_path(graph, prev, start_name, end_name, nodes=True):
    try:
        pathlist = [end_name]
        curr = end_name
        while prev[curr] != start_name:
            pathlist.append(prev[curr])
            curr = prev[curr]
        if prev[curr] == start_name:
            pathlist.append(start_name)
        
        if nodes:
            return [graph.node_dict[node_name] for node_name in pathlist[::-1]]
        else:
            return pathlist[::-1]
    except:
        return []

def yen_KSP(graph, start, end, K):

    dist, prev = Dijkstra(graph, start, end) # shortest path

    A = [None for i in range(K)]
    B = []

    A[0] = ([get_path(graph, prev, start.name, end.name, nodes=True), dist[end.name]])

    potential_paths = []

    for k in range(1, K):
        for i in range(len(A[k-1][0])-1):
            
            spur_node = A[k-1][0][i]
            root_path = A[k-1][0][0:i]
            
            neighbour_restore = []
            node_restore = []

            for path, distance in A[0:k]:
                if root_path == path[0:i]:
                    neighbour_dict = [neighbour for neighbour in path[i].neighbours if (neighbour["Name"] == path[i+1].name)]
                    path[i].remove_neighbour(neighbour_dict)
                    path[i+1].remove_neighbour(neighbour_dict)
                    neighbour_restore.append(path[i])
                    neighbour_restore.append(path[i])
                    
            for root_path_node in root_path:
                if root_path_node != spur_node:
                    node_restore.append(root_path_node)
                    graph.nodes.remove(root_path_node)

            spur_path_dist, spur_path_prev = Dijkstra(graph, spur_node, end)
            spur_path_list = [get_path(graph, spur_path_prev, spur_node.name, end.name), spur_path_dist[end.name]]

            total_path = root_path + spur_path_list[0]

            if total_path not in B:
                if not root_path:
                    root_dist = 0
                else:
                    root_dist = dist[root_path[-1].name]
                B.append([total_path, spur_path_list[1] + root_dist])

            #restoring previous graph and node data
            for node in neighbour_restore:
                node.restore_neighbours()
            graph.nodes.extend(node_restore)

        if B == []:
            return "no paths found"

        B.sort(reverse=True, key=lambda x: x[1])
        A[k] = B[0]
        B.pop(0)
    return A


def get_acc_ratio(node_list):
    total = 0
    acc_num = 0
    for node in node_list:
        if node.accessible:
            acc_num += 1
        total += 1

    return acc_num / total

def get_best_path(paths_list):
    '''[[path, dist]]'''
    for i in range(len(paths_list)):
        if get_acc_ratio(paths_list[i][0]) < .5:
            curr_dist = max(paths_list[i][1] * 2, paths_list[i][1] + 5)
            if i == (len(paths_list) - 1):
                print("ran out of options")
                paths_list[i][1] = max(paths_list[i][1] * 2, paths_list[i][1] + 5)
                return paths_list[i]
            if get_acc_ratio(paths_list[i+1][0]) < 0.5:
                multiplier = 2
            else:
                multiplier = 1
            
            if (max(paths_list[i+1][1] * multiplier, paths_list[i+1][1] + 5 * (multiplier-1)) < curr_dist):
                continue
            else:
                paths_list[i][1] = max(paths_list[i][1] * 2, paths_list[i][1] + 5)
                return paths_list[i]
    paths_list[0][1] = max(paths_list[i][1] * 2, paths_list[i][1] + 5)
    return paths_list[0]
                

def findpath_acc(inputfile, inputjson, outfile):

    graph = Graph.from_json(inputjson)

    with open(inputfile, "r") as f:
        for line in f.readlines():
            line = line.strip()
            start_name, end_name = line.split(",")
            
            A = yen_KSP(graph, graph.node_dict[start_name], graph.node_dict[end_name], 100)

            best_path = get_best_path(A)
            with open(outfile, "a") as f:
                f.write("{}, {}\n".format(str([node.name for node in best_path[0]]).replace("'", "").replace("[", "").replace("]", ""), str(best_path[1])))


if __name__ == "__main__":
    findpath_acc("3.in", "3.json", "3.out")