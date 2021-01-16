import matplotlib.pyplot as plt
import json

with open('4.json') as f:
    data = json.load(f)

nodeList = data["Nodes"]
xList = [node["Coordinates"][0] for node in nodeList]
yList = [node["Coordinates"][1] for node in nodeList]
label = [node["Name"] for node in nodeList]

fig, ax = plt.subplots()
ax.scatter(xList, yList)

for i, v in enumerate(label):
    ax.annotate(v, (xList[i], yList[i]))

plt.plot()
plt.show()