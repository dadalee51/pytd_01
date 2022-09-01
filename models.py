'''Model module ©️ Tigo.robotics 2022'''
#includes ai and player models, call algorithms 
#does not know about pygame, pure async model
import asyncio
import pygame
from game import Game, GameState
from pathfinder import AStar
from file_utils import FileAction
import math
from enum import Enum,auto
class Monster:
    def __init__(self,id,health,posx,posy,color,size, index, speed):
        self.id=id
        self.health=health #initial health
        self.posx=posx
        self.posy=posy
        self.color=color
        self.size=size
        self.index=index
        self.speed=speed
class Tower:
    class State(Enum): #state of tower is per object, cannot be global level. However it is still singleton.
        IDLE=auto()
        AIM=auto()
        FIRE=auto()
        RELOAD=auto()
    def tatan2(self,a,b):
        return round(math.degrees(math.atan2(a,b)),2)
    def __init__(self,id,posx,posy,color,size,effect_range):
        self.id=id
        self.power=1
        self.posx=posx
        self.posy=posy
        self.color=color
        self.size=size
        self.effect_range=effect_range
        self.aim_delay=0.01
        #dynamic changes
        self.aim_direction=[0,0]
        self.reload_time=100
        self.target=None
        self.fired=0
        self.state=Tower.State.IDLE
        self.reloading=0
    async def detect_monster(self): #IDLE to AIM
        for m in Game.monsters:
            mx=m.posx+Game.x_left_padding
            my=m.posy+Game.y_top_padding
            calc_range=math.sqrt((mx-self.posx)**2+(my-self.posy)**2)
            #print(calc_range)
            if calc_range<=self.effect_range:
                self.target=m
                self.aim_direction=self.tatan2(m.posx-self.posx, m.posy-self.posy)
                self.state=Tower.State.AIM
                await asyncio.sleep(self.aim_delay)
                return
        self.state=Tower.State.IDLE
    async def attack_monster(self): #AIM to FIRE
        if self.state==Tower.State.AIM:
            await asyncio.sleep(self.aim_delay)
            self.target.health-=self.power
            self.state=Tower.State.FIRE
    async def reload(self):
        if self.state==Tower.State.FIRE:
            await asyncio.sleep(self.aim_delay)
            self.state=Tower.State.RELOAD

#a tower defence game may no have main player on screen.
class Grid:
    grid_size=30
    grid_border_size=1
    grid_width=(Game.disp_width//grid_size)
    grid_height=(Game.disp_height//grid_size)
    goal_position=[1,4] #2
    begn_position=[4,1] #3
    strt_pos=[-1,-1] #mouse down log
    grid=[]
    
    astar=None
    
    start_x=-1
    start_y=-1
    goal_x=-1
    goal_y=-1
    current_path=[]

    @staticmethod
    def print_original_grid(grid):
        #print('try to print grid:',len(grid))
        for row in grid:
            for cell in row:
                print(cell,end='')
            print()

    @staticmethod
    def recreate_grid(grid):
        grid=Grid.init_grid()

    @staticmethod
    def conv_pos_to_xy(grid_size):
        pos = pygame.mouse.get_pos()
        if pos[0]>Game.screen_width+Game.x_left_padding or pos[1]>Game.screen_height+Game.y_top_padding: return -1,-1
        if pos[0]<Game.x_left_padding or pos[1]<Game.y_top_padding: return -1,-1
        x=(pos[0]-Game.x_left_padding)//(grid_size)
        y=(pos[1]-Game.y_top_padding)//(grid_size)
        return y,x
    
    #set the grid at mouse position to be the correct number.
    @staticmethod
    def update_position():
        grid_size=Grid.grid_size
        astar=Grid.astar
        grid=Grid.grid
        debug=0
        sy,sx=Grid.strt_pos
        ey,ex=Grid.conv_pos_to_xy(grid_size)
        if astar.data[ey][ex] == None: 
            pass
        elif (astar.goal==astar.data[ey][ex].name) or (astar.start==astar.data[ey][ex].name) :
            return astar
        if (ey,ex)==(-1,-1):
            return astar
        if Game.current_mode==0:
            grid[ey][ex]=0
        elif Game.current_mode==10:
            grid[ey][ex]=10
        else:
            grid[ey][ex]=Game.current_mode
            grid[sy][sx]=1
        if Game.current_mode==2:
            Grid.goal_position=ey,ex
        elif Game.current_mode==3:
            Grid.begn_position=ey,ex
        #Grid.recreate_grid(grid) #don't need to, just keep everywhere at one point.
        astar=AStar(grid) #this astar will be regenerated everytime the grid changes.
        return astar

    @staticmethod
    def init_grid():
        grid_height,grid_width=Grid.grid_height,Grid.grid_width
        grid=[]
        for y in range(grid_height+1):
            row=[]
            for x in range(grid_width+1):
                row+=[1]
            grid+=[row]
        gy,gx=Grid.goal_position
        by,bx=Grid.begn_position
        grid[gy][gx]=2
        grid[by][bx]=3
        return grid

    @staticmethod
    def to_pixel(v):
        return v*Grid.grid_size+Grid.grid_size//2

    @staticmethod
    def print_original_grid(grid):
        for row in grid:
            for cell in row:
                print(cell,end='')
            print()

