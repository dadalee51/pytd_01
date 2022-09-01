'''Timeline module ©️ Tigo.robotics 2022'''
import asyncio
from game import Game
'''
each timeline keeps track of a certain event that should be 
happening in sequence.
could be event based or time based or trigger based.
Timeline has the power of changing ANYTHING in the game.
'''
class Timeline:
    def __init__(self,id):
        print('timeline created')
        self.id=id
        self.debug=0
    async def flow(self):
        while True:
            if self.debug:print(Game.current_mode, Game.build_state, Game.player_state)
            await asyncio.sleep(1)



