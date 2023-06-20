'''Control module by Tigo.robotics 2022,2023'''
import pygame
import asyncio
from game import Game, GameState, PlayerState, BuildState
from models import Grid
from pathfinder import AStar, Node
from runners import MonsterRunner
class Input:
    def __init__(self):
        print('control created')
        self.debug=0
        self.mouse_last_action=1 #default to mouse up upon entrance.
    #following an extracted layer of callback to make our code easier to read.
    def on_left_down(self):
        if self.debug:print('left clicked')
        mpos=pygame.mouse.get_pos()
        if Game.buttons['start'].collidepoint(mpos):
            Game.state=GameState.STATE_PLAY
            MonsterRunner.regenerate_monsters()
        elif Game.buttons['stop'].collidepoint(mpos):
            Game.state=GameState.STATE_IDLE
        elif Game.buttons['save'].collidepoint(mpos):
            Game.state=GameState.STATE_SAVE
        elif Game.buttons['load'].collidepoint(mpos):
            Game.state=GameState.STATE_LOAD
    def on_right_down(self):
        if self.debug:print('right clicked')
        Game.player_state=PlayerState.PLAYER_MENU_SET
    #this gets called inside the on_left_up or on_right_up methods.
    def on_mouse_up(self):
        if self.debug:print('on mouse up after show menu')
        Game.player_state=PlayerState.PLAYER_MENU_HIDE
        #process right mouse selection
        mpos=pygame.mouse.get_pos()
        if Game.buttons['wall'].collidepoint(mpos):
            Game.build_state=BuildState.WALL
            Game.current_mode=0
        if Game.buttons['path'].collidepoint(mpos):
            Game.build_state=BuildState.PATH
            Game.current_mode=1
        if Game.buttons['tower1'].collidepoint(mpos):
            Game.build_state=BuildState.TOWER
            Game.current_mode=10
        if Game.buttons['tower2'].collidepoint(mpos):
            Game.build_state=BuildState.TOWER
            Game.current_mode=11
    def on_left_up(self):
        if Game.player_state==PlayerState.PLAYER_MENU_SHOW:
            self.on_mouse_up()
            return
        if self.debug:print('left up')
        Grid.astar=Grid.update_position()
        #reset to wall mode for transient states/modes.
        if Game.current_mode in (2,3):
            Game.current_mode=0
            Game.build_state=BuildState.WALL
        Game.strt_pos=[-1,-1]
        Game.player_state=PlayerState.PLAYER_NORMAL
    def on_right_up(self):
        if Game.player_state==PlayerState.PLAYER_MENU_SHOW:
            self.on_mouse_up()
            return
        if self.debug:print('right up')
        Game.player_state=PlayerState.PLAYER_MENU_SHOW
    def on_move(self):
        if self.debug:print('moved')
    def on_start_drag(self):
        if self.debug:print('start dragging')
        grid_pos= Grid.conv_pos_to_xy(Grid.grid_size)
        Grid.strt_pos=grid_pos
        y,x=grid_pos
        if isinstance(Grid.astar.data[y][x],Node):
            if Grid.astar.data[y][x].name==Grid.astar.start:
                Game.current_mode=3 #begn point
                Game.build_state=BuildState.MOVE_START
            elif Grid.astar.data[y][x].name==Grid.astar.goal:
                Game.current_mode=2 #start point
                Game.build_state=BuildState.MOVE_GOAL
    def on_during_drag(self):
        if self.debug:print('during dragging')
        if   not Game.build_state==BuildState.MOVE_START and \
             not Game.build_state==BuildState.MOVE_GOAL  and \
             not Game.build_state==BuildState.TOWER:
            Grid.astar=Grid.update_position() #problem with start and goal dragging here.

    def on_end_drag(self):
        if self.debug:print('end dragging')
        Grid.astar=Grid.update_position()
    #=================main handler loop=========================
    async def handle(self):
        while True:
            if Game.state==GameState.STATE_OVER:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    pass
                elif keys[pygame.K_q]:
                    print('Stopping Game!')
                    Game.loop.stop()
                elif keys[pygame.K_RETURN]:
                    print('restart game')
                    Game.state=GameState.STATE_IDLE
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Game.loop.stop()
                await asyncio.sleep(0.01)
            else:
                #otherwise run normal checks    
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    pass
                elif keys[pygame.K_q]:
                    print('Stopping Game!')
                    Game.loop.stop()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Game.loop.stop()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.on_left_down()
                            Game.mouse_last_action=0
                        elif event.button == 3:
                            self.on_right_down()
                            Game.mouse_last_action=4
                    elif event.type == pygame.MOUSEBUTTONUP:
                        #follow this sequence: end_drag, mouse_up general check, then individual ups.
                        if Game.mouse_last_action==2:#move -> up == on end drag.
                            self.on_end_drag()
                            Game.mouse_last_action=1
                        if event.button == 1:
                            self.on_left_up()
                        elif event.button == 3:
                            self.on_right_up()
                        Game.mouse_last_action=1
                    elif event.type == pygame.MOUSEMOTION:
                        if Game.mouse_last_action == 0: #down then move == start dragging
                            self.on_start_drag()
                            Game.mouse_last_action=2
                        elif Game.mouse_last_action ==2:
                            self.on_during_drag()
                        else:
                            self.on_move()
                            Game.mouse_last_action=3
                            #does not change the last action here if no one start drag.
                await asyncio.sleep(0)