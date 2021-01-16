import random

class nearestSearch:

    def __init__(self, nodeDict):
        self.nodeDict = nodeDict
        self.unvisited = [node for node in nodeDict.keys()]
        self.totalCost = 0
        self.visited = []
        self.visitedScores = []
        self.path = []
        self.btracking_counter = 0

    def step(self, node):
        minVal = 100
        minStation = None
        for neighbour in node["Neighbours"]:
            if neighbour["Name"] in self.unvisited:
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

    def reset(self):
        self.unvisited = [node for node in self.nodeDict.keys()]
        self.totalCost = 0
        self.visited = []
        self.visitedScores = []
        self.path = []
        self.btracking_counter = 0

    def searchGraph(self):
        bestScore = 300
        bestPath = None
        for _ in range(0, len(self.nodeDict)):
            startingNode = list(self.nodeDict.keys())[random.randint(0, len(self.nodeDict))]
            currNode = startingNode
            while len(self.unvisited) != 0:
                # Option 1
                if currNode == None:
                    self.btracking_counter += 1
                    currNode = self.visited.pop(0)
                    self.totalCost += self.visitedScores.pop(0)
                    self.path.append(currNode)
                currNode = self.step(self.nodeDict[currNode])
            if bestScore > self.totalCost:
                bestScore = self.totalCost
                bestPath = self.path
                bestBT = self.btracking_counter
            self.reset()
        print("Best case - back tracked {} times".format(bestBT))
        return bestScore, bestPath, bestBT
