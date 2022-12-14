from morabaraba.morabaraba_player import MorabarabaPlayer
from morabaraba.morabaraba_board import MorabarabaBoard
from morabaraba.morabaraba_action import MorabarabaAction, MorabarabaActionType
from morabaraba.morabaraba_rules import MorabarabaRules
from morabaraba.morabaraba_state import MorabarabaState
from core import Color
import random
import numpy as np
from copy import deepcopy


class AI(MorabarabaPlayer):
    name = "TheCrewPhase2v3"

    def __init__(self, color):  
        super(AI, self).__init__(color)
        self.position = color.value
        self.inverse_board = MorabarabaBoard((7, 7))
        self.vip_square = None
        self.menaces = [
                {'soudure':(0,0),'horizontal':[(0,3),(0,6)],'vertical':[(3,0),(6,0)],'diagonal':[(1,1),(2,2)]},
                {'soudure':(0,6),'horizontal':[(0,0),(0,3)],'vertical':[(6,6),(3,6)],'diagonal':[(1,5),(2,4)]},
                {'soudure':(6,6),'horizontal':[(6,3),(6,0)],'vertical':[(3,6),(0,6)],'diagonal':[(5,5),(4,4)]},
                {'soudure':(6,0),'horizontal':[(6,3),(6,6)],'vertical':[(3,0),(0,0)],'diagonal':[(5,1),(4,2)]},
                {'soudure':(1,1),'horizontal':[(1,5),(1,3)],'vertical':[(2,1),(5,1)],'diagonal':[(2,2),(0,0)]},
                {'soudure':(1,5),'horizontal':[(1,1),(1,3)],'vertical':[(3,5),(5,5)],'diagonal':[(2,4),(0,6)]},
                {'soudure':(5,5),'horizontal':[(5,1),(5,3)],'vertical':[(3,5),(1,5)],'diagonal':[(4,4),(6,6)]},
                {'soudure':(5,1),'horizontal':[(5,5),(5,3)],'vertical':[(3,1),(1,1)],'diagonal':[(4,2),(6,0)]},
                {'soudure':(2,2),'horizontal':[(2,4),(2,3)],'vertical':[(3,2),(4,2)],'diagonal':[(1,1),(0,0)]},
                {'soudure':(2,4),'horizontal':[(2,2),(2,3)],'vertical':[(3,4),(4,4)],'diagonal':[(1,5),(0,6)]},
                {'soudure':(4,4),'horizontal':[(4,2),(4,3)],'vertical':[(3,4),(2,4)],'diagonal':[(5,5),(6,6)]},
                {'soudure':(4,2),'horizontal':[(4,4),(4,3)],'vertical':[(3,2),(2,2)],'diagonal':[(5,1),(6,0)]}
                ]

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
        board_ndArray = state.get_board()._board_state.__copy__()
        board_ndArray[board_ndArray == Color(-1)] = 2
        board_ndArray[board_ndArray == Color(1)] = Color(-1) 
        board_ndArray[board_ndArray == 2] = Color(1)
        self.inverse_board._board_state = board_ndArray
        _, act = self.notMinimax(state, self.position)
        return act

    @staticmethod
    def is_an_end_of_square(cell, board):
        if cell[0] == cell[1]:
            return True, 1
        elif cell[0] + cell[1] == board._board_state.shape[0]-1:
            return True, -1
        return False, 0

    @staticmethod
    def which_lines_pass_through(cell, board):
        #res = {"vertical":[cell], "horizontal":[cell]}
        res = {"vertical":[], "horizontal":[]}
        semi_shape = board._board_state.shape[0]//2
        #horizontal
        if cell[0] == semi_shape:
            a = range((abs(cell[1]-1) // cell[0]) * (cell[0]+1), (abs(cell[1]-1) // cell[0]) * (cell[0]+1) + cell[0])
        elif cell[0] > semi_shape:
            x = int(cell[0] - 2*((cell[0]-1)%semi_shape) - 2)
            a = range(x, x + 2*(semi_shape - x) + 1, semi_shape - x)
        else:
            x = int(cell[0])
            a = range(x, x + 2*(semi_shape - x) + 1, semi_shape - x)
        for i in a:
            if (cell[0], i) != cell:
                res["horizontal"].append((cell[0], i))
        #vertical
        if cell[1] == semi_shape:
            b = range((abs(cell[0]-1) // cell[1]) * (cell[1]+1), (abs(cell[0]-1) // cell[1]) * (cell[1]+1) + cell[1])
        elif cell[1] > semi_shape:
            x = int(cell[1] - 2*((cell[1]-1)%semi_shape) - 2)
            b = range(x, x + 2*(semi_shape - x) + 1, semi_shape - x)
        else:
            x = int(cell[1])
            b = range(x, x + 2*(semi_shape - x) + 1, semi_shape - x)
        for i in b:
            if (i, cell[1]) != cell:
                res["vertical"].append((i, cell[1]))
        #diagonal
        _, on_diagonal = AI.is_an_end_of_square(cell, board)
        if(on_diagonal):
            #res["diagonal"] = [cell]
            res["diagonal"] = []
            if(on_diagonal == 1): #La diagonale o?? pour (a, b), on a a == b
                c = [(i, i) for i in range((abs(cell[0]-1)//semi_shape) * semi_shape + abs(cell[0]-1)//semi_shape, (abs(cell[0]-1)//semi_shape) * semi_shape+abs(cell[0]-1)//semi_shape+semi_shape)]
            else:
                c = [(i, 2*semi_shape-i) for i in range((abs(cell[0]-1)//semi_shape) * semi_shape + abs(cell[0]-1)//semi_shape, (abs(cell[0]-1)//semi_shape) * semi_shape+abs(cell[0]-1)//semi_shape+semi_shape)]
            for i in c:
                if i != cell:
                    res["diagonal"].append(i)
        return res

    def is_making_mill(self, state, player, action):
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
            return [False, []]

        if(player == -1):
            player_pieces = board.get_player_pieces_on_board(Color(player))
            opponent_pieces = self.inverse_board.get_player_pieces_on_board(Color(player))
        else:
            opponent_pieces = board.get_player_pieces_on_board(Color(-1 * player))
            player_pieces = self.inverse_board.get_player_pieces_on_board(Color(-1 * player))

        cell = act['action']['to']
        crossroads = AI.which_lines_pass_through(cell, board)
        player_mills = []
        for axe in list(crossroads.keys()):
            cpt = 0
            for _cell in crossroads[axe]:
                if((act['action_type'] == MorabarabaActionType.MOVE or act['action_type'] == MorabarabaActionType.FLY) and act['action']['at'] in crossroads[axe]):
                    break
                if _cell in opponent_pieces:
                    cpt -= 1
                    break
                elif _cell in player_pieces:
                    cpt +=1
            if cpt == 1:
                crossroads[axe].append(cell)
                player_mills.append(crossroads[axe])

        is_making_mill = len(player_mills) > 0

        return [ is_making_mill , player_mills ]

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
            return [False, []]
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

    def solve_a_menace_from(self, player, state):
        if(player == -1):
            player_pieces = state.get_board().get_player_pieces_on_board(Color(player))
            opponent_pieces = self.inverse_board.get_player_pieces_on_board(Color(player))
        else:
            player_pieces = self.inverse_board.get_player_pieces_on_board(Color(-1 * player))
            opponent_pieces = state.get_board().get_player_pieces_on_board(Color(-1 * player))
        for menace in self.menaces:
            count=0
            for player_piece in player_pieces:
                if count>=2:
                    return True, menace['soudure']
                if player_piece in menace['horizontal']:
                    count+=1
                    for h_menace in menace['horizontal']:
                        if h_menace in opponent_pieces:
                            count-=1
                elif player_piece in menace['vertical']:
                    count+=1
                    for v_menace in menace['horizontal']:
                        if v_menace in opponent_pieces:
                            count-=1
                elif player_piece in menace['diagonal']:
                    count+=1
                    for d_menace in menace['horizontal']:
                        if d_menace in opponent_pieces:
                            count-=1
            if count>=2:
                return True, menace['soudure']
        return False, []

    @staticmethod
    def next_square_head(cell, board_shape):
        if sum(cell) == board_shape[0] - 1:
            return (cell[0], cell[0])
        elif cell[0] == cell[1]:
            return (board_shape[0] - 1 - cell[0], cell[1])
        elif cell[0] == board_shape[0]//2:
            return (cell[0] + (cell[0] - cell[1]), cell[1])
        return (cell[0], (cell[0] - cell[1]) + cell[1])

    @staticmethod
    def next_square_vertex(cell, board_shape):
        if sum(cell) == board_shape[0] - 1:
            return (cell[0], board_shape[0]//2)
        elif cell[0] == cell[1]:
            return (board_shape[0]//2, cell[1])
        elif cell[0] == board_shape[0]//2:
            return (cell[0] + (cell[0] - cell[1]), cell[1])
        return (cell[0], (cell[0] - cell[1]) + cell[1])

    @staticmethod
    def is_my_move_putting_me_in_danger(state, action, player):
        act = action.get_action_as_dict()
        if(act['action_type'] == "MOVE" or act['action_type'] == "FLY"):
            temp_state = deepcopy(state)
            MorabarabaRules.make_move(temp_state, action, player)
            opp_acts = MorabarabaRules.get_player_actions(temp_state, player * -1)
            cell = act['action']['at']
            for opp_act in opp_acts:
                if opp_act.get_action_as_dict()['action']['to'] == cell and self.is_a_mill_move(temp_state, player*-1, opp_act)[0]:
                    return True
            return False
        return False

    def which_actions_r_guessed_2_b_the_best(self, state, player):
        if(0):
            return 0, random_play(state, player)
        else:
            #premier coup
            if(len(state.get_board().get_player_pieces_on_board(Color(player))) == 0):
                return [MorabarabaRules.random_play(state, player)]
            # D ?? F E N S E
            opponent_possibilities = {}
            opponent_possibilities['score'] = []
            opponent_mills_list = []
            res = []
            if(state.mill):
                #Emp??cher ses mills par mes STEAL
                #Faire un deepcopy ?? la place
                """state_copy = MorabarabaState(state.get_board(), state.get_next_player())
                state_copy.set_latest_move(state.get_latest_move())
                state_copy.set_latest_player(state.get_latest_player())
                state_copy.score = dict(state.score)
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
                state_copy.fly_moves = state.fly_moves"""
                state_copy = deepcopy(state)
                opponent_possibilities['action'] = np.array(MorabarabaRules.get_player_actions(state_copy, player * -1))
                if(len(opponent_possibilities['action']) != 0):
                    for possibility in opponent_possibilities['action']:
                        _, mills = self.is_a_mill_move(state, player * -1, possibility)
                        opponent_mills_list.append(mills)
                        opponent_possibilities['score'].append(len(mills))
                    opponent_possibilities['score'] = np.array(opponent_possibilities['score'])
                    opponent_mills_list = np.array(opponent_mills_list)
                    max_score = opponent_possibilities['score'].max()
                    while(max_score):
                        if(opponent_possibilities['action'][0].get_action() == "ADD"):
                            for index in np.linspace(0, opponent_mills_list.size-1, opponent_mills_list.size, dtype=np.int8)[opponent_possibilities['score'] == max_score]:
                                action_to_block = opponent_possibilities['action'][index].get_action_as_dict()['action']
                                for mill in opponent_mills_list[index]:
                                    for cell in mill:
                                        if cell != action_to_block['to']:
                                            act = MorabarabaAction(action_type=MorabarabaActionType.STEAL, at=cell)
                                            if act not in res:
                                                res.append(MorabarabaAction(action_type=MorabarabaActionType.STEAL, at=cell))
                        else:
                            for dangerous_possibility in opponent_possibilities['action'][opponent_possibilities['score'] == max_score]:
                                act = MorabarabaAction(action_type=MorabarabaActionType.STEAL, at=dangerous_possibility.get_action_as_dict()['action']['at'])
                                if act not in res:
                                    res.append(act)
                        if len(res):
                            return res
                        else:
                            max_score -= 1
            else:
                #Voir si je peux faire mill
                my_possibilities = {}
                my_possibilities['action'] = np.array(MorabarabaRules.get_player_actions(state, player))
                np.random.shuffle(my_possibilities['action'])
                my_possibilities['score_mill'] = []
                my_possibilities['score_making_mill'] = []
                if(len(my_possibilities['action']) != 0):
                    for possibility in my_possibilities['action']:
                        _, mills = self.is_a_mill_move(state, player, possibility)
                        my_possibilities['score_mill'].append(len(mills))
                        _, mills_in_construction = self.is_making_mill(state, player, possibility)
                        my_possibilities['score_making_mill'].append(mills_in_construction)
                    my_possibilities['score_mill'] = np.array(my_possibilities['score_mill'])
                    if my_possibilities['score_mill'].any():
                        return my_possibilities['action'][my_possibilities['score_mill'] == my_possibilities['score_mill'][my_possibilities['score_mill']>0].min()].tolist()

                #Emp??cher ses mills par mes ADD, MOVE ou FLY
                opponent_possibilities['action'] = np.array(MorabarabaRules.get_player_actions(state, player * -1))
                if(len(opponent_possibilities['action']) != 0):
                    for possibility in opponent_possibilities['action']:
                        _, mills = self.is_a_mill_move(state, player * -1, possibility)
                        opponent_mills_list.append(mills)
                        opponent_possibilities['score'].append(len(mills))
                    opponent_possibilities['score'] = np.array(opponent_possibilities['score'])
                    max_score = opponent_possibilities['score'].max()
                    while(max_score):
                        if(opponent_possibilities['action'][0].get_action() == "ADD"):
                            for dangerous_possibility in opponent_possibilities['action'][opponent_possibilities['score'] == max_score]:
                                res.append(MorabarabaAction(action_type=MorabarabaActionType.ADD, to=dangerous_possibility.get_action_as_dict()['action']['to']))
                        else:
                            for dangerous_possibility in opponent_possibilities['action'][opponent_possibilities['score'] == max_score]:
                                cell = dangerous_possibility.get_action_as_dict()['action']['to']
                                for potential_solution in my_possibilities['action']:
                                    if potential_solution.get_action_as_dict()['action']['to'] == cell:
                                        res.append(potential_solution)
                        if len(res):
                            return res
                        else:
                            max_score -= 1

                    #Utiliser la technique du parcours de carr??s
                    #if(my_possibilities["action"][0].get_action() == "ADD"):
                    #    n = state.get_board().get_board_state().shape[0]
                    #    if(player == -1):
                    #        player_pieces = state.get_board().get_player_pieces_on_board(Color(player))
                    #        opponent_pieces = self.inverse_board.get_player_pieces_on_board(Color(player))
                    #    else:
                    #        player_pieces = self.inverse_board.get_player_pieces_on_board(Color(-1 * player))
                    #        opponent_pieces = state.get_board().get_player_pieces_on_board(Color(-1 * player))
                    #    board = state.get_board()
                    #    board_shape = board.get_board_state().shape
                    #    cell = self.vip_square
                    #    cpt = 0
                    #    for i in range(n+1):
                    #        cell = AI.next_square_vertex(cell, board_shape)
                    #        if cell in opponent_pieces: cpt -= 1
                    #        elif cell in player_pieces: cpt += 1
                    #    if cpt>0 and AI.next_square_vertex(self.vip_square, board_shape) not in opponent_pieces and AI.next_square_vertex(self.vip_square, board_shape) not in player_pieces:
                    #        self.vip_square = AI.next_square_head(self.vip_square, board_shape)
                    #        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 3")
                    #        return 0, MorabarabaAction(action_type=MorabarabaActionType.ADD, to=self.vip_square)
                    #    else:
                    #        print(self.vip_square)
                    #        vip_diagonal = AI.which_lines_pass_through(AI.next_square_head(self.vip_square, board_shape), board)["diagonal"]
                    #        for diaginal_hole in vip_diagonal:
                    #            cpt = 0
                    #            cell = diaginal_hole
                    #            for i in range(n+1):
                    #                if cell in opponent_pieces: cpt -= 1
                    #                elif cell in player_pieces: cpt += 1
                    #                cell = AI.next_square_vertex(cell, board_shape)
                    #            if cpt>=0 and diaginal_hole not in opponent_pieces and diaginal_hole not in player_pieces:
                    #                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 4")
                    #                self.vip_square = diaginal_hole
                    #                return 0, MorabarabaAction(action_type=MorabarabaActionType.ADD, to=self.vip_square)

                    #Voir s'il y a une double menace ?? emp??cher
                    #print("|||||", self.solve_a_menace_from(-1*self.position, state))
                    menace, cellToBock = self.solve_a_menace_from(-1*player, state)
                    if(menace):
                        for possibility in my_possibilities['action']:
                            if(possibility.get_action_as_dict()['action']['to'] == cellToBock):
                                res.append(possibility)
                        if len(res):
                            return res

                my_possibilities['score_making_mill'] = np.array(my_possibilities['score_making_mill'])
                if my_possibilities['score_making_mill'].any():
                    return my_possibilities['action'][my_possibilities['score_making_mill'] == my_possibilities['score_making_mill'].max()].tolist()

    def notMinimax(self, state, player):
        #Si c'est le premier coup
        if(len(state.get_board().get_player_pieces_on_board(Color(player))) == 0):
            if self.vip_square == None and sum(state.score.values()) == 0:
                n = state.get_board().get_board_state().shape[0]
                if(player == -1):
                    opponent_pieces = self.inverse_board.get_player_pieces_on_board(Color(player))
                else:
                    opponent_pieces = state.get_board().get_player_pieces_on_board(Color(-1 * player))
                middleSquare = (5, 1)
                if middleSquare not in opponent_pieces:
                    self.vip_square = middleSquare
                    return 0, MorabarabaAction(action_type=MorabarabaActionType.ADD, to=self.vip_square)
                a = random.choice([4, 6])
                self.vip_square = (a, n - a - 1)
                return 0, MorabarabaAction(action_type=MorabarabaActionType.ADD, to=self.vip_square)
        else:
            # D ?? F E N S E
            opponent_possibilities = {}
            opponent_possibilities['score'] = []
            opponent_mills_list = []
            if(state.mill):
                #Emp??cher ses mills par mes STEAL
                state_copy = deepcopy(state)
                opponent_possibilities['action'] = MorabarabaRules.get_player_actions(state_copy, player * -1)
                if(len(opponent_possibilities['action']) != 0):
                    for possibility in opponent_possibilities['action']:
                        _, mills = self.is_a_mill_move(state, player * -1, possibility)
                        opponent_mills_list.append(mills)
                        opponent_possibilities['score'].append(len(mills))
                    maxScore = max(opponent_possibilities['score'])
                    index_maxScore = opponent_possibilities['score'].index(maxScore)
                    if(maxScore):
                        actionToBlock = opponent_possibilities['action'][index_maxScore].get_action_as_dict()['action']
                        if(opponent_possibilities['action'][0].get_action() == "ADD"):
                            for mill in opponent_mills_list[index_maxScore]:
                                shuf_mill = mill.copy()
                                random.shuffle(shuf_mill)
                                for cell in shuf_mill:
                                    if(cell != actionToBlock['to']):
                                        act = MorabarabaAction(action_type=MorabarabaActionType.STEAL, at=cell)
                                        if MorabarabaRules.is_legal_move(state, act, player):
                                            return maxScore, act
                        else:
                            act = MorabarabaAction(action_type=MorabarabaActionType.STEAL, at=actionToBlock['at'])
                            if MorabarabaRules.is_legal_move(state, act, player):
                                return maxScore, act

                #Voir si supprimer un de ses joueurs m'aide ?? faire mill au prochain coup
                my_possibilities = {}
                my_possibilities['action'] = MorabarabaRules.get_player_actions(state, player)
                random.shuffle(my_possibilities['action'])
                my_possibilities['score_mill'] = []
                my_possibilities['score_making_mill'] = []
                if(len(my_possibilities['action']) != 0):
                    for possibility in my_possibilities['action']:
                        state_copy = deepcopy(state)
                        MorabarabaRules.make_move(state_copy, possibility, player)
                        board_ndArray = state_copy.get_board()._board_state.__copy__()
                        board_ndArray[board_ndArray == Color(-1)] = 2
                        board_ndArray[board_ndArray == Color(1)] = Color(-1) 
                        board_ndArray[board_ndArray == 2] = Color(1)
                        self.inverse_board._board_state = board_ndArray
                        cell = possibility.get_action_as_dict()['action']['at']
                        depth2_possibilities = MorabarabaRules.get_player_actions(state_copy, player)
                        for depth2_possibility in depth2_possibilities:
                            if depth2_possibility.get_action_as_dict()['action']['to'] == cell:
                                can_mill, mills = self.is_a_mill_move(state_copy, player, depth2_possibility)
                                if(can_mill):
                                    return 0, possibility
            else:
                #Voir si je peux faire mill
                my_possibilities = {}
                my_possibilities['action'] = MorabarabaRules.get_player_actions(state, player)
                random.shuffle(my_possibilities['action'])
                my_possibilities['score_mill'] = []
                my_possibilities['mills_in_construction'] = []
                my_possibilities['score_making_mill'] = []
                if(len(my_possibilities['action']) != 0):
                    for possibility in my_possibilities['action']:
                        _, mills = self.is_a_mill_move(state, player, possibility)
                        my_possibilities['score_mill'].append(len(mills))
                        _, mills_in_construction = self.is_making_mill(state, player, possibility)
                        my_possibilities['score_making_mill'].append(len(mills_in_construction))
                        my_possibilities['mills_in_construction'].append(mills_in_construction)
                    sorted_mills_scores = sorted(my_possibilities['score_mill'])
                    for minNotNullScore in sorted_mills_scores:
                        if(minNotNullScore):
                            return minNotNullScore, my_possibilities['action'][my_possibilities['score_mill'].index(minNotNullScore)]

                #Emp??cher ses mills par mes ADD, MOVE ou FLY
                opponent_possibilities['action'] = MorabarabaRules.get_player_actions(state, player * -1)
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
                                act = MorabarabaAction(action_type=MorabarabaActionType.ADD, to=actionToBlock['to'])
                                if MorabarabaRules.is_legal_move(state, act, player):
                                    return maxScore, act
                            else:
                                for possibility in my_possibilities['action']:
                                    if(possibility.get_action_as_dict()['action']['to'] == actionToBlock['to']):
                                        return maxScore, possibility

                    #Utiliser la technique du parcours de carr??s
                    if(my_possibilities["action"][0].get_action() == "ADD" and state.score[self.position] == 0):
                        n = state.get_board().get_board_state().shape[0]
                        if(player == -1):
                            player_pieces = state.get_board().get_player_pieces_on_board(Color(player))
                            opponent_pieces = self.inverse_board.get_player_pieces_on_board(Color(player))
                        else:
                            player_pieces = self.inverse_board.get_player_pieces_on_board(Color(-1 * player))
                            opponent_pieces = state.get_board().get_player_pieces_on_board(Color(-1 * player))
                        board = state.get_board()
                        board_shape = board.get_board_state().shape
                        cell = self.vip_square
                        cpt = 0
                        for i in range(n+1):
                            cell = AI.next_square_vertex(cell, board_shape)
                            if cell in opponent_pieces: cpt -= 1
                            elif cell in player_pieces: cpt += 1
                        if cpt>0 and AI.next_square_vertex(self.vip_square, board_shape) not in opponent_pieces and AI.next_square_vertex(self.vip_square, board_shape) not in player_pieces:
                            self.vip_square = AI.next_square_head(self.vip_square, board_shape)
                            act = MorabarabaAction(action_type=MorabarabaActionType.ADD, to=self.vip_square)
                            if MorabarabaRules.is_legal_move(state, act, player):
                                return 0, act
                        else:
                            vip_diagonal = AI.which_lines_pass_through(AI.next_square_head(self.vip_square, board_shape), board)["diagonal"]
                            for diaginal_hole in vip_diagonal:
                                cpt = 0
                                cell = diaginal_hole
                                for i in range(n+1):
                                    if cell in opponent_pieces: cpt -= 1
                                    elif cell in player_pieces: cpt += 1
                                    cell = AI.next_square_vertex(cell, board_shape)
                                if cpt>=0 and diaginal_hole not in opponent_pieces and diaginal_hole not in player_pieces:
                                    self.vip_square = diaginal_hole
                                    act = MorabarabaAction(action_type=MorabarabaActionType.ADD, to=self.vip_square)
                                    if MorabarabaRules.is_legal_move(state, act, player):
                                        return 0, act

                    #Voir s'il y a une double menace ?? emp??cher
                    menace, cellToBock = self.solve_a_menace_from(-1*self.position, state)
                    if(menace):
                        for possibility in my_possibilities['action']:
                            if(possibility.get_action_as_dict()['action']['to'] == cellToBock and AI.is_my_move_putting_me_in_danger(state, possibility, player) == False):
                                return 0, possibility

                #Voir si je peux construire un mill 
                sorted_making_mill_scores = sorted(my_possibilities['score_making_mill'], reverse=True)
                for maxNotNullScore in sorted_making_mill_scores:
                    if(maxNotNullScore):
                        act = my_possibilities['action'][my_possibilities['score_making_mill'].index(maxNotNullScore)]
                        if act.get_action_as_dict()["action_type"] == MorabarabaActionType.ADD: 
                            return 0, act
                        elif not AI.is_my_move_putting_me_in_danger(state, act, player):
                            mills_in_construction = my_possibilities['mills_in_construction'][my_possibilities['score_making_mill'].index(maxNotNullScore)]
                            #Voir si l'une de ces possibilit??s peut ??tre concr??tis??e au prochain tour
                            state_copy = deepcopy(state)
                            old_inverse = deepcopy(self.inverse_board._board_state)
                            MorabarabaRules.make_move(state_copy, act, player)
                            board_ndArray = state_copy.get_board()._board_state.__copy__()
                            board_ndArray[board_ndArray == Color(-1)] = 2
                            board_ndArray[board_ndArray == Color(1)] = Color(-1) 
                            board_ndArray[board_ndArray == 2] = Color(1)
                            self.inverse_board._board_state = board_ndArray
                            empty_cells = []
                            for mill in mills_in_construction:
                                for cell in mill:
                                    if state_copy.get_board().is_empty_cell(cell):
                                        empty_cells.append(cell)
                            depth2_possibilities = MorabarabaRules.get_player_actions(state_copy, player)
                            for depth2_possibility in depth2_possibilities:
                                if depth2_possibility.get_action_as_dict()['action']['to'] in empty_cells:
                                    can_mill, mills = self.is_a_mill_move(state_copy, player, depth2_possibility)
                                    if(can_mill):
                                        return 0, act
                            self.inverse_board._board_state = old_inverse
                        my_possibilities['action'].pop(my_possibilities['score_making_mill'].index(maxNotNullScore))
                        my_possibilities['mills_in_construction'].pop(my_possibilities['score_making_mill'].index(maxNotNullScore))
                        my_possibilities['score_making_mill'].pop(my_possibilities['score_making_mill'].index(maxNotNullScore))

            # A T T A Q U E si mon mouvement ne me met pas en danger
            for possibility in my_possibilities['action']:
                if(not AI.is_my_move_putting_me_in_danger(state, possibility, player)):
                    return 0, possibility

            return 0, MorabarabaRules.random_play(state, player)

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
        return True, res
