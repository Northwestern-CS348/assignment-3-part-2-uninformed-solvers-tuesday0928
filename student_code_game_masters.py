from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        # peg1
        peg1 = []
        onPeg1 = self.kb.kb_ask(parse_input('fact: (on ?d peg1)'))
        if onPeg1:
            for disk in onPeg1:
                peg1.append(int(str(disk.bindings_dict['?d']).replace('disk', '')))
        peg1.sort()

        # peg2
        peg2 = []
        onPeg2 = self.kb.kb_ask(parse_input('fact: (on ?d peg2)'))
        if onPeg2:
            for disk in onPeg2:
                peg2.append(int(str(disk.bindings_dict['?d']).replace('disk', '')))
        peg2.sort()

        peg3 = []
        onPeg3 = self.kb.kb_ask(parse_input('fact: (on ?d peg3)'))
        if onPeg3:
            for disk in onPeg3:
                peg3.append(int(str(disk.bindings_dict['?d']).replace('disk', '')))
        peg3.sort()

        res = tuple(peg1), tuple(peg2), tuple(peg3)
        return res

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        movableQuery = self.produceMovableQuery()
        matchedQuery = match(movable_statement, movableQuery.statement)

        disk = matchedQuery['?disk']
        initPeg = matchedQuery['?init']
        targetPeg = matchedQuery['?target']

        # move the disk from init to target
        self.kb.kb_assert(parse_input('fact: (on ' + disk + ' ' + targetPeg + ')'))
        self.kb.kb_retract(parse_input('fact: (on ' + disk + ' ' + initPeg + ')'))

        # remove it from top of current peg
        self.kb.kb_retract(parse_input('fact: (top ' + disk + ' ' + initPeg + ')'))

        # was target peg empty?
        targetEmpty = self.kb.kb_ask(parse_input('fact: (empty ' + targetPeg + ')'))
        if not targetEmpty:
            old_top = self.kb.kb_ask(parse_input('fact: (top ?disk ' + targetPeg + ')'))[0].bindings_dict['?disk']
            self.kb.kb_retract(parse_input('fact: (top ' + old_top + ' ' + targetPeg + ')'))
            self.kb.kb_assert(parse_input('fact: (top ' + disk + ' ' + targetPeg + ')'))
        else:
            self.kb.kb_retract(parse_input('fact: (empty ' + targetPeg + ')'))
            self.kb.kb_assert(parse_input('fact: (top ' + disk + ' ' + targetPeg + ')'))

        # was disk above another disk?
        aboveAnother = self.kb.kb_ask(parse_input('fact: (above ' + disk + '?disk' + ')'))
        if aboveAnother:
            new_top = aboveAnother[0].bindings_dict['?disk']
            self.kb.kb_retract(parse_input('fact: (above ' + disk + ' ' + new_top + ')'))
            self.kb.kb_assert(parse_input('fact: (top ' + new_top + ' ' + initPeg + ')'))
        else:
            self.kb.kb_assert(parse_input('fact: (empty ' + initPeg + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
