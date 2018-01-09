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
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    search_stack = util.Stack()
    successors = problem.getSuccessors(problem.getStartState())

    for ea in successors:
        search_stack.push(ea)

    find_goal = False
    path_actions = []
    visited_pos = set()
    visited_pos.add(problem.getStartState())
    while not search_stack.isEmpty() and not find_goal:
        choice = search_stack.pop()

        if not problem.isGoalState(choice[0]):
            if not choice[0] in visited_pos:
                visited_pos.add(choice[0])
                path_actions.append(choice)

            choice_successors = filter(lambda v: v[0] not in visited_pos, problem.getSuccessors(choice[0]))

            if not len(choice_successors):
                path_actions.pop(-1)
                if path_actions:
                    search_stack.push(path_actions[-1])
            else:
                for ea in choice_successors:
                    search_stack.push(ea)
        else:
            path_actions.append(choice)
            visited_pos.add(choice[0])
            find_goal = True

    return [ea[1] for ea in path_actions]

    
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    search_Queue = util.Queue()
    exploredSet = {}

    path_action = []
    tmpPath = []
    realPath = []
    cornerPath = []

    if problem.isGoalState(problem.getStartState()):
        return 'Stop'

    search_Queue.push((problem.getStartState(), 'Start', 0))
    path_action.append([problem.getStartState()])

    while not search_Queue.isEmpty():
        choice = search_Queue.pop()
        if problem.isGoalState(choice[0]):
            break;
        tmpPath = path_action.pop(0)
        if choice[0] not in exploredSet:
            successors = problem.getSuccessors(choice[0])
            exploredSet[choice[0]] = True
        for x in successors:
            if x[0] not in exploredSet:
                search_Queue.push(x)
                subPath = []
                subPath = tmpPath[:]
                subPath.append(x)
                path_action.append(subPath)
    for x in path_action[0][1:]:
        realPath.append(x[1])
    return realPath
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    search_PQ = util.PriorityQueue()
    search_PQ.push((problem.getStartState(), [], 0), 0)  # state, total actions, total cost

    state, allactions, allcost = search_PQ.pop()
    visited_states = [
        (state, 0)]  # with cost why do I have to do that? => would be better to add them when state is unpacked
    # print "pop ",allcost
    while (not problem.isGoalState(state)):

        successors = problem.getSuccessors(state)
        for next_state, action, cost in successors:
            already_seen = False
            total_cost = problem.getCostOfActions(allactions + [action])
            for i in range(len(visited_states)):
                state_tmp, cost_tmp = visited_states[i]
                if (next_state == state_tmp) and (total_cost >= cost_tmp):
                    already_seen = True
            if (not already_seen):
                search_PQ.push((next_state, allactions + [action], total_cost), total_cost)
                visited_states.append((next_state, total_cost))
        state, allactions, allcost = search_PQ.pop()
        # print "pop ",allcost

    return allactions
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    search_PQ = util.PriorityQueue()
    search_PQ.push((problem.getStartState(), [], 0), 0)  # state, total actions, total cost

    state, allactions, allcost = search_PQ.pop()
    visited_states = [
        (state, 0)]  # with cost why do I have to do that? => would be better to add them when state is unpacked
    while (not problem.isGoalState(state)):

        successors = problem.getSuccessors(state)
        for next_state, action, cost in successors:
            total_cost = problem.getCostOfActions(allactions + [action])
            already_seen = False
            # print "next state:",next_state, action
            for i in range(len(visited_states)):
                state_tmp, cost_tmp = visited_states[i]
                if (next_state == state_tmp) and (total_cost >= cost_tmp):
                    already_seen = True
            if (not already_seen):
                total_cost = problem.getCostOfActions(allactions + [action])
                search_PQ.push((next_state, allactions + [action], total_cost),
                               total_cost + heuristic(next_state, problem))
                visited_states.append((next_state, total_cost))
        state, allactions, allcost = search_PQ.pop()

    return allactions
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
