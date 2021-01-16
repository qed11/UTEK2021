import json

def myfunc(c):
    return c[1]

#read the .json file
f = open('1b.json', 'r')
paths = json.load(f)
sorts = []
f.close()

#check the accessibility ration by iterating through the Nodes contained in a path and tally the ones that are accessible
#store the result in a list with format [PathName, accessibility to non-accessibility ratio]
for i in paths['Paths']:
    access = 0
    stations = i['Nodes']
    length = len(stations)
    for j in range(length):
        if stations[j]['Accessible'] == True:
            access += 1
    non = length - access
    sorts.append([i['PathName'],access/non])

#using python's sorting algorithm to sort the 
sorts.sort(reverse = True, key=myfunc)

#write it out to 1b.out file
k = 3
writer = open('1b.out','w')
for i in range(k):
    if i != k-1:
        writer.write(sorts[i][0])
        writer.write(', ')
    else:
        writer.write(sorts[i][0])
writer.close()
