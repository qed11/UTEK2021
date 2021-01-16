import random

class nearestSearch:

    def __init__(self, nodeList):
        self.unvisited = nodeList
        self.nodeList = nodeList
        self.unvisited = [node["Name"] for node in nodeList]
        self.totalCost = 0
        self.visited = []
        self.visitedScores = []
        self.path = []

    def step(self, node):
        minVal = 100
        minStation = None
        for neighbour in node["Neighbours"]:
            if neighbour["Name"] not in self.visited:
               if neighbour["Distance"] < minVal:
                   minVal = neighbour["Distance"]
                   minStation = neighbour["Name"]

        if minStation == None:
            return minStation
        self.visited.append(minStation)
        self.visitedScores.append(minVal)
        self.path.append(minStation)
        self.unvisited.remove(minStation)
        self.totalCost += minVal
        return minStation

    def searchGraph(self):
        startingNode = random.randint(0, len(self.nodeList))
        startingName = self.nodeList[startingNode]["Name"]
        currNode = startingNode
        while len(self.unvisited) != 0:
            # Option 1
            if currNode == None:
                currNode = self.visited.pop(0)
                self.totalCost += self.visitedScores.pop(0)
                self.path.append(currNode)
            currNode = self.step(self.nodeList[currNode])
        return self.totalCost, self.path
