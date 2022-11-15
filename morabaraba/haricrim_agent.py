from morabaraba.morabaraba_player import MorabarabaPlayer
from morabaraba.morabaraba_board import MorabarabaBoard
from morabaraba.morabaraba_action import MorabarabaAction, MorabarabaActionType
from morabaraba.morabaraba_rules import MorabarabaRules
from morabaraba.morabaraba_state import MorabarabaState
from copy import deepcopy
from core import Color
import random
import numpy as np


class AI(MorabarabaPlayer):
    name = "Haricrim"

    def __init__(self, color):  
        super(AI, self).__init__(color)
        self.position = color.value
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
        
        
    # me=self.position
    # board = MorabarabaState.get_board()

        

        

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
        print(MorabarabaRules.is_making_mill(state.get_board(),1,(4,3)))

        return self.minimax(state ,self.position ,3)[1]  # 3 is the depth of the tree
        
    def evaluate(self, state, strategie):
        """ Return the evaluation of a state for the game.
            prend en argument state et la strategie en cours, et retourne l'evaluation de ce state en fonction de la strategie
            pour la phase de defense, on joue sur le nombre de mills et la possibilité de bloquer l'adversaire(stuck)
            pour la phase d'attaque , on joue sur les pions qu'il reste en jeu
        """  
        stuck=0
        if strategie=='defense':
            all_my_mills = state.get_board().player_mills(self.position)
            all_adv_mills = state.get_board().player_mills(-self.position)
            if MorabarabaRules.is_player_stuck(state, -self.position):
                stuck=np.inf
            return len(all_my_mills) - len(all_adv_mills) + stuck + self.solve_a_menace_from(state)[2]*10   
        
        if strategie=='attack':
            my_pieces_on_board=state.get_board().get_player_pieces_on_board(Color(self.position))
            adv_pieces_on_board=state.get_board().get_player_pieces_on_board(Color(-self.position))
            if MorabarabaRules.is_player_stuck(state, -self.position):
                stuck=np.inf
            return len(my_pieces_on_board) - len(adv_pieces_on_board) + stuck + self.solve_a_menace_from(state)[2]*10   
        
    
        
        
    def strategie(self,state):
        """ Return the best strategie for the game.
            arguments:state
            retourne: 'defense' or 'attack' en fonction du nombre de pions qu'on a en main, ce qui indique la phase actuelle du jeu 
        """  
        in_my_hand=state.get_player_info(self.position)['in_hand'] #maybe une erreur de synthaxe ici
        if in_my_hand==0:
            return 'attack'
        else:
            return 'defense'
        
    def solve_a_menace_from(self, state):
        # if(player == -1):
        #     player_pieces = state.get_board().get_player_pieces_on_board(Color(player))
        #     opponent_pieces = self.inverse_board.get_player_pieces_on_board(Color(player))
        # else:
        #     player_pieces = self.inverse_board.get_player_pieces_on_board(
        #         Color(-1 * player))
        #     opponent_pieces = state.get_board().get_player_pieces_on_board(Color(-1 * player))
        
        player_pieces = state.get_board().get_player_pieces_on_board(Color(self.position))
        opponent_pieces = state.get_board().get_player_pieces_on_board(Color(-self.position))
        for menace in self.menaces:
            count = 0
            for player_piece in player_pieces:
                if count >= 2:
                    return True, menace['soudure'], count
                if player_piece in menace['horizontal']:
                    count += 1
                    for h_menace in menace['horizontal']:
                        if h_menace in opponent_pieces:
                            count -= 1
                elif player_piece in menace['vertical']:
                    count += 1
                    for v_menace in menace['horizontal']:
                        if v_menace in opponent_pieces:
                            count -= 1
                elif player_piece in menace['diagonal']:
                    count += 1
                    for d_menace in menace['horizontal']:
                        if d_menace in opponent_pieces:
                            count -= 1
            if count >= 2:
                return True, menace['soudure'],count
        return False, [],count


    def possibilities2(self,state):
        """ Return all the possibilities for the game.
            prend en argument state et retourne toutes les possibilités d'actions du joueur en cours(self.position).
            ca prend le state, le copie, et applique toutes les actions possibles sur la copie, et retourne une liste
            de tous les states qui en resultent avec les actions qui les ont causés
        """
        possibilities2=[]
        for move  in MorabarabaRules.get_player_actions(state, self.position):
            temp_state = deepcopy(state)
            MorabarabaRules.act(temp_state, move, self.position)
            possibilities2.append([temp_state,'0', move])
            
        return possibilities2
    
    
    def minimax(self, state, maximizingPlayer, depth, alpha=np.inf, beta=-np.inf):
        """ Return the best move for the game.
        """  
        # count=[0,0]
        if depth == 0 or MorabarabaRules.is_end_game(state):
            # print('depth', depth)
            return self.evaluate(state, self.strategie(state)),None

        if maximizingPlayer==self.position:
            maxEval = -np.inf
            best_move = None
            # count[0]+=1
            # print('depth', depth)
            for move in self.possibilities2(state):
                # count[1]+=1
                evaluation = self.minimax(move[0], -self.position, depth - 1, alpha=np.inf, beta=-np.inf )[0]
                # print('evaluation',evaluation, 'move', move)
                
                # print('count',count)
                maxEval = max(maxEval, evaluation)
                if maxEval==evaluation:
                    best_move=move[2]
                # alpha = max(alpha, maxEval)
                # if maxEval >= beta:
                #     print('beta <= alpha, break')
                #     break
            # print('alpha', alpha)
            print('maxEval',maxEval,'bestmove = ', best_move)
            
            return maxEval, best_move

        else: # Minimizing player
            print('depth', depth)
            print('min')
            minEval = np.inf
            best_move = None
            for move in self.possibilities2(state):
                evaluation = self.minimax(move[0], self.position, depth - 1, alpha=np.inf, beta=-np.inf )[0]
                print('evaluation', evaluation, 'move', move)
                minEval = min(minEval, evaluation)
                if minEval==evaluation:
                    best_move=move[2]
                # beta = min(beta, minEval)
                # if maxEval <= alpha:
                #     print('maxEval <= alpha, break')
                #     break
            # print('beta', beta)
            print('minEval',minEval,'bestmove = ', best_move)
            # print('minim')
            return minEval, best_move
        
    ############################################################################################################
    
    def evaluate_possibilities(self, possibilities, strategie):
        """ Return the evaluation of all the possibilities for the game.
        """
        evaluations = []
        for possibility in possibilities:
            evaluations.append(
                [self.evaluate(possibility[0], strategie), possibility[1]])
        return evaluations

    def possibilities(self,state):
        """ Return the possibilities for the game."""
        possibilities=[]
        if state.get_player_info(self.position)['in_hand']==0:
            for piece in state.get_board().get_player_pieces_on_board(Color(self.position)):
                for move in state.get_board().get_effective_cell_moves(piece):
                    temp_state = deepcopy(state)
                    MorabarabaRules.act(temp_state, MorabarabaAction(action_type=MorabarabaActionType.MOVE, at=piece, to=move), self.position)
                    possibilities.append([temp_state,piece,MorabarabaAction(action_type=MorabarabaActionType.MOVE, at=piece, to=move)])
        
        elif state.get_player_info(self.position)['in_hand']>0:
            for piece in state.get_board().get_all_empty_cells():
                temp_state = deepcopy(state)
                MorabarabaRules.act(temp_state, MorabarabaAction(action_type=MorabarabaActionType.ADD, to=piece), self.position)
                possibilities.append([temp_state,piece,MorabarabaAction(action_type=MorabarabaActionType.ADD, to=piece)])
                
        elif len(state.get_board().get_player_pieces_on_board(Color(self.position)))<=3:
            for piece in state.get_board().get_player_pieces_on_board(Color(self.position)):
                for move in state.get_board().get_all_empty_cells():
                    temp_state = deepcopy(state)
                    # temp_piece = temp_state.get_board().get_player_pieces_on_board(Color(self.position))
                    MorabarabaRules.act(temp_state, MorabarabaAction(action_type=MorabarabaActionType.FLY, at=piece, to=move), self.position)
                    possibilities.append([temp_state,piece,MorabarabaAction(action_type=MorabarabaActionType.FLY, at=piece, to=move)])
                    # possibilities.append(temp_piece)      
        return possibilities
    
    # def get_best_move(self, state, strategie):
    #     """ Return the best move for the game.
    #     """
    #     depth = 3
    #     alpha=  np.inf
    #     beta= -np.inf
    #     bestMove = None
    #     bestScore = -np.inf
    #     for move in state.get_possible_moves():
    #         score = self.minimax(state, depth, alpha, beta)
    #         if score > bestScore:
    #             bestScore = score
    #             bestMove = move
    #     return bestMove
        
        
        
                
    
        
    
        
        
        