# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState()) 
    -> problem.isGoalState requires only the coordinates
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    -> problem.isGetSuccessors requires only the coordinates

    """
    #python pacman.py -l tinyMaze -p SearchAgent

    "*** YOUR CODE HERE ***"
    fringe = util.Stack()                # Fringe to manage which states to expand using a stack
    fringe.push(problem.getStartState()) # Push into the stack the intial state of type [(x,y)]
    
    # print (problem.getStartState()) -> type (x,y)
    
    visited = []                    # List to check whether state has already been visited
    finalPath=[]                         # Final direction list
    pathToCurrentState=util.Stack()      # Stack to maintaing path from start to a state
    currState = fringe.pop()        # Pop last inserted state -> type (x,y)

    while not problem.isGoalState(currState): # Loop till i find the goal state
        if currState not in visited:    # If the current state that i'm visiting is new, append it to the list of visited states
            visited.append(currState)   
            successors = problem.getSuccessors(currState) # Get the successor of the state i'm in 
            for coordinates,direction,cost in successors: 
                fringe.push(coordinates) 
                tempPath = finalPath + [direction] # List of directions
                pathToCurrentState.push(tempPath)
        currState = fringe.pop()
        finalPath = pathToCurrentState.pop()
    return finalPath #Return the list of path till the goal state 



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    #python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()                # Fringe to manage which states to expand using a queue
    fringe.push(problem.getStartState()) # Push into the stack the intial state of type [(x,y)]
    
    # print (problem.getStartState()) -> type (x,y)
    
    visited = []                    # List to check whether state has already been visited
    finalPath=[]                         # Final direction list
    pathToCurrentState=util.Queue()      # Stack to maintaing path from start to a state
    currState = fringe.pop()        # Pop last inserted state -> type (x,y)

    while not problem.isGoalState(currState): # Loop till i find the goal state
        if currState not in visited:    # If the current state that i'm visiting is new, append it to the list of visited states
            visited.append(currState)   
            successors = problem.getSuccessors(currState) # Get the successor of the state i'm in 
            for coordinates,direction,cost in successors: 
                fringe.push(coordinates) 
                tempPath = finalPath + [direction]
                pathToCurrentState.push(tempPath)
        currState = fringe.pop()
        finalPath = pathToCurrentState.pop()
    return finalPath # Return the list of path


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    #python pacman.py -l mediumDottedMaze -p StayEastSearchAgent

    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()                    # Fringe to manage which states to expand using a priority queue
    fringe.push(problem.getStartState(),0)      # Push into the queue the initial coordinates and the cost
    visited = []                                # List to check whether state has already been visited
    tempPath=[]                                 # Temp variable to get intermediate paths
    finalPath=[]                                     # List to store final sequence of directions 
    pathToCurrentState=util.PriorityQueue()               # Queue to store direction to coordinates (currState and pathToCurrent go hand in hand)
    currState = fringe.pop()
    while not problem.isGoalState(currState):   # While my current state is not the goal state
        if currState not in visited:            # If it's an unvisited state
            visited.append(currState)           # Insert the coordinates into the list of visited states
            successors = problem.getSuccessors(currState)   # Get the successor to see if I can arrive at the goal state
            for coordinates,direction,cost in successors:     
                tempPath = finalPath + [direction]           # list of directions
                costToGo = problem.getCostOfActions(tempPath)  #Uniform cost Search requires the cost of the action
                if coordinates not in visited:  # If i've neever been to those coordinates 
                    fringe.push(coordinates,costToGo) # Push into the fringe the cost and the coordinates 
                    pathToCurrentState.push(tempPath,costToGo)  # Push into the fringe the direction and the costs
        currState = fringe.pop() # Take out another state from the fringe
        finalPath = pathToCurrentState.pop()  
    return finalPath



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()                    # Fringe to manage which states to expand
    fringe.push(problem.getStartState(),0)      # Push into the fringe the initial coordinates and the cost
    currState = fringe.pop()                    # Pop a state
    visited = []                                # List to check whether state has already been visited
    tempPath=[]                                 # Temp variable to get intermediate paths
    finalPath=[]                                     # List to store final sequence of directions 
    pathToCurrentState=util.PriorityQueue()               # Queue to store direction to coordinates (currState and pathToCurrent go hand in hand)
    while not problem.isGoalState(currState):       # While my actual state is not the goal state
        if currState not in visited:            # If it's an unvisited state
            visited.append(currState)           # Insert the state in the list of visited states
            successors = problem.getSuccessors(currState)   # Get the successor
            for coordinates,direction,cost in successors:         # for each element in successors
                tempPath = finalPath + [direction]               # Get every direction
                costToGo = problem.getCostOfActions(tempPath) + heuristic(coordinates,problem) #Cost is based on the cost of the action + an heuristic
                if coordinates not in visited:   # If the coordinates are new
                    fringe.push(coordinates,costToGo) # Push them into the fringe with the cost 
                    pathToCurrentState.push(tempPath,costToGo)   # Push the tempPath and the cost into the list of patch
        currState = fringe.pop()    # Take out the currentState and repeate
        finalPath = pathToCurrentState.pop()    
    return finalPath # Return list of Path
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
