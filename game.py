'''game singleton module by Tigo.robotics 2022,2023'''
import pygame
from enum import Enum, auto
class GameState(Enum):
    STATE_PLAY=auto()
    STATE_SAVE=auto()
    STATE_LOAD=auto()
    STATE_CONFIG=auto()
    STATE_IDLE=auto()
    STATE_QUIT=auto()
    STATE_OVER=auto()
    
class PlayerState(Enum):
    PLAYER_NORMAL=auto()
    PLAYER_MENU_SET=auto()
    PLAYER_MENU_SHOW=auto()
    PLAYER_MENU_HIDE=auto()

class BuildState(Enum):
    PATH=auto()
    WALL=auto()
    TOWER=auto()

    MOVE_START=auto()
    MOVE_GOAL=auto()
    

class Game:
    #following are memory location for models
    monsters=[]
    towers=[]
    #screen and position related
    x_left_padding=100
    y_top_padding=100
    
    screen_width=1024
    screen_height=768
    disp_width=screen_width-x_left_padding
    disp_height=screen_height-y_top_padding
    
    mouse_last_action=1
    '''
    0 is left down
    1 is up
    2 is drag
    3 is move no drag
    4 is right down
    '''
    current_mode=0
    '''
    0 wall
    1 pathway
    2 goal
    3 start
    10~1000 and above defending tower series
    '''   
    screen=pygame.display.set_mode((screen_width,screen_height))
    loop=None

    state=GameState.STATE_IDLE
    player_state=PlayerState.PLAYER_NORMAL
    build_state=BuildState.WALL
    font =None
    buttons=dict()
    instructions='''drag to move: start and goal, right-click :choose tower, drag: empty blocks to create walls. q-quit game'''
    score=0 #game score
    life = 100 #need a limit of the game, when tower life reaches zero, game over.

    debug_rect=(0,0,1,1)
    