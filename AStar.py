import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # cost from start to current node
        self.h = 0  # Heuristic cost from current node to goal
        self.f = 0  # total cost (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node, grid):
    neighbors = []
    x = node.position[0]
    y = node.position[1]
    tile = grid[x][y]
    OPEN = 2
    DOOR = 3
    if(tile.visited == False and tile.top == OPEN or tile.top == DOOR):
        neighbors.append((0, 1))
    if(tile.visited == False and tile.bot == OPEN or tile.bot == DOOR):
        neighbors.append((0, -1))
    if(tile.visited == False and tile.left == OPEN or tile.left == DOOR):
        neighbors.append((-1, 0))
    if(tile.visited == False and tile.right == OPEN or tile.right == DOOR):
        neighbors.append((1, 0))
    return neighbors

def a_star(start, goal, grid):
    open_list = []
    closed_list = set()

    start_node = Node(start)
    goal_node = Node(goal)

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        #print(f"current_node -> {current_node.position}")
        closed_list.add(current_node.position)

        if(current_node == goal_node):
            path = []
            while (current_node):
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1][1:] # return reversed path and remove the first index (current position)

        neighbors = get_neighbors(current_node, grid) 
        #if(current_node.position[0] == 6 and current_node.position[1] == 19):
            #print(f"neighbors -> {neighbors}")

        for neighbor in neighbors:
            neighbor_position = (current_node.position[0] + neighbor[0], current_node.position[1] + neighbor[1])
            neighbor_node = Node(neighbor_position, current_node)

            #if(current_node.position[0] == 6 and current_node.position[1] == 19):
                #print(neighbor_position)

            if (neighbor_node.position in closed_list):
                continue

            neighbor_node.g = current_node.g + 1
            neighbor_node.h = heuristic(neighbor_node.position, goal_node.position)
            #print(neighbor_node.h)
            #if(neighbor_node.h == 1):
                #print(f" --> {neighbor_node.position}")
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            if(add_to_open(open_list, neighbor_node, grid[goal[0]][goal[1]], grid)):
                heapq.heappush(open_list, neighbor_node)

    return None # No path found


def add_to_open(open_list, neighbor_node, goal_name, board):
    for node in open_list:
        #if(neighbor_node == node and neighbor_node.g >= node.g):
        tile = board[node.position[0]][node.position[1]]
        if(neighbor_node == node and neighbor_node.g > node.g and (tile.name == goal_name or tile.name == "tile")):
            return False
    return True 




