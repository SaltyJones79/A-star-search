"""
Programer: Jeremy Saltz
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import nessisariy libraries
import heapq
import sys
import copy

# if there was no argument suppied from the command line.
if (len(sys.argv) != 2):
    print()
    print("Usage: %s [hueristic index choice]" %(sys.argv[0]))
    print()
    sys.exit(1)

#the set class
class Set():
    def __init__(self):
        self.thisSet = set()
    def add(self,entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())
    def length(self):
        return len(self.thisSet)
    def isMember(self,query):
        return query.__hash__() in self.thisSet

#the state class
class state():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.tiles = [[0,1,2],[3,4,5],[6,7,8]]
    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def __hash__(self):
        state_tuple = tuple(tuple(row) for row in self.tiles)
        return hash(state_tuple)
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    def copy(self):
        s = copy.deepcopy(self)
        return s

#prioiruty queue
class PriorityQueue():
    def __init__(self):
        self.thisQueue = []
    def push(self, thisNode):
        heapq.heappush(self.thisQueue, (thisNode.f, -thisNode.id, thisNode))
    def pop(self):
        return heapq.heappop(self.thisQueue)[2]
    def isEmpty(self):
        return len(self.thisQueue) == 0
    def length(self):
        return len(self.thisQueue)

#node class
nodeid = 0
class node():
    def __init__(self, board_state, heuristic, g=0):
        global nodeid
        self.id = nodeid
        nodeid += 1
        self.board_state = board_state
        self.h = heuristic
        self.g = g
        self.f = self.g + self.h
        self.parent = None

    def __str__(self):
        return f'Node: id={self.id} f={self.f} g={self.g} h{self.h}'

#converts the char array to a 3x3 grid of ints
def convert_char(char_array):
    #converts the chars to ints
    make_int= [int(char) for char in char_array]

    #takes the int array and makes it a 3x3 grid for the puzzle shuffling
    int_array = [make_int[i:i+3] for i in range(0, len(make_int), 3)]

    #returns the 3x3 array
    return int_array

#a function to calculate the missplaced value
def missplaced_tile_Hval(board_state):
    
    s = state()#create a state object for goal state
    goal_state = s.tiles#the goal state for calculating the missplaced value

    count = 0#to store the missplaced value

    #loops trough to get the total
    for i in range(3):
        #inner loop for each row
        for j in range(3):
            #if it is not the empty tile or in it's goal state add one
            if board_state[i][j] != 0 and board_state[i][j] != goal_state[i][j]:
                count += 1
                
    return count#returns the missplaced value
    
#a function to calculate the manhattan distance
def manhattan_distance(board_state, target_state):
    #to save the manhattan distance
    distance = 0

    #loops through the array
    for i in range(3):
        #inner loop for the rows
        for j in range(3):
            #saves the number in the tile to check for the empty tile
            tile = board_state[i][j]
            if tile != 0:
                #loops through to find the location of the tile
                for x in range(3):
                    for y in range(3):
                        #saves the location of the tile for calculation later
                        if target_state[x][y] == tile:
                            #save tile location
                            target_x, target_y = x, y
                            break

                # Calculate the Manhattan distance for the tile
                distance += abs(i - target_x) + abs(j - target_y)
    #returns the distance
    return distance

#fucntion for generating successor nodes 
def generate_successors(current_node, index, goal_state):
    
    successors = []
    current_state = current_node.board_state  # Extract the state from the current_node
    hueristic_val = [0, 0, 0, 0]
    hueristic_val[0] = 0
    hueristic_val[1] = missplaced_tile_Hval(current_state.tiles)
    hueristic_val[2] = manhattan_distance(current_state.tiles, goal_state.tiles)
    hueristic_val[3] = (manhattan_distance(current_state.tiles, goal_state.tiles) + (round(missplaced_tile_Hval(current_state.tiles)/4)))
    # Get the position of the zero tile
    zero_x, zero_y = None, None
    for i in range(3):
        for j in range(3):
            if current_state.tiles[i][j] == 0:
                zero_x, zero_y = i, j
                break

    # Attempt to move the zero tile in all four directions
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x, new_y = zero_x + dx, zero_y + dy

        # Check if the new position is valid
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            # Create a copy of the current state
            successor_state = current_state.copy()
            
            # Swap the zero tile with the adjacent tile
            successor_state.tiles[zero_x][zero_y], successor_state.tiles[new_x][new_y] = successor_state.tiles[new_x][new_y], successor_state.tiles[zero_x][zero_y]


            # Calculate the heuristic values for the successor state
            hueristic_val[1] = missplaced_tile_Hval(successor_state.tiles)
            hueristic_val[2] = manhattan_distance(successor_state.tiles, goal_state.tiles)
            hueristic_val[3] = (manhattan_distance(successor_state.tiles, goal_state.tiles) + (round(missplaced_tile_Hval(successor_state.tiles)/4)))
            # Create a node for the successor and add it to the list
            successor_node = node(successor_state, hueristic_val[index], current_node.g + 1)
            successor_node.parent = current_node
            successors.append(successor_node)

    return successors
#the A* search function
def a_star_search(board_state, goal_state, h_index):
    heuristic_val = [0, 0, 0, 0]#sets an array for different heuristics
    heuristic_val[0] = 0
    heuristic_val[1] = missplaced_tile_Hval(board_state.tiles)#calulates the tile displacement
    #the manhattan distance
    heuristic_val[2] = manhattan_distance(board_state.tiles, goal_state.tiles)
    #my custom heuristic that adds a fraction of the tile displacement rounded to the Manhattan Distance
    heuristic_val[3] = (manhattan_distance(board_state.tiles, goal_state.tiles) + (round(missplaced_tile_Hval(board_state.tiles)/3)))

    #sets the initial h(n) value for the search
    initial_h_val = heuristic_val[h_index]

    #sets the data for the inital node
    initial_node = node(board_state, initial_h_val, 1)

    #stats a list for the open list
    open_list = PriorityQueue()
    #starts the closed list to keep from infiant loops
    closed_list = Set()

    #pushes the initial node on to list to start generating children
    open_list.push(initial_node)

    # Variables to track the required statistics
    visited_nodes = 0
    max_memory = 0
    optimal_path = []
    depth = 0
    expanded_nodes = 0
    generated_nodes = 0

    # A* search loop
    while not open_list.isEmpty():
        current_node = open_list.pop()
        expanded_nodes += 1  # Increment expanded nodes count
        visited_nodes += 1
        if current_node.board_state.tiles == goal_state.tiles:
            # You've found the goal state, perform your desired actions
            # Backtrack to find the optimal path
            depth = current_node.g - 1
            while current_node:
                optimal_path.append(current_node.board_state)
                current_node = current_node.parent
            optimal_path.reverse()
            break

        if closed_list.isMember(current_node.board_state):
            continue

        successors = generate_successors(current_node, h_index, goal_state)

        for successor in successors:
            g = current_node.g + 1  # Assuming step cost is always one
            generated_nodes += 1  # Increment generated nodes count
            heuristic_val[1] = missplaced_tile_Hval(successor.board_state.tiles)
            heuristic_val[2] = manhattan_distance(successor.board_state.tiles, goal_state.tiles)
            heuristic_val[3] = (manhattan_distance(successor.board_state.tiles, goal_state.tiles) + (round(missplaced_tile_Hval(successor.board_state.tiles)/4)))
            successor_node = node(successor.board_state, heuristic_val[h_index], g)
            successor_node.parent = current_node
            open_list.push(successor_node)

        closed_list.add(current_node.board_state)
        current_memory = open_list.length() + closed_list.length()
        if current_memory > max_memory:
            max_memory = current_memory
   # Calculate the approximate effective branching factor
    if generated_nodes == 0:
        b = 0  # Avoid division by zero
    else:
        b = max_memory**(1/depth) 

    # Print the required statistics
    print("V=%d" % (visited_nodes))
    print("N=%d" % (max_memory))
    print("d=%d" % (depth))
    print("b=%f" % (b))

    # Print each state along the optimal path
    print("\n")
    for state in optimal_path:
        print(state)

    
def main():
    #to store the index value for the different heuristics
    h_index = sys.argv[1]

    #stores the inputs to then save as a matix
    inputs = []
    for line in sys.stdin:
        inputs += line.split()

    #converts the chars to ints and makes it a 3x3 board of ints
    game_board = convert_char(inputs)
    #to use the state class
    s = state()
    s.tiles = game_board
    print(s)
    target_state = state()#to know what the target state is.
    #calls the A* search
    a_star_search(s, target_state, int(h_index))
    

main()