'''Timeline module by Tigo.robotics 2022,2023'''
import asyncio
from game import Game, GameState
'''
each timeline keeps track of a certain event that should be 
happening in sequence.
could be event based or time based or trigger based.
Timeline has the power to change ANYTHING in the game.
'''
class Timeline:
    def __init__(self,id):
        print('timeline created')
        self.id=id
        self.debug=0
    async def flow(self):
        while True:
            if self.debug:print(Game.current_mode, Game.build_state, Game.player_state)
            if Game.life<=0:
                Game.state=GameState.STATE_OVER
                Game.life=100 #when game state changed to state over, reset game.life
            '''Here we can add chapters of our game'''
            await asyncio.sleep(0)




