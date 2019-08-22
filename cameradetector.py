import math


class Vertex:
    def __init__(self, node):
        # the vertex number
        self.id = node
        # storing the initial distance in graph
        self.connections = [None] * 6105
        self.adjacent_list = []
        # storing optimum distance for updating purpose
        # initialize to infinity
        self.optimum = math.inf
        self.visited = False
        self.finalised = False
        # keep track of the path
        self.previous = None
        self.camera = False

    def get_id(self):
        return self.id

    def set_distance(self, dist):
        self.optimum = dist

    def get_distance(self):
        return self.optimum

    # add connection to adjacent vertex at each vertex
    # store distance at the vertex at the same time
    def add_adjacent(self, adjacent, dist, toll):
        self.adjacent_list.append((adjacent, toll))
        self.connections[adjacent] = dist

    def set_previous(self, prev_node):
        self.previous = prev_node

    # so that when vertex obkect is compared, it will be based on its optimum distance
    def __lt__(self, obj):
        return self.optimum < obj.optimum

    # so that when vertex object is being check existence, it will be based on its id
    #def __eq__(self, obj):
        #return self.id == obj.id

    # for displaying purpose
    def __str__(self):
        if self.previous is None:
            previous = "None"
        else:
            previous = self.previous.get_id()
        return "(" + str(self.id) + " , " + str(self.optimum) + " , " + str(previous) + ")"


class Graph:
    def __init__(self):
        self.vertices = [None] * 6105

    # create a vertex object in the list of graph
    def add_vertex(self, node):
        new_vertex = Vertex(node)
        self.vertices[node] = new_vertex

    # return the vertext object by id
    def get_vertex(self, n):
        if self.vertices[n] is not None:
            return self.vertices[n]
        else:
            return None

    def add_edge(self, source, adjacent, dist, toll):
        if self.vertices[source] is None:
            self.add_vertex(source)
        if self.vertices[adjacent] is None:
            self.add_vertex(adjacent)

        self.vertices[source].add_adjacent(adjacent, dist, toll)
        self.vertices[adjacent].add_adjacent(source, dist, toll)


import heapq


# find the k closest cameras from the source
def dijkstra(graph, source, kmax):
    # initialize the source vertex as distance of 0
    source.set_distance(0.0)

    # initialize discovered list
    discovered = []
    # insert pair into the list
    heapq.heappush(discovered, (0.0, source))
    # initialize a priority queue using the list

    # create a list to store all the finalised vertex
    finalised = []
    k = []
    # while discovered is not empty
    while len(discovered) > 0:

        # get the smallest distance from discovered list

        # heapq.heapify(discovered) - no need to call here, called down there
        pop_min = heapq.heappop(discovered)
        smallest = pop_min
        current_node = smallest[1]  # graph.get_vertex(smallest)
        current_node.visited = True

        # if v is not finalised
        if current_node.finalised is False:

            # if the vertex has red light camera, straight away put it in finalised
            # because Alice wouldnt want to pass through red light camera
            # thus, every vertex with red light camera is the end node (target)
            if current_node.camera is True:
                k.append(current_node)
            else:
                # for each outgoing edge of current node
                # where we search through all the edges of current vertex in edge list
                # the list of edges is called connections
                for adjacenttuple in current_node.adjacent_list:
                    adjacent = adjacenttuple[0]

                    toll = adjacenttuple[1]

                    adjacent_node = graph.get_vertex(adjacent)

                    if not toll:
                        # print("no toll")
                        # if the edge is not in discovered or finalised

                        if adjacent_node.visited is False:
                            if adjacent_node.finalised is True:
                                pass
                            else:
                                # update the new distance of adding edges and current vertex
                                # update the previous vertex if distance is being updated for back tracking purpose
                                # means the route has been changed
                                new_distance = current_node.get_distance() + current_node.connections[adjacent]
                                adjacent_node.set_distance(new_distance)
                                adjacent_node.set_previous(current_node)
                                adjacent_node.visited = True

                                # insert into discovered list only when the vertex has no toll roads
                                # if true then ignored
                                heapq.heappush(discovered, (new_distance, adjacent_node))

                        # if the new distance is smaller than the optimum
                        # in current vertex + new edge adjacent
                        else:
                            new_distance = current_node.get_distance() + current_node.connections[adjacent]

                            if new_distance < adjacent_node.get_distance():
                                adjacent_node.set_distance(new_distance)
                                adjacent_node.set_previous(current_node)
                                adjacent_node.visited = True

                                heapq.heappush(discovered, (new_distance, adjacent_node))

                                # print('not supposed to be here la bro',adjacent_node.get_id())

            current_node.finalised = True
            # print('finalised weyh',current_node.get_id(),current_node.finalised)
            finalised.append(current_node)

        # check how many cameras there are in the finalised list
        # return only the needed ( user input )
        # break if enough
        if len(k) == kmax:
            break

        # call heapify to sort the list into min heap position after the inserting and updating each time
        # heapq.heapify(discovered)
    # print('yo the finalised',finalised)
    return finalised, k


# to recover the path by looking at the previous of each vertex
def recovering_path(v):
    path = []
    recovering_path_aux(v, path)
    path.append(v.get_id())
    return path

def recovering_path_aux(v, path):
    if v.previous:
        recovering_path_aux(v.previous, path)
        path.append(v.previous.get_id())
    return


graph = Graph()

edges = open("edges.txt", "r")
for line in edges:
    each_line = line.strip("\n")
    vertex = each_line.split(" ")

    # excluding the vertex with toll roads
    if len(vertex) < 4:
        graph.add_edge(int(vertex[0]), int(vertex[1]), float(vertex[2]), False)
    # if len = 4, there is toll (4th element = TOLL)
    else:
        graph.add_edge(int(vertex[0]), int(vertex[1]), float(vertex[2]), True)
        # set an indicator to check whether the vertex is in toll road
        # graph.get_vertex(int(vertex[0])).toll.append(int(vertex[1]))
        # graph.get_vertex(int(vertex[1])).toll.append(int(vertex[0]))

vertices = open("vertices.txt", "r")
for line in vertices:
    each_line = line.strip("\n")
    vertex = int(each_line)
    # all the vertex in vertices.txt has cameras
    graph.get_vertex(vertex).camera = True

location = int(input('Enter your location:'))
k = int(input('Enter k: '))

source = graph.get_vertex(location)
finalized, klist = dijkstra(graph, source, k)

if len(klist) == 0:
    print("Oops! You're stuck here Alice!")
i = 1
for node in klist:
    if node.get_id() == location:
        print('Oops! Cannot help, Alice!! Smile for the camera!')
    else:
        print("Camera " + str(i) + ":", node.get_id(), " Distance from your location: " + str(node.get_distance()))
        each_shortest = recovering_path(node)
        print("Shortest path: ", end='')
        for j in range(len(each_shortest) - 1):
            print(each_shortest[j], end=" --> ")
        print(each_shortest[-1])
    i += 1

# test to check whether graph is working
# print(graph.get_vertex(6032).connections)

# check whether the vertices with cameras are marked
# print(graph.get_vertex(12).camera)

