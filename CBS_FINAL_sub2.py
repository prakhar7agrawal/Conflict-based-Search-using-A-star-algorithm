import numpy as np
class Agent:        #Agents in this code would be represented in terms of their starting and ending points of the 5*5 grid
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Node:         #This class is for the nodes that we access in A star algorithm for a single agent, which is searched adjacent to its parent node at a certain time step
    def __init__(self, parent, position,t):
        self.parent = parent
        self.position = position
        self.t=t
        self.g = 0
        self.h = 0
        self.f = 0

class ctNode():     #this node defines the structure of the constraint tree, which starts from a root which assumes no constraints for agents and expands as conflicts are found and added as per CBS algorithm
    def __init__(self, solution,parent):
        self.parent=parent
        constraint= []
        self.constraint = constraint
        self.solution = solution
        self.cost= 0    
def low_level_path(maze, agent,constraints):           #Astar algorithm for single agent pathfinding is modified in this function by adding constraints at different timesteps which were added after conflicts were found in the solutions of the parent node in the constraint tree
    start = Node(None, agent.start,0)
    open_ = []
    #open list consists of the nodes which are left for exploration in te A star algorithm and are possible the nodes with the lowest f costs
    open_.append(start)
    while open_:
        current_node = open_[0]
        current_index = 0
        for i in range(1, len(open_)):
            if open_[i].f < current_node.f:
                current_node = open_[i]
                current_index = i
        open_.pop(current_index)
        #The if statement below is to be implemented when the node accessed in open list is the end vertex of the given agent and then it backtracks through the parents of the nodes to return the solution path of the agent with given constraints
        if current_node.position == agent.end:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        for poss_neigh in ((0, 1), (1, 0), (0, -1), (-1, 0),(1,-1),(1,1),(-1,-1),(-1,1)):   #Now we would be accessing the adjecent nodes of the current node and would select the nodes which have not been explored and dont have any constraint to the open list
            position = [current_node.position[0] + poss_neigh[0], current_node.position[1] + poss_neigh[1]]
            #below two if statements are to make sure that the points that are being accessed are withing the maze
            if position[0] < 0 or position[0] >= len(maze) or position[1] < 0 or position[1] >= len(maze):
                continue
            if maze[position[0]][position[1]] == 1:
                continue
            child_node = Node(current_node, position,current_node.t+1)  #this created a node which has previous node as its parent and is accesed at consecutive time step
            child_node.g = current_node.g + 1
            child_node.h = (child_node.position[0] - agent.end[0])**2 + (child_node.position[1] - agent.end[1])**2
            child_node.f = child_node.g + child_node.h

            if [child_node.position,child_node.t] in constraints:       #This removes those nodes from consideration which are within the constraints of that node
                continue
            open_.append(child_node) 


#SIC function calulates the sum of individual costs of the optimised paths of all the agents and is used as representation of cost in high level cbs
#The cost of an agent's path is the number of time steps required for the agent to complete the path
def SIC(solution):
    cost=0
    for path in solution:
        cost+=len(path)-1
    return cost

#This function checks the validity of the solution by looking for constraints
def isValid(solution):
    for i in range(len(solution)):
        for j in range(i+1,len(solution)):
            for k in range(min(len(solution[i]),len(solution[j]))):
                if solution[i][k]==solution[j][k]:
                    return [i,j,solution[i][k],k]
    return 1

def CBS(maze, agents):       
  #This is the high level search algorithm which creates a tree for nodes having increasing set of constraints anc calculates the most optimised solution to a given problem for multi agent pathfinding
    root = ctNode([], None)
    root.solution = []
    for agent in agents:
        root.solution.append(low_level_path(maze, agent, []))
    root.cost = SIC(root.solution)
    #open list contains of the ctnodes which are not explored yet and then check all these one by one in order of decreasing costs.
    open_list = []
    open_list.append(root)
    #We loop through the open list now to look for any the nodes with lowest cost and valid solutions, and if valid solution is not found, we resolve the conflicts
    #found by adding constraints of that conflict to the respective agents of the ctnode
    while open_list: 
        x = 0
        min_cost = float("inf")
        for i in range(len(open_list)):     #Here we find out the node with the lowest cost
            if open_list[i].cost < min_cost:
                min_cost = open_list[i].cost
                x = i
        n = open_list.pop(x)
        a = isValid(n.solution)     #Here we check for validity of the solution, and if the solution is valid, then it is returned
        if a == 1:
            return n.solution
        conflict = a

        #Resolution of conflicts, here we add two more possible nodes to the open list by adding constraint to them corresponding to the conflict and find the solution of the
        #node by employing low leve search
        for i in [0, 1]:
            solution_copy = n.solution.copy()
            next_node = ctNode(solution_copy, n)
            next_node.constraint = [conflict[i], conflict[2], conflict[3]]
            con = next_node
            agent_constraints = []
            while con.constraint != []:     #This is the backtracking algorithm where we start from current node and reach upto the last node to add the constraints
                if con.constraint[0] == conflict[i]:
                    constraint = con.constraint
                    agent_constraints.append([constraint[1], constraint[2]])
                con = con.parent 
            next_node.solution[conflict[i]] = low_level_path(maze, agents[conflict[i]], agent_constraints)  #This is where we employ low level search to find the solution of the newly found node
            open_list.append(next_node)
        
def main():     #Main function takes the inputs for a n*n maze for agents and obstacles
    n = int(input("Enter the dimensions of the square matrix"))
    dimension_of_maze = n
    maze_map = [[0 for _ in range(dimension_of_maze)] for _ in range(dimension_of_maze)]

    num_agents_required = int(input("Enter the count of agents: "))
    agents = []

    num_obstacles_present = int(input("Enter the number of obstacles: "))
    for _ in range(num_obstacles_present):
        obstacle_row = int(input("Enter obstacle's row coordinate: "))
        obstacle_column = int(input("Enter obstacle's column coordinate: "))
        maze_map[obstacle_row][obstacle_column] = 1

    for _ in range(num_agents_required):
        agent_start_row = int(input("Enter agent's starting row coordinate: "))  
        agent_start_column = int(input("Enter agent's starting column coordinate: "))
        agent_stop_row = int(input("Enter agent's stopping row coordinate: "))
        agent_stop_column = int(input("Enter agent's stopping column coordinate: "))
        agents.append(Agent([agent_start_row, agent_start_column], [agent_stop_row, agent_stop_column]))
    for i in CBS(maze_map, agents):
            print(i)

if __name__ == "__main__":
    main()

"""Novelties added:
1.  Storing only one constraint per node and gaining others by backtracking, which reduces memory consumption, thus increasing space complexiity
"""