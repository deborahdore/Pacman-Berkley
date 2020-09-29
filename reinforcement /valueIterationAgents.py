# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates() #gives a list of tuples of states  [state = (x,y)]
              mdp.getPossibleActions(state) #gives a list of possible actions based on the state proposed (west, east, north, south)
              mdp.getTransitionStatesAndProbs(state, action) #gives a list of ((state), probability) based on the action (state function)
              mdp.getReward(state, action, nextState)#gives a reward based on (state, action, state)
              mdp.isTerminal(state) #returns true or false
              
            VALUE ITERATION(S,A,P,R,0)
            INPUTS: 
                S = set of all states "mdp.getStates()"
                A = set of all actions "mdp.getPossibleActions(state)"
                P = a state transition function specifying P(s'| s,a) "mdp.getTransitionStatesAndProbs(state, action)"
                R = reward function R(s,a,s') " mdp.getReward(state, action, nextState"
                0 = threshold > 0
            
                OP[S] = optimal policy
                V[S] = value function 

                Vk[s] = array,sequence oof value funcition 

                1:  for k = 1 : infinity
                2:      for each state
                3:          Vk[s] = max summatory{P(s'| s,a) * R(s,a,s') + yVk-1[S']}
                4:      if for all |Vk[s] - Vk-1[s]| <= 0
                5:          for each state s
                6:              OP[s] = arg max summatory{PP(s'| s,a) * R(s,a,s') + yVk-1[S']} 
                7:          return OP, Vk
        """
        self.mdp = mdp
        self.discount = discount #value 0.9
        self.iterations = iterations #100 interactions left
        self.values = util.Counter() # A Counter is a dict with default 0
        "*** YOUR CODE HERE ***"
        for iteration in range(0, self.iterations):     #range that goes from 0 to 100  
            for state in mdp.getStates():               #for each state possibile       
                if not self.mdp.isTerminal(state):      #if the state is not terminal
                    action = self.getAction(state)      #recover the possibile action on that state 
                    #assign to each state the expected return from that state given that the agent uses the policy = Value Function
                    self.values[state] = self.computeQValueFromValues(state, action) 
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.
        """
        "*** YOUR CODE HERE ***"
        #if there are no legal actions, 
        # which is the case at the terminal state,
        # you should return None.
        if self.mdp.isTerminal(state):
            return None

        bestAction = None #initializing best action
        bestVal = None #initializing best Value
        for action in self.mdp.getPossibleActions(state): #for every possibile action 
            value = self.computeQValueFromValues(state, action) #compute the q value
            if bestVal is None or bestVal < value:
                bestVal = value
                bestAction = action
        return bestAction


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        #Q value is equal to the summation of every probability * (reward + discount + the value of the next states)
        "*** YOUR CODE HERE ***"
        value = 0 #initialising the return value 
        #saves in stateSucc the next state (x,y) and in prob the probability of that state with that action 
        for stateSucc, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            #compute the value
            #mdp.getReward(state, action, nextState) -> gives a reward based on (state, action, state)
            #self.discount is an integer that express the discount 
            #self.getValue(stateSucc) returns the value of the state
            value += prob * (self.mdp.getReward(state, action,stateSucc) + (self.discount * self.values[stateSucc]))
        return value

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
