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
'''
class tempQueue():
    def __init__(self):
        self.q = []
        self.q_dict = {}
    
    def put(self, thing):
        thing: [distance, node]
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
'''    
class Heap():
    def __init__(self):
        self.heap = []
        self.dic = {}

    def __setitem__(self,key,dist):
        #feed in format ^^ PLZ READ
        if key in self.dic:
            disc = self.dic.pop(key)
            self.heap.pop(disc[2])
            self._heapify()
        eminem = [dist, key, len(self.heap)] # a rapper...wrapper... get it?
        self.dic[key] = eminem
        self.heap.append(eminem)
        #self._bubbly(len(self.heap)-1)
        self._heapify()
        
    def _reindex(self):
        for i in range(len(self.heap)):
                self.heap[i][2] = i
                self.dic[self.heap[i][1]] = self.heap[i]

    def empty(self):
        if self.heap == []:
            return 1
        return 0

    def _bubbly(self,i):
        h = self.heap
        while i:
            parent = (i-1) >> 1
            if h[parent][0] >= h[i][0]:
                self._swap(i,parent)
            i = parent
        
    def _swap(self,i,j):
        h = self.heap
        h[i],h[j] = h[j],h[i]
        
        h[i][2] = i
        h[j][2] = j
        
    def _heapify(self):
        h = self.heap
        n = len(self.heap) - 1
        i = 0
        while i <= n:
            left = 2*i + 1
            right = (i+1)*i
            if left <= n and h[left][0] < h[i][0]:
                mini = left
            else:
                mini = i
            if right <= n and h[right][0]< h[i][0]:
                mini = right 
            if mini == i:
                break
            self._swap(i,mini)
            i = mini
        
        for i in range(len(self.heap)):
                self.heap[i][2] = i
                self.dic[self.heap[i][1]] = self.heap[i]
        
    
    def pop(self):
       h = self.heap
       d = self.dic
       value = h.pop(0)
       d.pop(value[1])
       self._heapify()
       
       return value

    def change_dist(self, key, dist):
        h = self.heap
        d = self.dic
        if key not in d:
            return
        d[key][0] = dist
        h[d[key][2]][0] = dist
        self._heapify()
        
    

def Dijkstra(graph, start, end):

    dist = {} # dictionary of distances from start
    prev = {} # dictionary of best path, probably need to change
    
    dist[start.name] = 0 # distance from start to start = 0
    Q = Heap() # creating heap
    for node in graph.nodes:
        if node.name != start.name:
            dist[node.name] = float("inf")
            prev[node.name] = None
        Q[node.name] = float('inf')
    
    while not Q.empty():
        curr = Q.pop()
        curr_dist, curr_node = curr[0], graph.node_dict[curr[1]]

        for neighbour in curr_node.neighbours:
            alt = dist[curr_node.name] + neighbour["Distance"]

            # checking for accessibility and adding 5 to weight if not accessible
            if not graph.node_dict[neighbour["Name"]].accessible:
                alt += 5

            if alt < dist[neighbour["Name"]]:
                dist[neighbour["Name"]] = alt
                prev[neighbour["Name"]] = curr_node.name
                Q.change_dist(neighbour["Name"], alt)  

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

    A = []

    A[0] = [get_path(graph, prev, start.name, end.name, nodes=True), dist[end.name]]

    potential_paths = []

    for k in range(1, K+1):
        for i in range(len(A[k-1][0])-1):
            
            spur_node = A[k-1][0][i]
            root_path = A[k-1][0][0:i]
            
            for path, distance in A:
                if root_path == path[0:i]:
                    pass


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
            print(get_path(graph, prev, start_name, end_name, nodes=False), dist[end_name])


if __name__ == "__main__":
    findpath_acc("3.in", "3.json")
    '''
    q = Heap()
    q['Yonge'] = 3
    q['Dundas'] = 6
    q['College'] = 2
    q['whassup'] = 4
    q['pepehands'] = float('inf')
    print(q.heap)
    """
    a = q.pop()
    print(a)
    print(q.heap)
    a = q.pop()
    print(a)
    print(q.heap)
    """
    q.change_dist('College',80)
    print(q.heap)
    print(q.dic)
    '''