"""
Copyright (C) 2014 Ryan Hansen.  All rights reserved.
This source code (including its associated software) is owned by Ryan Hansen and
is protected by United States and international intellectual property law, including copyright laws, patent laws,
and treaty provisions.
"""

import itertools
import random

from core.const import PLAYERS, WIN_VECTORS, CORNERS


class Game(object):
    x = []
    o = []
    move = None

    @property
    def available(self):
        """Return a list of available moves based on the position already held by both players"""

        board = self.x + self.o
        moves = []
        for p in range(0, 9):
            if p not in board:
                moves.append(p)
            p += 1
        return moves

    def take(self, player, pos):
        """Assign the chose position to the given player"""

        attr = self.__getattribute__(PLAYERS[player])
        attr.append(pos)

    def next_move(self):
        """Calculate the best next move."""

        # Take the center position first, if available (avoid unnecessary processing of eval_tree)
        if 4 not in self.o and 4 not in self.x:
            return 4

        # If the opponent takes center first, take one of the corners (again, avoiding eval_tree)
        if self.o[0] == 4 and len(self.x) == 0:
            return CORNERS[random.randrange(0, 4)]

        # If possible, win the game. I found that eval_tree (minimax) will definitely not lose, but when faced with the
        # decision to block vs. win, it chooses to block.
        win = self.winnable('machine')
        if win:
            return win

        scores = self.eval_tree('machine')

        return max(scores, key=scores.get)

    def eval_tree(self, player, depth=0):
        """Determine the next move based on the implementation of the famous minimax algorithm"""

        depth += 1  # Recursion depth, incrementing by one with each pass
        scores = {}  # The collection of scores for each of the moves evaluated
        opponent = self.switch_player(player)  # opponent gets passed to next_move for minimax recursion

        # Start evaluating available moves
        for m in self.available:
            self.take(player, m)  # Take the proposed move
            if self.winner(player):  # See if proposed move gives the win to <player>
                self.clear(player, m)  # Clear the evaluated move
                if player == 'machine':
                    # Machine always gets positive scores for wins
                    scores[m] = 10
                else:
                    # Opponent always gets negative scores for wins
                    scores[m] = -10
                break
            scores[m] = self.eval_tree(opponent, depth)  # save the score and continue the game simulation
            self.clear(player, m)  # clear the evaluated move

        try:
            if depth == 1:
                return scores
            else:
                if player == 'machine':
                    # Machine always wants MAX score moves (the "max" of minimax)
                    return max(scores.itervalues())
                else:
                    # Opponent (human) always gets MIN score moves
                    return min(scores.itervalues())
        except ValueError:
            return 0  # We have a draw

    def winner(self, player):
        """Check to see if <player> has won the game"""

        # Get the occupied positions held by <player>
        occupied = self.__getattribute__(PLAYERS[player])
        # Loop over all 3-digit permutations of <player>'s positions, comparing each one against known win vectors.
        # If we find a match, we have a winner.
        for p in itertools.permutations(occupied, 3):
            if p in WIN_VECTORS:
                return p
        return False

    def winnable(self, player):
        """Test if the current game state is winnable by <player>.

        If true, return the winning position.  Obviously, if the game is winnable for <player>, it is also blockable for
        the opponent, so this same function may be used for either detection depending on whose turn it is.
        """

        # Get the occupied positions for the player
        occupied = self.__getattribute__(PLAYERS[player])
        # Get the occupied position for the opponent
        opp = self.__getattribute__(PLAYERS[self.switch_player(player)])
        # Loop frenzy. I'll buy lunch for whoever comes up with the list comprehension for this sucker. I gave up.
        for v in WIN_VECTORS:  # Loop the win vectors
            for perm in itertools.permutations(v, 2):  # Loop through all 2-digit permutations of each vector
                vector = list(perm)  # Listify each permutation
                for p in itertools.permutations(occupied, 2):  # Loop through all 2-digit permutations of occupied
                    if list(p) == vector:
                        # At this point, we know the player holds two positions that match one of the win vectors
                        # which means we have a possible winner.  We then return the position that will result in the
                        # win (or block, as the case may be).  Easy enough using some "set" magic.
                        win = list(set(v) - set(vector))[0]
                        # Now we make sure win move is not held by the opponent
                        if win not in opp:
                            return win
        return False

    @staticmethod
    def switch_player(player):
        """Return the opponent of <player>.  This becomes useful for the back-and-forth nature of minimax."""

        return [k for k, v in PLAYERS.iteritems() if k != player][0]

    def clear(self, player, pos):
        """Clear a given move from <player>'s occupied positions"""

        moves = self.__getattribute__(PLAYERS[player])
        moves.remove(pos)

    @classmethod
    def reset(cls):
        """Reset the game"""

        cls.x = []
        cls.o = []