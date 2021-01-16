import json
#load the json file
f = open('1a.json','r')
stations = json.load(f)
f.close()

#check accessibility and writ it into a list
accessible = []
for i in stations['Nodes']:
    if i['Accessible'] == True:
        accessible.append(i['Name'])

#write the list content into the .out file with the correct formatting
wr = open('1a.out','w')
for i in range(len(accessible)):
    if i < len(accessible)-1:
        wr.write(accessible[i])
        wr.write(', ')
    else:
        wr.write(accessible[i])
wr.close()