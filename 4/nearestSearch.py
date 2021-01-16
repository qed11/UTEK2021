from pathFinder import find_shortest_path
import random

class nearestSearch:

    '''
    nearestSearch: class that performs nearest neighbour search with Djikstra's Algorithm
    '''

    def __init__(self, nodeData):
        '''
        :param map (dict):  json data to load

        Initialized parameters:
        path (list): List containing path followed for tsp
        unvisited (list): List containing stations to visit for tsp
        totalCost (int): Value for the total distance followed
        '''

        self.nodeData = nodeData
        self.totalCost = 0
        self.path = []
        self.unvisited = None

    def step(self, node):
        '''
        Method that applies one iteration of Djikstras for nearest neighbour search

        :param node (string): Name of current station
        :return (string): Name of nearest station to visit
        '''

        minVal = 100
        extendPath = None
        for unvisited in self.unvisited:

            # Apply Djikstras to find shortest path to a node of interest
           path_out = find_shortest_path(self.nodeData, node, unvisited)
           distance = path_out[-1]
           path = path_out[:-1]
           if distance < minVal:
               minVal = distance
               closeVisited = unvisited
               extendPath = path[0]

        self.path.extend(extendPath[:-1]) # Include path minus target location (redundant on next iteration)
        self.unvisited.remove(closeVisited)
        self.totalCost += minVal
        return extendPath[-1]

    def searchGraph(self):
        '''
        Method that uses Djikstras to find approximate solution to travelling salesman problem over select stations

        :return (int, list): Total distance travelled and list of stations travelled for said distance
        '''

        # Select random starting node
        startingNode = self.unvisited[random.randint(0, len(self.unvisited)-1)]
        self.unvisited.remove(startingNode)
        currNode = startingNode

        while len(self.unvisited) != 0:
            currNode = self.step(currNode)

        # Traverse back to original node in the end
        path_out = find_shortest_path(self.nodeData, currNode, startingNode)
        self.totalCost += path_out[-1]
        self.path.extend(path_out[:-1][0])

        return self.totalCost, self.path
