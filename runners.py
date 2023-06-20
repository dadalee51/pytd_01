'''class for monsters and towers to react - copyright 2022 Tigo.Robotics'''
#runners are in charge of handle state changes, game dynamics, algorithms in realtime.
from models import Monster, Tower
from game import Game, GameState
from models import Grid, MonsterState
import asyncio
from pathfinder import AStar
from file_utils import FileAction
class TowerRunner:
    def __init__(self):
        self.tower_created=0
        self.tower_updated=0
    def create_towers(self):
        #create tower from grid numbers
        if self.tower_created: return
        for j,row in enumerate(Grid.grid):
            for i,cell in enumerate(row):
                if cell >= 10 and cell <=1000:
                    if cell==10:
                        twr=Tower('tower1'+str(i)+str(j),Game.x_left_padding+Grid.grid_size*i,Game.y_top_padding+Grid.grid_size*j,(100,0,100),10,100)
                        twr.type=0
                    elif cell==11:
                        twr=Tower('tower2'+str(i)+str(j),Game.x_left_padding+Grid.grid_size*i,Game.y_top_padding+Grid.grid_size*j,(100,50,50),10,100)
                        twr.power=20
                        twr.type=1
                    Game.towers.append(twr)
                     #go through all towers
        for t in Game.towers:
            Game.loop.create_task(t.detect_monster())
            Game.loop.create_task(t.attack_monster())
            Game.loop.create_task(t.reload())
        self.tower_created=1
    def update_towers(self):
        #add towers to list and activate them
        pass

    async def run(self):
        while True:
            if Game.state==GameState.STATE_IDLE:
                #idle state, remove all tower models
                Game.towers=[]
                self.tower_created=0  
            elif Game.state==GameState.STATE_PLAY:
                self.create_towers()
            await asyncio.sleep(0)


        
class MonsterRunner:
    def __init__(self):
        pass

    @staticmethod
    def regenerate_monsters():
        m =Monster('aMon', 100,Grid.start_x*Grid.grid_size,Grid.start_y*Grid.grid_size, (50,0,50), 5, 1, 1)
        m2 =Monster('bMon', 100,Grid.start_x*Grid.grid_size,Grid.start_y*Grid.grid_size, (50,0,50), 5, 1, 1)
        m2.speed=5
        m2.color=(255,0,0)
        m2.size=10
        Game.monsters.append(m)
        Game.monsters.append(m2)
    #produce and track monsters
    async def run(self):
        while True:
            if Game.state==GameState.STATE_IDLE:
                for e in Game.monsters:
                    e.posx=Grid.start_x*Grid.grid_size+Grid.grid_size/2
                    e.posy=Grid.start_y*Grid.grid_size+Grid.grid_size/2
                    e.index=1
                Game.life=100 #reset to 100
            elif Game.state==GameState.STATE_PLAY:
                for e in Game.monsters:
                    if e.health<0:
                        Game.score+=1
                        Game.monsters.remove(e)
                        continue
                    if e.index >= len(Grid.current_path):continue
                    next_target = Grid.current_path[e.index] #node
                    dx=Grid.to_pixel(next_target.x)-e.posx
                    dy=Grid.to_pixel(next_target.y)-e.posy
                    if dx>0:mx=1
                    else: mx=-1
                    if dy>0:my=1
                    else: my=-1
                    if abs(dx)<e.speed: e.posx+=mx
                    else: e.posx+=mx*e.speed
                    if abs(dy)<e.speed: e.posy+=my
                    else: e.posy+=my*e.speed
                    if abs(dx)<1 and abs(dy)<10:
                        e.index+=1 
                    if e.state==MonsterState.NORMAL:
                        e.color=(0,0,0)
                    else:
                        #flash the monster when hit.
                        e.color=(255,255,255)
                        e.state=MonsterState.NORMAL
                    #If monster arrive at goal, take away game life
                    if (Grid.goal_x)*Grid.grid_size <= e.posx <= (Grid.goal_x+1)*Grid.grid_size and\
                       (Grid.goal_y)*Grid.grid_size <= e.posy <= (Grid.goal_y+1)*Grid.grid_size:
                        Game.life-=10
                        Game.monsters.remove(e)
                        continue
            elif Game.state==GameState.STATE_SAVE:
                #call file_utils to save the file, then quickly send state to IDLE
                FileAction.write_to_file(Grid.grid)
                print('file saved')
                Game.state=GameState.STATE_IDLE
            elif Game.state==GameState.STATE_LOAD:
                Grid.grid= FileAction.read_from_file()
                Grid.astar=AStar(Grid.grid)
                Grid.astar=Grid.update_position()
                print('file loaded')
                Game.state=GameState.STATE_IDLE
            elif Game.state==GameState.STATE_CONFIG:
                pass
            await asyncio.sleep(0)


