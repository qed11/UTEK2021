import json

def myfunc(c):
    return c[1]

f = open('1b.json', 'r')
paths = json.load(f)
sorts = []
f.close()

for i in paths['Paths']:
    access = 0
    #print(i['PathName'])
    stations = i['Nodes']
    length = len(stations)
    for j in range(length):
        if stations[j]['Accessible'] == True:
            access += 1
    non = length - access
    sorts.append([i['PathName'],access/non])

sorts.sort(reverse = True,key=myfunc)

k = 3
writer = open('1b.out','w')
for i in range(k):
    if i != k-1:
        writer.write(sorts[i][0])
        writer.write(', ')
    else:
        writer.write(sorts[i][0])
