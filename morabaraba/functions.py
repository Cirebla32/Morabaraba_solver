from morabaraba.morabaraba_player import MorabarabaPlayer
from morabaraba.morabaraba_board import MorabarabaBoard
from morabaraba.morabaraba_action import MorabarabaAction, MorabarabaActionType
from morabaraba.morabaraba_rules import MorabarabaRules
from morabaraba.morabaraba_state import MorabarabaState
from core import Color


# menace1=[{(0,0),(0,6),(6,6)},[(0,6),(6,6),(6,0)],[(6,6),(6,0),(0,0)],[(6,0),(0,0),(0,6)],
#          [(1,1),(1,5),(5,5)],[(1,5),(5,5),(5,1)],[(5,5),(5,1),(1,1)],[(5,1),(1,1),(1,5)],
#          [(2,2),(2,4),(4,4)],[(2,4),(4,4),(4,2)],[(4,4),(4,2),(2,2)],[(4,2),(2,2),(2,4)]]
me=MorabarabaPlayer.position
board = MorabarabaState.get_board()

menace_square1={'horizontal':[[(0,0),(0,3)],[(6,0),(6,3)]],
                 'vertical'  :[[(0,0),(3,0)],[(0,6),(3,6)]],
                 'diagonal'  :[[(1,1),(2,2)],[(1,5),(2,4)],[(5,1),(4,2)],[(4,4),(5,5)]],
                 'soudure'   :[(0,0),(0,6),(6,0),(6,6)]}

adv_pieces_on_board=MorabarabaBoard.get_player_pieces_on_board(Color(-me))


def defence_against_menace(pieces):
    count1={'x':0,'y':0,'z':0}
    count2={'x':0,'y':0,'z':0}
    count3={'x':0,'y':0,'z':0}
    count4={'x':0,'y':0,'z':0}
    blocker=[]
    for piece in pieces:
        if piece in menace_square1['horizontal'][0]:
            count1['x']+=1
        if piece in menace_square1['vertical'][0]:
            count1['y']+=1
        if piece in menace_square1['diagonal'][0]:
            count1['z']+=1
            
        if piece in menace_square1['horizontal'][0]:
            count2['x']+=1
        if piece in menace_square1['vertical'][1]:
            count2['y']+=1
        if piece in menace_square1['diagonal'][1]:
            count2['z']+=1
            
        if piece in menace_square1['horizontal'][1]:
            count3['x']+=1
        if piece in menace_square1['vertical'][0]:
            count3['y']+=1
        if piece in menace_square1['diagonal'][2]:
            count3['z']+=1
            
        if piece in menace_square1['horizontal'][1]:
            count4['x']+=1
        if piece in menace_square1['vertical'][1]:
            count4['y']+=1
        if piece in menace_square1['diagonal'][3]:
            count4['z']+=1
            
        if count1['x']>=1 and count1['y']>=1 or count1['x']>=1 and count1['z']>=1 or count1['y']>=1 and count1['z']>=1:
            blocker.append(menace_square1['soudure'][0])
        if count2['x']>=1 and count2['y']>=1 or count2['x']>=1 and count2['z']>=1 or count2['y']>=1 and count2['z']>=1:
            blocker.append(menace_square1['soudure'][1])
        if count3['x']>=1 and count3['y']>=1 or count3['x']>=1 and count3['z']>=1 or count3['y']>=1 and count3['z']>=1:
            blocker.append(menace_square1['soudure'][2])
        if count4['x']>=1 and count4['y']>=1 or count4['x']>=1 and count4['z']>=1 or count4['y']>=1 and count4['z']>=1:
            blocker.append(menace_square1['soudure'][3]) 
        
    return blocker