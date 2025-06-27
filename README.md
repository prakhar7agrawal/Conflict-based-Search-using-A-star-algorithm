# Conflict-Based-Search
Implementation of conflict-based-search algorithm for multi-agent pathfinding based on A* Algorithm.
I have shown the implementation using grids created on terminal only without any interface as the work is solely about understanding the algorithm and implementing it with added Novelties.

The novelties added are:
    Storing only one constraint per node and gaining others by backtracking, which reduces memory consumption, thus increasing space complexity
    Implementation of Standley Tie Breaking
    Implementing low level search for only the new constraint in each constraint node to improve time complexity
For more info about the algorithm, refer to the following research paper: https://www.sciencedirect.com/science/article/pii/S0004370214001386#:~:text=CBS%20is%20a%20two%2Dlevel%20algorithm%2C%20divided%20into%20high%2D,constraints%20for%20a%20single%20agent.
