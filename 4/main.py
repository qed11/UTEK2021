import json
from nearestSearch import nearestSearch

def main():

    # Load json data
    with open('4.json') as f:
        data = json.load(f)

    # Read inputs
    f = open('4.in', 'r')
    inputList = []
    inputStr = f.readline()
    while len(inputStr) != 0:
        # Process inputs into lists of strings (stations to visit)
        inputStr = inputStr.split(',')
        inputStr[-1] = inputStr[-1].rstrip()
        inputList.append(inputStr)
        inputStr = f.readline()
    f.close()

    # Prep output file
    f = open('4.out', 'w')
    print("InputList: {}".format(inputList))

    #Initiate nearestSearch class
    sol = nearestSearch(data)
    for i, input in enumerate(inputList):
        sol.set_unvisited(input)
        cost, path = sol.searchGraph()
        newString = ', '.join(path)
        newString += ', {}'.format(cost)

        #Add new line unless last line
        if i != len(inputList)-1:
            newString += '\n'
        f.write(newString)
    f.close()

if __name__ == '__main__':
    main()





