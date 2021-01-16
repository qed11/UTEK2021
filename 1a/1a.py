import json
#load the json file
f = open('1a.json','r')
stations = json.load(f)
f.close()

#check accessibility and writ it into a list
yeet = []
for i in stations['Nodes']:
    if i['Accessible'] == True:
        yeet.append(i['Name'])
wr = open('1a.out','w')

#write the list content into the .out file with the correct formatting
for i in range(len(yeet)):
    if i < len(yeet)-1:
        wr.write(yeet[i])
        wr.write(', ')
    else:
        wr.write(yeet[i])
wr.close()