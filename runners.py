'''class for monsters and towers to react - copyright 2022 Tigo.Robotics'''
#runners are in charge of handle state changes, game dynamics, algorithms in realtime.
from models import Monster, Tower
from game import Game, GameState
from models import Grid
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
                    twr=Tower('tower'+str(i)+str(j),Game.x_left_padding+Grid.grid_size*i,Game.y_top_padding+Grid.grid_size*j,(100,0,100),10,100)
                    Game.towers.append(twr)
        self.tower_created=1
    def update_towers(self):
        pass

    async def run(self):
        while True:
            if Game.state==GameState.STATE_IDLE:
                #idle state, remove all tower models
                Game.towers=[]
                self.tower_created=0  
            elif Game.state==GameState.STATE_PLAY:
                self.create_towers()
                #go through all towers
                for t in Game.towers:
                    await t.detect_monster()
                    await t.attack_monster()
                    await t.reload()
                    
            await asyncio.sleep(0.01)


        
class MonsterRunner:
    def __init__(self):
        pass
    #produce and track monsters
    async def run(self):
        m =Monster('aMon', 100,0,100, (50,0,50), 5, 1, 3)
        Game.monsters.append(m)
        while True:
            if Game.state==GameState.STATE_IDLE:
                for e in Game.monsters:
                    e.posx=Grid.start_x*Grid.grid_size+Grid.grid_size/2
                    e.posy=Grid.start_y*Grid.grid_size+Grid.grid_size/2
                    e.index=1
            elif Game.state==GameState.STATE_PLAY:
                for e in Game.monsters:
                    if e.health<0:
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
            await asyncio.sleep(0.01)


