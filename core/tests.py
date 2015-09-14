"""
Copyright (C) 2014 Ryan Hansen.  All rights reserved.
This source code (including its associated software) is owned by Ryan Hansen and
is protected by United States and international intellectual property law, including copyright laws, patent laws,
and treaty provisions.
"""

import unittest
from core.game import Game
from core.const import PLAYERS


class TicTacToeTest(unittest.TestCase):

    def setUp(self):
        self.board = Game()

    def tearDown(self):
        self.board.reset()

    def test_001(self):
        """Test the available move checker"""

        moves = self.board.available
        # Make sure all moves are available
        self.assertTrue(len(moves) == 9, 'Not all moves are available')
        self.assertTrue(moves == [0, 1, 2, 3, 4, 5, 6, 7, 8], 'Available moves do not match')

    def test_002(self):
        """Test position setter"""

        self.board.take('machine', 4)  # Machine takes center position
        moves = self.board.available
        self.assertTrue(len(moves) == 8, 'Position not taken')
        self.assertTrue(moves == [0, 1, 2, 3, 5, 6, 7, 8], 'Available moves do not match')

    def test_003(self):
        """Test win detection"""

        self.board.take('machine', 1)
        # At this point we shoulnd't have a winner yet
        self.assertFalse(self.board.winner('machine'), 'We have a winner')
        self.board.take('machine', 7)
        # Now the machine player should have won
        self.assertTrue(self.board.winner('machine'), '{0} is not the winner'.format(PLAYERS['machine']))
        self.assertTrue(self.board.winner('machine') == (1, 4, 7), 'Unexpected winning vector')

    def test_004(self):
        """Test win detection"""

        self.board.clear('machine', 1)
        # Now the machine player should have a winning move available
        self.assertTrue(self.board.winnable('machine') == 1, 'Exptected to be able to win')

    def test_005(self):
        """Test game evaulation -- Winning move"""

        self.board.take('human', 0)
        self.board.take('human', 3)
        move = self.board.eval_tree('machine')
        self.assertTrue(move == 1, 'Expected to choose position 1 for the win')

    def test_006(self):
        """Test game evaluation -- Blocking move"""

        Game.reset()
        self.board.take('human', 4)
        self.board.take('human', 2)
        self.board.take('machine', 0)
        self.board.take('machine', 1)
        move = self.board.eval_tree('machine')
        self.assertTrue(move == 6, 'Expected to choose position 6 for the block')

    def test_007(self):
        """Test game evaluation - minimax."""

        Game.reset()
        self.board.take('human', 0)
        self.board.take('human', 4)
        self.board.take('machine', 8)
        move = self.board.next_move()
        self.assertTrue(move == 2 or move == 6, 'Expected to choose position 2 or 6 to lead to a draw')