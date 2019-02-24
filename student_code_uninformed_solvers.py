
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
        #print("CALL")
        #print("Current state is, ", self.currentState.state)

        if self.currentState.state == self.victoryCondition:
            return True

        if not self.currentState.children:
            movables = self.gm.getMovables()
            for move in movables:
                self.gm.makeMove(move)
                new_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                new_state.parent = self.currentState
                self.currentState.children.append(new_state)
                self.queue.append(new_state)
                self.gm.reverseMove(move)

        while self.front < len(self.queue):
            # if already visited this state, skip it
            if self.queue[self.front] in self.visited:
                self.front = self.front + 1
            else:
                aState = self.queue[self.front]
                if aState.parent == self.currentState:
                    #print("just go one level down to ", state.state)
                    self.currentState = aState
                    self.gm.makeMove(self.currentState.requiredMovable)
                    self.visited[self.currentState] = True
                    if self.currentState.state == self.victoryCondition:
                        return True
                    else:
                        self.front += 1
                        #self.solveOneStep()
                        return False
                else:
                    if self.currentState.depth == aState.depth:
                        # siblings?
                        if self.currentState.parent == aState.parent:
                            #print("go up and down to sibling ", state.state)
                            self.gm.reverseMove(self.currentState.requiredMovable)
                            #self.currentState = self.currentState.parent
                            self.currentState = aState
                            self.gm.makeMove(self.currentState.requiredMovable)
                            self.visited[self.currentState] = True
                            if self.currentState.state == self.victoryCondition:
                                return True
                            else:
                                self.front += 1
                                #self.solveOneStep()
                                return False
                        # cousins
                        else:
                            #print("go to cousin, ", state.state)
                            while self.currentState.parent:
                                self.gm.reverseMove(self.currentState.requiredMovable)
                                self.currentState = self.currentState.parent
                            moveLst = []
                            tempState = aState
                            for i in range(aState.depth):
                                moveLst.append(tempState.requiredMovable)
                                tempState = tempState.parent
                            moveLst.reverse()
                            for i in range(aState.depth):
                                self.gm.makeMove(moveLst[i])
                            self.currentState = aState
                            self.visited[self.currentState] = True
                            if self.currentState.state == self.victoryCondition:
                               return True
                            else:
                                self.front += 1
                               #self.solveOneStep()
                                return False

                    else:
                        # state.depth > self.currentState.depth:
                        #print("go to niece, ", state.state)
                        while self.currentState.parent:
                            self.gm.reverseMove(self.currentState.requiredMovable)
                            self.currentState = self.currentState.parent
                        moveLst = []
                        tempState = aState
                        for i in range(aState.depth):
                            moveLst.append(tempState.requiredMovable)
                            tempState = tempState.parent
                        moveLst.reverse()
                        for i in range(aState.depth):
                            self.gm.makeMove(moveLst[i])
                        self.currentState = aState
                        self.visited[self.currentState] = True
                        if self.currentState.state == self.victoryCondition:
                            return True
                        else:
                            self.front += 1
                            #self.solveOneStep()
                            return False
