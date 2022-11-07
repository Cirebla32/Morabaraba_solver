from morabaraba.morabaraba_player import MorabarabaPlayer
from morabaraba.morabaraba_board import MorabarabaBoard
from morabaraba.morabaraba_action import MorabarabaAction, MorabarabaActionType
from morabaraba.morabaraba_rules import MorabarabaRules
from morabaraba.morabaraba_state import MorabarabaState
from core import Color
import random
import numpy as np


class AI(MorabarabaPlayer):
    name = "®©"

    def __init__(self, color):  
        super(AI, self).__init__(color)
        self.position = color.value
        self.inverse_board = MorabarabaBoard((7, 7))

    def play(self, state, remain_time):
        """ Return Morabara action.
            Example : an add to (0, 1) is equivalent to MorabarabaAction(action_type=MorabarabaActionType.ADD, to=(0, 1))
            Example : a move from (0, 1) to (0, 2) is equivalent to MorabarabaAction(action_type=MorabarabaActionType.MOVE, at=(0, 1), to=(0, 2))
            Example : a fly from (0, 1) to (0, 2) is equivalent to MorabarabaAction(action_type=MorabarabaActionType.FLY, at=(0, 1), to=(0, 2))
            Example : a steal at (0, 1) is equivalent to MorabarabaAction(action_type=MorabarabaActionType.STEAL, at=(0, 1))

        Utils:
            you can retrieve the coordinates of a cell through the alias or vice versa
            Example : Retrieve cell coordinates of b2 is equivalent to : state.get_board().coordinates('b2'), which return (1, 1)
            Example : Retrieve alias of cell with coordinates (1, 1) is equivalent to : state.get_board().names((1,1)), which return 'b2'  
    
        Args:
            action_type (MorabarabaActionType): The type of the performed action.
        """
        print(state.mill)
        board_ndArray = state.get_board()._board_state.__copy__()
        board_ndArray[board_ndArray == Color(-1)] = 2
        board_ndArray[board_ndArray == Color(1)] = Color(-1) 
        board_ndArray[board_ndArray == 2] = Color(1)
        self.inverse_board._board_state = board_ndArray
        _, act = self.minimax(state, 1, self.position)
        return act
        return MorabarabaRules.random_play(state, self.position)

    def is_a_mill_move(self, state, player, action):
        """Take the state, the player and his action and find if this action is a mill move. It returns the mills founded.

        Args:
            state (MorabarabaState): A state object from the Morabaraba game.
            action (MorabarabaAction): An action object from the Morabaraba game and containing the move.
            player (int): The number of the player making the move.

        Returns:
            bool: True if everything goes fine and the move was made. False is else.
        """
        board = state.get_board()
        act = action.get_action_as_dict()
        if(act['action_type'] == MorabarabaActionType.STEAL):
            cell = act['action']['at']
        else:
            cell = act['action']['to']
        player_mills = []
        if(player == -1):
            player_pieces = board.get_player_pieces_on_board(Color(player))
            opponent_pieces = self.inverse_board.get_player_pieces_on_board(Color(player))
        else:
            opponent_pieces = board.get_player_pieces_on_board(Color(-1 * player))
            player_pieces = self.inverse_board.get_player_pieces_on_board(Color(-1 * player))
        mills = board.mills()
        for mill in mills:
            if cell in mill:
                cpt = 0
                if((act['action_type'] == MorabarabaActionType.MOVE or act['action_type'] == MorabarabaActionType.FLY) and act['action']['at'] in mill):
                    cpt = -1
                for mill_cell in mill:
                    if mill_cell in player_pieces: cpt += 1
                    elif mill_cell in opponent_pieces: break
                if cpt == 2: player_mills.append(mill)
        
        is_mill = len(player_mills) > 0

        return [ is_mill , player_mills ]

    def minimax(self, state, d, player):
        if(d == 0 or MorabarabaRules.is_end_game(state)):
            return state.score[self.position] - state.score[-1 * self.position], MorabarabaRules.random_play(state, player)
            #results = SeegaRules.get_results(state)
            #if(results['tie']):
            #    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>TIE<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            #    return 0, None
            #elif(results['winner'] == self.position):
            #    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>WON<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            #    return results['score'][self.position], None
            #else:
            #    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>LOOSED<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            #    return -1 * results['score'][-1 * self.position], None
        else:
            # D É F E N S E
            opponent_possibilities = {}
            opponent_possibilities['score'] = []
            if(state.mill):
                #Empêcher ses mills par mes STEAL
                state_copy = MorabarabaState(state.get_board(), state.get_next_player())
                state_copy.set_latest_move(state.get_latest_move())
                state_copy.set_latest_player(state.get_latest_player())
                state_copy.score = dict(state.score)
                #state_copy.on_board = dict(state.on_board)
                #state_copy.rewarding_move = state.rewarding_move
                state_copy.just_stop = state.just_stop
                state_copy.boring_moves = state.boring_moves
                state_copy.mill = False
                state_copy.in_hand = state.in_hand.copy()
                state_copy.fly_case = state.fly_case
                state_copy.captured = state.captured
                state_copy.latest_player1_move = state.latest_player1_move.copy()
                state_copy.latest_player2_move = state.latest_player2_move.copy()
                state_copy.before_latest_player1_move= state.before_latest_player1_move.copy()
                state_copy.before_latest_player2_move= state.before_latest_player2_move.copy()
                state_copy.fly_moves = state.fly_moves

                opponent_possibilities['action'] = MorabarabaRules.get_player_actions(state_copy, player * -1)
            else:
                #Voir si je peux faire mill
                my_possibilities = {}
                my_possibilities['action'] = MorabarabaRules.get_player_actions(state, player)
                my_possibilities['score'] = []
                if(len(my_possibilities['action']) != 0):
                    for possibility in my_possibilities['action']:
                        _, mills = self.is_a_mill_move(state, player, possibility)
                        print(_, possibility)
                        my_possibilities['score'].append(len(mills))
                    sorted_scores = sorted(my_possibilities['score'])
                    for minNotNullScore in sorted_scores:
                        if(minNotNullScore):
                            return minNotNullScore, my_possibilities['action'][my_possibilities['score'].index(minNotNullScore)]


                #Empêcher ses mills par mes ADD, MOVE ou FLY
                opponent_possibilities['action'] = MorabarabaRules.get_player_actions(state, player * -1)
                opponent_possibilities['score'] = []
                opponent_mills_list = []
                if(len(opponent_possibilities['action']) != 0):
                    for possibility in opponent_possibilities['action']:
                        _, mills = self.is_a_mill_move(state, player * -1, possibility)
                        opponent_mills_list.append(mills)
                        opponent_possibilities['score'].append(len(mills))
                    maxScore = max(opponent_possibilities['score'])
                    if(maxScore):
                        actionToBlock = opponent_possibilities['action'][opponent_possibilities['score'].index(maxScore)].get_action_as_dict()['action']
                        
                        if(len(my_possibilities['action'] ) != 0):
                            if(my_possibilities['action'][0].get_action() == "ADD"):
                                return maxScore, MorabarabaAction(action_type=MorabarabaActionType.ADD, to=actionToBlock['to'])
                            elif(my_possibilities['action'][0].get_action() == "STEAL"):
                                for mills in opponent_mills_list[maxScore]:
                                    for mill in mills:
                                        for cell in mill:
                                            if(cell != actionToBlock['to']):
                                                return maxScore, MorabarabaAction(action_type=MorabarabaActionType.STEAL, at=cell)
                            else:
                                for possibility in my_possibilities['action']:
                                    if(possibility.get_action_as_dict()['action']['to'] == actionToBlock['to']):
                                        return maxScore, possibility


            # A T T A Q U E
            possibilities = {}
            possibilities['action'] = MorabarabaRules.get_player_actions(state, player)
            possibilities['score'] = []
            for possibility in possibilities['action']:
                print(">>>>>>>>>>>>>>>>>>>>",(possibility.get_action_as_dict()))
                state_copy = MorabarabaState(state.get_board(), state.get_next_player())
                state_copy.set_latest_move(state.get_latest_move())
                state_copy.set_latest_player(state.get_latest_player())
                state_copy.score = dict(state.score)
                #state_copy.on_board = dict(state.on_board)
                #state_copy.rewarding_move = state.rewarding_move
                state_copy.just_stop = state.just_stop
                state_copy.boring_moves = state.boring_moves
                state_copy.mill = state.mill
                state_copy.in_hand = state.in_hand.copy()
                state_copy.fly_case = state.fly_case
                state_copy.captured = state.captured
                state_copy.latest_player1_move = state.latest_player1_move.copy()
                state_copy.latest_player2_move = state.latest_player2_move.copy()
                state_copy.before_latest_player1_move= state.before_latest_player1_move.copy()
                state_copy.before_latest_player2_move= state.before_latest_player2_move.copy()
                state_copy.fly_moves = state.fly_moves
                MorabarabaRules.act(state_copy, possibility, player)
                score, _ = self.minimax(state_copy, d-1, state.get_next_player())
                #print(d, possibility, score)
                possibilities['score'].append(score)
            #print(possibilities['score'])
            if(len(possibilities['score']) == 0):
                if(player == self.position):
                    return -9999999, None
                else:
                    return 9999999, None
            #input(">>> ")
            if(player == self.position):
                choice = random.choice(AI.value_indexes(possibilities['score'], max(possibilities['score'])))
            else:
                choice = random.choice(AI.value_indexes(possibilities['score'], min(possibilities['score'])))
            return possibilities['score'][choice], possibilities['action'][choice]

    @staticmethod
    def value_indexes(liste, value):
        res = []
        for i in range(len(liste)):
            if(liste[i] == value):
                res.append(i)
        return res

    @staticmethod
    def only_steal_actions(actionList):
        res = []
        for action in actionList:
            if(action.get_action() == 'STEAL'):
                res.append(action)
        if(len(res) == 0):
            return False, actionList
        print(res)
        return True, res
