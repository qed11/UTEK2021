import json
from nearestSearch import nearestSearch

with open('4.json') as f:
    data = json.load(f)

nodeList = data["Nodes"]
processDict = {}
for node in nodeList:
    processDict[node["Name"]] = node
    # Preprocessed because a default list sucks

sol = nearestSearch(processDict)
cost, path, _ = sol.searchGraph()
print("Cost: {} Visited Path: {}".format(cost, path))