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

# menace_square1={'horizontal' :[[(0,0),(0,3)],[(6,0),(6,3)]],
#                  'vertical'  :[[(0,0),(3,0)],[(0,6),(3,6)]],
#                  'diagonal'  :[[(1,1),(2,2)],[(1,5),(2,4)],[(5,1),(4,2)],[(4,4),(5,5)]],
#                  'soudure'   :[(0,0),(0,6),(6,0),(6,6)]}

# menace_square2={'horizontal':[[(0,3),(0,6)],[(6,3),(6,6)]]}
menace1={'soudure':(0,0),'horizontal':[(0,3),(0,6)],'vertical':[(3,0),(6,0)],'diagonal':[(1,1),(2,2)]}
menace2={'soudure':(0,6),'horizontal':[(0,0),(0,3)],'vertical':[(6,6),(3,6)],'diagonal':[(1,5),(2,4)]}
menace3={'soudure':(6,6),'horizontal':[(6,3),(6,0)],'vertical':[(3,6),(0,6)],'diagonal':[(5,5),(4,4)]}
menace4={'soudure':(6,0),'horizontal':[(6,3),(6,6)],'vertical':[(3,0),(0,0)],'diagonal':[(5,1),(4,2)]}
menace5={'soudure':(1,1),'horizontal':[(1,5),(1,3)],'vertical':[(2,1),(5,1)],'diagonal':[(2,2),(0,0)]}
menace6={'soudure':(1,5),'horizontal':[(1,1),(1,3)],'vertical':[(3,5),(5,5)],'diagonal':[(2,4),(0,6)]}
menace7={'soudure':(5,5),'horizontal':[(5,1),(5,3)],'vertical':[(3,5),(1,5)],'diagonal':[(4,4),(6,6)]}
menace8={'soudure':(5,1),'horizontal':[(5,5),(5,3)],'vertical':[(3,1),(1,1)],'diagonal':[(4,2),(6,0)]}
menace9={'soudure':(2,2),'horizontal':[(2,4),(2,3)],'vertical':[(3,2),(4,2)],'diagonal':[(1,1),(0,0)]}
menace10={'soudure':(2,4),'horizontal':[(2,2),(2,3)],'vertical':[(3,4),(4,4)],'diagonal':[(1,5),(0,6)]}
menace11={'soudure':(4,4),'horizontal':[(4,2),(4,3)],'vertical':[(3,4),(2,4)],'diagonal':[(5,5),(6,6)]}
menace12={'soudure':(4,2),'horizontal':[(4,4),(4,3)],'vertical':[(3,2),(2,2)],'diagonal':[(5,1),(6,0)]}
menaces=[menace1,menace2,menace3,menace4,menace5, menace6, menace7, menace8, menace9, menace10, menace11, menace12]


adv_pieces_on_board=MorabarabaBoard.get_player_pieces_on_board(Color(-me))

def defence_against_menace(pieces):
    blockers=[]
    for menace in menaces:
        count=0
        for piece in pieces:
            if piece in menace['horizontal']:
                count+=1
            elif piece in menace['vertical']:
                count+=1
            elif piece in menace['diagonal']:
                count+=1
        if count>=2:
            blockers.append(menace['soudure'])
    return blockers

a_jouer=defence_against_menace(adv_pieces_on_board)

# def defence_against_menace(pieces):
#     count1={'x':0,'y':0,'z':0}
#     count2={'x':0,'y':0,'z':0}
#     count3={'x':0,'y':0,'z':0}
#     count4={'x':0,'y':0,'z':0}
#     blocker=[]
#     for piece in pieces:
#         if piece in menace_square1['horizontal'][0]:
#             count1['x']+=1
#         if piece in menace_square1['vertical'][0]:
#             count1['y']+=1
#         if piece in menace_square1['diagonal'][0]:
#             count1['z']+=1
            
#         if piece in menace_square1['horizontal'][0]:
#             count2['x']+=1
#         if piece in menace_square1['vertical'][1]:
#             count2['y']+=1
#         if piece in menace_square1['diagonal'][1]:
#             count2['z']+=1
            
#         if piece in menace_square1['horizontal'][1]:
#             count3['x']+=1
#         if piece in menace_square1['vertical'][0]:
#             count3['y']+=1
#         if piece in menace_square1['diagonal'][2]:
#             count3['z']+=1
            
#         if piece in menace_square1['horizontal'][1]:
#             count4['x']+=1
#         if piece in menace_square1['vertical'][1]:
#             count4['y']+=1
#         if piece in menace_square1['diagonal'][3]:
#             count4['z']+=1
            
#         if count1['x']>=1 and count1['y']>=1 or count1['x']>=1 and count1['z']>=1 or count1['y']>=1 and count1['z']>=1:
#             blocker.append(menace_square1['soudure'][0])
#         if count2['x']>=1 and count2['y']>=1 or count2['x']>=1 and count2['z']>=1 or count2['y']>=1 and count2['z']>=1:
#             blocker.append(menace_square1['soudure'][1])
#         if count3['x']>=1 and count3['y']>=1 or count3['x']>=1 and count3['z']>=1 or count3['y']>=1 and count3['z']>=1:
#             blocker.append(menace_square1['soudure'][2])
#         if count4['x']>=1 and count4['y']>=1 or count4['x']>=1 and count4['z']>=1 or count4['y']>=1 and count4['z']>=1:
#             blocker.append(menace_square1['soudure'][3]) 
        
#     return blocker