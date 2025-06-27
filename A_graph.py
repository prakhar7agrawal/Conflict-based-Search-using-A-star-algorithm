"""We have defined the class node given in consideration that the graph is a grid, so the position of Node
with respect to origin and its parent node ie the open node previous to that node is required"""
class Node():
    def __init__(self, parent= None, position = None):
        self.parent = parent
        self.position = position
        #g, h and f are the distance moved till that node, heuristic estimated distance in terms of square of distance and total cost respectively
        self.g = 0
        self.h = 0
        self.f = 0
        #__eq__ is the equality function which is just to make sure that comparison of two nodes means comparison of their positions
    def __eq__(self, node2):
        return (self.position == node2.position )
    
#below is the A* Algorithm for single agent pathfinding on a maze with specified start and end points
def Astarsingle(maze, start, end):
    start_node = Node(None, start)          #as start node has no parent
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)          #parent of end_node is not known initially so we set it as none
    #We have defined f of end_node as 0 so that the curr_node definitely becomes the end_node at some point
    end_node.g = end_node.h = end_node.f = 0
    open_ = []          #open_ is the list of the nodes which can be explored but are not explored yet
    closed_ = []        #closed_ is the list of the explored nodes
    open_.append(start_node)
    while len(open_)>0:
        curr_node = open_[0]    #we would start exploring the open list from its first element
        curr_index = 0
        
        for index, item in enumerate(open_):
            if curr_node.f > item.f:  #this is so that the nodes with less cost function can be set to current node
                curr_node = item
                curr_index = index

        open_.pop(curr_index)
        closed_.append(curr_node)

        if(curr_node == end_node):      #This is for printing with backtracking of nodes from end node to start node
            path = []
            curr = curr_node
            while curr is not None:
                path.append(curr.position)
                curr = curr.parent
            return path[::-1]
        #finding the childdren for a particular node
        children = []
        for poss_neigh in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            node_pos = ( curr_node.position[0] + poss_neigh[0], curr_node.position[1] + poss_neigh[1])
            
            if node_pos[0] > (len(maze) - 1) or node_pos[0] < 0 or node_pos[1] > (len(maze[len(maze)-1]) -1) or node_pos[1] < 0:
                continue

            if maze[node_pos[0]][node_pos[1]] == 1:
                continue



            child_node = Node(curr_node, node_pos)
            children.append(child_node)
        #Looping through the children to find the child nodes that can be explored for checking
        for child in children:
            for close_ in closed_:
                if child == close_:
                    continue

            child.g = curr_node.g +1
            child.h = ((child.position[0] - end_node.position[0])**2) + ((child.position[1]- end_node.position[1])**2)
            child.f = child.g + child.h
            
            for open_node in open_:
                if child == open_node and child.g > open_node.g:
                    continue
            open_.append(child)







def main():
    maze = [[0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],]
    
    start = (1, 2)
    end = (2, 4)

    path = Astarsingle(maze, start, end)
    maze[start[0]][start[1]] = "s"
    maze[end[0]][end[1]] = "e"
    for pos in path:
        if pos != start and pos !=end:
            maze[pos[0]][pos[1]] = "*"

    print(path)
    for i in range(0, 5):
        print(maze[i])

if __name__ == '__main__':
    main()
