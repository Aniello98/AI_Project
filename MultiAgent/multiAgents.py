# multiAgents.py
# --------------
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



from util import manhattanDistance
from util import euclideanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        oldFood = currentGameState.getFood()
        #newGhostStates = successorGameState.getGhostStates()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        score = -1

        if(successorGameState.isLose()):
            return -float('inf')
        if(successorGameState.isWin()):
            return float('inf')
        if Directions.STOP in action:
            return -100
        
        minDistanceFromFood = 1000000
        for f in oldFood.asList():
            distance = manhattanDistance(newPos,f)
            if distance < minDistanceFromFood:
                minDistanceFromFood = distance

        score-=minDistanceFromFood

        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def minimax(self, s, d, i):
        values = []

        if(s.isLose()):
                return s.getScore(), "Stop"
        if(s.isWin()):
                return s.getScore(), "Stop"

        #print(d)
        if(d == self.depth):
            return s.getScore(), "Stop"
        if(i == 0):
            for action in s.getLegalActions(0):
                values.append(self.minimax(s.generateSuccessor(i, action), d, (i+1)%s.getNumAgents())[0])
            return max(values), action
        else:
            if (i == s.getNumAgents()-1):
                    d+=1
            for action in s.getLegalActions(i):
                
                values.append(self.minimax(s.generateSuccessor(i, action), d, (i+1)%s.getNumAgents())[0])
            return min(values), action

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        values = []

        for action in gameState.getLegalActions(0):
                values.append((self.minimax(gameState.generateSuccessor(self.index, action), 0, self.index+1), action))

        #value, action = self.minimax(gameState.state,0)

        
        i = values.index(max(values))

        return values[i][1]
        
        #calcolare utility fino a depth
        #scegliere azione che porta alla miglior utility
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        
        alpha = float('-inf')
        beta = float('inf')
        
        for action in gameState.getLegalActions(0): #b1 b2
            v = self.min_value(gameState.generateSuccessor(self.index, action), 0, alpha, beta, self.index+1)
         #   print("print v: ", v)
            #print(alpha)
            if v[0] >alpha:
                
                best_a = action
                print("best_a: ",best_a)
                alpha = v[0]
        return best_a
        #util.raiseNotDefined()

    def min_value(self, state, d, alpha, beta, i):
        #print("in min index is: ", i)
        v=float('inf')
        
        if(state.isLose()):
           #     print("score in min, lose state: ", state.getScore())

                return state.getScore(), "Stop"
        if(state.isWin()):
          #      print("score in min, win state: ", state.getScore())

                return state.getScore(), "Stop"

        #print(d)
        if(d == self.depth):
         #   print("score in min: ", state.getScore())
            return state.getScore(), "Stop"
        
        for action in state.getLegalActions(i):
            if (i+1)%state.getNumAgents()==0:
                v = min(v, self.max_value(state.generateSuccessor(i, action), d+1, alpha, beta, (i+1)%state.getNumAgents())[0])
            else :
                v = min(v, self.min_value(state.generateSuccessor(i, action), d, alpha, beta, (i+1)%state.getNumAgents())[0])
            if v<alpha:
                return v, action
            beta = min(beta,v)
        #print("beta: ",beta)
        return v, action

    def max_value(self, state, d, alpha, beta, i):
        #print("in max index is: ",i)
        v=float('-inf')

        if(state.isLose()):
              #  print("score in max, lose state: ", state.getScore())

                return state.getScore(), "Stop"
        if(state.isWin()):
             #   print("score in max, win state: ", state.getScore())

                return state.getScore(), "Stop"


        #print("depth: ", d)
        if(d == self.depth):
            #print("score in max: ", state.getScore())
            return state.getScore(), "Stop"

        for action in state.getLegalActions(i):
            if (i+1)%state.getNumAgents() == 0:
                v = max(v, self.max_value(state.generateSuccessor(i, action), d+1, alpha, beta, (i+1)%state.getNumAgents())[0])
            else :
                v = max(v, self.min_value(state.generateSuccessor(i, action), d, alpha, beta, (i+1)%state.getNumAgents())[0])
            if beta<v:
                return v, action
            alpha = max(alpha,v)
        return v, action


        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax(self, s, d, i):
            values = []
            sum=0

            if(s.isLose()):
                    return s.getScore(), "Stop"
            if(s.isWin()):
                    return s.getScore(), "Stop"

            #print(d)
            if(d == self.depth):
                return s.getScore(), "Stop"
            if(i == 0):
                for action in s.getLegalActions(0):
                    values.append(self.expectimax(s.generateSuccessor(i, action), d, (i+1)%s.getNumAgents())[0])
                return max(values), action
            else:
                if (i == s.getNumAgents()-1):
                        d+=1
                for action in s.getLegalActions(i):
                    sum+=self.expectimax(s.generateSuccessor(i, action), d, (i+1)%s.getNumAgents())[0] / len(s.getLegalActions(i))
                return sum, action

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        values = []

        for action in gameState.getLegalActions(0):
                values.append((self.expectimax(gameState.generateSuccessor(self.index, action), 0, self.index+1), action))

        #value, action = self.minimax(gameState.state,0)

        
        i = values.index(max(values))

        return values[i][1]
        

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
