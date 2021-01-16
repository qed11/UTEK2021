#UTEK 2021 PROGRAMMING COMPETITION - QUESTION 2

#begin by reading and storing the JSON file for further use

#function that implements Djikstra's Algorithm to find the shortest path between two nodes in the JSON listing
def find_shortest_path(data, LocA, LocB):
    '''
    (dict, string, string) -> list

    Returns a list containing the path, alongside the total distance, between
    LocA and LocB as accessed from the dictionary data from 2.json.
    
    Sample Outputs:
    
    >>>find_shortest_path(data, "Yonge and Dundas", "College")
    [["Yonge and Dundas", "College"], 15]
        
    '''
    start = LocA
    end = LocB

    #create a distance dictionary for each node; populate so all distances start at infinity
    dist = dict()

    for Loc in data['Nodes']:
        dist[Loc['Name']] = float('inf')

    #set the distance for the starting node to 0
    dist[LocA] = 0

    #initialize a list of visited nodes, unvisited nodes, and a 'previously visited nodes'
    visited = list()
    previous = {}
    unvisited = list()

    for Loc in data['Nodes']:
        unvisited.append(Loc['Name'])
        previous[Loc['Name']] = None

    #create a dictionary of numerical indices associated with each node - makes it easier to index the JSON data when finding neighbours
    indices = dict()
    count = 0

    for nodes in data['Nodes']:
        indices[data['Nodes'][count]['Name']] = count
        count += 1

    #implement the bread and butter of Djikstra's Algorithm
    cur_node = start
    cur_index = indices[cur_node]

    while cur_node != end and len(unvisited) > 0:
        #update the lists with the currently visited node (first time is starting node)
        visited.append(cur_node)
        unvisited.remove(cur_node)

        #visit all the neighbours and update their distances
        for neighbour in data["Nodes"][cur_index]["Neighbours"]:
            if previous[neighbour['Name']] == None:
                previous[neighbour['Name']] = cur_node
            new_dist = dist[cur_node] + neighbour["Distance"]
            if new_dist < dist[neighbour['Name']]:
                dist[neighbour['Name']] = new_dist
                previous[neighbour['Name']] = cur_node

        #now we select a new node to use - use the shortest distance in the distance dictionary
        if len(unvisited) == 0:
            continue
        small_dist = dist[unvisited[0]]
        
        for i in range(len(unvisited)):
            if dist[unvisited[i]] < small_dist:
                small_dist = dist[unvisited[i]]     #gives the shortest distance, now need to find the node associated with it
        
        for place in dist:
            if dist[place] == small_dist:
                if place in unvisited:
                    cur_node = place
                    cur_index = indices[cur_node]

    #either ending condition is met (there is a path) or it is not. Consider both cases.
    if cur_node != end:
        return [[], None]
    else:
        #if a path is found, retrace it
        path = [end]
        reverse_node = end
        while reverse_node != start:
            reverse_node = previous[reverse_node]
            path.append(reverse_node)


    #prepare final return value, then return the path and distance
    final_distance = dist[end]

    return [path[::-1], final_distance]
