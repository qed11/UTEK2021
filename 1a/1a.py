import json
f = open('1a.json','r')
paths = json.load(f)
f.close()
yeet = []
for i in paths['Nodes']:
    if i['Accessible'] == True:
        yeet.append(i['Name'])
wr = open('1a.out','w')

for i in range(len(yeet)):
    if i < len(yeet)-1:
        wr.write(yeet[i])
        wr.write(', ')
    else:
        wr.write(yeet[i])
wr.close()