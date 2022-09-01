'''Visual module ©️ Tigo.robotics 2022'''
#provide several layers of visuals in this code.
#includes background, foregrounds, text, also button appearances
import pygame
from game import Game, PlayerState
from models import Monster,Grid, Tower
from enum import Enum, auto
class Settings():
    MENU_HEIGHT=150
    MENU_WIDTH=140
    BUTTON_WIDTH=120
    BUTTON_HEIGHT=20

class Layer:
    def __init__(self,sw,sh):
        self.sf=pygame.Surface([sw,sh], pygame.SRCALPHA, 32)
        self.sf=self.sf.convert_alpha()

    #buttons could be dynamic
    def create_button(self, name, disptext,color,x_off, y_off):
        text = Game.font.render(disptext, True, (0,0,0))
        the_b = pygame.draw.rect(self.sf,color,(x_off,y_off,Settings.BUTTON_WIDTH,Settings.BUTTON_HEIGHT))
        Game.buttons[name]=the_b
        self.sf.blit(text,(x_off+30,y_off+5,60,40))

class Background(Layer):
    def draw_grid(self):
        for j in range(Grid.grid_height+1):
            for i in range(Grid.grid_width+1):
                ncolr=(0,0,0)
                if Grid.grid[j][i]==10:
                    #tower
                    ncolr=(255,255,0)
                elif Grid.astar.data[j][i]:
                    ncolr=(255,255,255)
                    if Grid.astar.data[j][i].name==Grid.astar.start:
                        Grid.start_x=i
                        Grid.start_y=j
                        ncolr=(0,255,0)
                    elif Grid.astar.data[j][i].name==Grid.astar.goal:
                        ncolr=(255,0,0)
                        Grid.goal_x=i
                        Grid.goal_y=j
                    
                pygame.draw.rect(Game.screen,ncolr,(Game.x_left_padding+i*Grid.grid_size,\
                                               Game.y_top_padding+j*Grid.grid_size,\
                                               Grid.grid_size-Grid.grid_border_size,\
                                               Grid.grid_size-Grid.grid_border_size))
        self.create_button('start','StartWave',(50,255,0),0,30)
        self.create_button('stop','StopWave',(150,10,10),140,30)
        self.create_button('save','SaveMap',(50,10,200),320,30)
        self.create_button('load','LoadMap',(200,200,50),460,30)

    #umbrella draw function
    def draw(self):
        Game.screen.fill((30,30,30))
        self.draw_grid()
        Game.screen.blit(self.sf,(0,0))

class Foreground(Layer):
    def __init__(self, sw,sh):
        self.player_menu_pos=pygame.mouse.get_pos()
        super().__init__(sw,sh)
        
    def draw_monsters(self):
        for m in Game.monsters:
            if m.health>0:
                pygame.draw.circle(self.sf,m.color,(Game.x_left_padding+m.posx,Game.y_top_padding+m.posy),m.size)
  
    def draw_towers(self):
        px,py=Game.x_left_padding,Game.y_top_padding
        for t in Game.towers:
            pad=Grid.grid_size//2-t.size//2
            pygame.draw.rect(self.sf,t.color, (pad+t.posx, pad+t.posy,t.size,t.size))
            #then process each tower's state:
            if t.state==Tower.State.AIM:
                #pygame.draw.line(self.sf,t.color,(pad+t.posx,pad+t.posy),(px+t.target.posx,py+t.target.posy))
                pass
            elif t.state==Tower.State.FIRE:
                pygame.draw.line(self.sf,(0,255,0),(pad+t.posx,pad+t.posy),(px+t.target.posx,py+t.target.posy),width=5)
            elif t.state==Tower.State.RELOAD:
                pass
    def draw_text(self):
        text = Game.font.render(Game.instructions, True, (255,255,50))
        Game.screen.blit(text,(0,0,30,30))

    def draw_path(self):
        for p in Grid.current_path:
            ncolr=(0,255,255,100)
            pygame.draw.rect(self.sf,ncolr,(Game.x_left_padding+p.x*Grid.grid_size,\
                                                Game.y_top_padding+p.y*Grid.grid_size,\
                                                Grid.grid_size-Grid.grid_border_size,\
                                                Grid.grid_size-Grid.grid_border_size))
        if Game.current_mode in (2,3):
            ncolr=(0,0,0)
            if Game.current_mode==2: #goal
                ncolr=(255,0,0)
            if Game.current_mode==3: #start
                ncolr=(0,255,0)                                
            p=Grid.conv_pos_to_xy(Grid.grid_size)
            pygame.draw.rect(self.sf,ncolr,(Game.x_left_padding+p[1]*Grid.grid_size,\
                                                Game.y_top_padding+p[0]*Grid.grid_size,\
                                                Grid.grid_size-Grid.grid_border_size,\
                                                Grid.grid_size-Grid.grid_border_size))
    
    def draw_player_menu_set(self):
        mpos=self.player_menu_pos=pygame.mouse.get_pos()


    def draw_player_menu_show(self):
        color=(45,45,67)
        mpos=self.player_menu_pos
        if mpos[1]>Game.screen_height-Settings.MENU_HEIGHT:
            mpos=mpos[0],Game.screen_height-Settings.MENU_HEIGHT
        pygame.draw.rect(self.sf,color,(mpos[0],mpos[1],Settings.MENU_WIDTH,Settings.MENU_HEIGHT))
        self.create_button('path','CreatePath',(200,200,200),mpos[0]+10,mpos[1]+10)
        self.create_button('wall','CreateWall',(200,200,200),mpos[0]+10,mpos[1]+35)
        self.create_button('tower1','BasicTower',(200,200,200),mpos[0]+10,mpos[1]+60)

    #umbrella draw function
    def draw(self):
        self.sf.fill((0,0,0,0))
        #draw solved pathway - is it allowed here?
        Grid.current_path=Grid.astar.solve()
        self.draw_path()
        self.draw_towers()
        self.draw_monsters()
        self.draw_text()
        if Game.player_state==PlayerState.PLAYER_MENU_SET:
            self.draw_player_menu_set()
        elif Game.player_state==PlayerState.PLAYER_MENU_SHOW:
            self.draw_player_menu_show()

        Game.screen.blit(self.sf,(0,0))
