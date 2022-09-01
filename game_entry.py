'''main loop ©️ Tigo.robotics 2022'''
import pygame
import asyncio
import sys
from timeline import Timeline
from controls import Input
from game import Game
from vislayers import Background, Foreground
from models import Grid
from runners import MonsterRunner, TowerRunner
from pathfinder import AStar
class MainLoop:
    def __init__(self):
        pass
    async def run(self):
        b=Background(Game.screen_width,Game.screen_height)
        f=Foreground(Game.screen_width,Game.screen_height)
        while True:
            b.draw()
            f.draw()
            pygame.display.flip()
            await asyncio.sleep(0.01)
if __name__ == '__main__':
    pygame.init()
    loop=asyncio.get_event_loop()
    Game.loop=loop
    Game.font=pygame.font.SysFont(None, 20)
    Grid.grid=Grid.init_grid()
    Grid.astar=AStar(Grid.grid) 
    ml=MainLoop()
    t=Timeline('main time')
    mi=Input()
    mm=MonsterRunner()
    tr=TowerRunner()
    loop.create_task(ml.run())
    loop.create_task(t.flow())
    loop.create_task(mi.handle())
    loop.create_task(mm.run())
    loop.create_task(tr.run())
    loop.run_forever()
    print('game quit')
    pygame.quit()
    sys.exit()