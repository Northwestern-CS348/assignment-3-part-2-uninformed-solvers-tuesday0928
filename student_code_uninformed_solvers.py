
from solver import *
from read import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if self.currentState.state == self.victoryCondition:
            return True
        else:
            if not self.currentState.children:
                movables = self.gm.getMovables()
                for move in movables:
                    self.gm.makeMove(move)
                    new_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                    new_state.parent = self.currentState
                    self.currentState.children.append(new_state)
                    self.gm.reverseMove(move)

            startInd = self.currentState.nextChildToVisit
            endInd = len(self.currentState.children)

            while startInd < endInd:
                if self.currentState.children[startInd] not in self.visited:
                    # found an unvisited child
                    self.currentState.nextChildToVisit = startInd + 1
                    child = self.currentState.children[startInd]
                    self.visited[child] = True
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child
                    return self.currentState.state == self.victoryCondition
                else:
                    startInd += 1

            if startInd == endInd:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                self.solveOneStep()

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = []
        self.front = 0
        self.rear = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        print("CALL")
        print("Current state is: ", self.currentState.state)
        if self.currentState not in self.visited:
            print("How did you even get here??")

        # a trivial case
        if self.currentState.state == self.victoryCondition:
            return True

        if not self.currentState.parent:
            self.queue.append(self.currentState)

        movables = self.gm.getMovables()
        if movables:
            print("the movables are: ")
            for move in movables:
                print(move)
                self.gm.makeMove(move)
                new_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                print("Created new state with move", new_state.state, new_state.requiredMovable)
                new_state.parent = self.currentState
                self.queue.append(new_state)
                self.rear += 1
                self.gm.reverseMove(move)
        else:
            print("no movables from this state")

        self.front += 1
        while self.front <= self.rear:
            visited_p = False
            for st in self.visited.keys():
                if st.state == self.queue[self.front].state:
                    visited_p = True
                    break
            if not visited_p:
                print("The unvisited state under consideration: ", self.queue[self.front].state)
                print("the required movable to get to this state is, ", self.queue[self.front].requiredMovable)
                old_state = self.currentState
                self.currentState = self.queue[self.front]
                self.visited[self.currentState] = True
                self.gm.makeMove(self.queue[self.front].requiredMovable)
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    self.currentState = old_state
                    self.gm.reverseMove(self.queue[self.front].requiredMovable)
                    print("reversed move ,", self.queue[self.front].requiredMovable)
                    print("current state is, ", self.currentState.state)
            else:
                self.front = self.front + 1
