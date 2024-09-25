#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programer: Jeremy Saltz
Random-board.py is a program that takes an input 
and creates a puzzle to be solved by the a-star.py
program. The input is a text file OLA1-input.txt.
The text file is a 3x3 grid of numbers 0 - 8 that 
look like this 0 1 2 and are then handled like an 
               3 4 5
               6 7 8 
array of numbers. The 0 is considered a blank tile 
and is the number to consider when making moves to
shuffle the board. The program takes two other arguments
from the command line along with the file as imput.
The first argument is the seed number to save a seed 
of randomly generated numbers for testing different 
heuristics for comparision. The second argument is 
how many random moves you would like the program to
take to shuffle the board. After the program is done
the game board will be shuffled for puzzle solving in 
the a-star.py program.
"""
#import sys to get input from the command line
#import the numpy.random for random number generation
import sys, numpy.random as random # type: ignore
import copy #to make a deep copy in the state class

#if there are not enough arguments in the command line print warring
if (len(sys.argv) != 3):
    print()
    print("Usage: %s [seed] [number of random moves]" %(sys.argv[0]))
    print()
    sys.exit(1)

#the state class
class state():
    #creates an intial board state. 
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.tiles = [[0,1,2],[3,4,5],[6,7,8]]
    #tries to move left if it's possible
    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    #tries to move right if possible 
    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    #tries to move up if possible
    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    #tries to move down if possble
    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    #
    def __hash__(self):
        return (tuple(self.tiles[0]),tuple(self.tiles[1]),tuple(self.tiles[2]))
    #turns the 3x3 board state to a printable format
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    #makes a copy of itself
    def copy(self):
        s = copy.deepcopy(self)
        return s
#converts the input read from the command line and turns the array of 
#characters to a 3x3 list of ints for use with the state class
def convert_char(char_array):
    #turns chars to ints 
    make_int= [int(char) for char in char_array]

    #turns the 1x9 array to a 3x3 array 
    int_array = [make_int[i:i+3] for i in range(0, len(make_int), 3)]

    #returns the array
    return int_array

#the main function
def main():

    #stores the seed number for the random numbers being generated
    rng = random.default_rng(int(sys.argv[1]))

    #saves the number of moves to be made
    number_of_moves = int(sys.argv[2])

    #saves the inputs from the command line
    inputs = []
    for line in sys.stdin:
        inputs += line.split()

    #save the game board a a 3x3 grid
    game_board = convert_char(inputs)

    #create an object of the state class
    s = state()

    #sets the tiles to the sames state as the 3x3 grid
    s.tiles = game_board

    #loops through making moves based on how many moves have been
    #sent through the command line
    for x in range(number_of_moves):

        #generate a random number from 0 - 3 
        #the numbers are then used to decide 
        #which move to make. 
        # 0=up, 1=right, 2=down, 3=left
        move = rng.integers(4)
        if move == 0:
            new_board = s.up()
        elif move == 1:
            new_board = s.right()
        elif move == 2:
            new_board = s.down()
        else:
            new_board = s.left()
        #if the move was leagle update the board.
        if new_board is not None:
            s = new_board

    print(s)

main()