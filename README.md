pytd_01 is a educational tower defence game written for school holidays during Tigo.Robotics 2022
mpl-2.0 license applied.


## Web Version

visit [https://dadalee51.github.io/]
for web version

## Basic Outline
asyncio
the game was written using asyncio library, so every module has their own task. 
inter task communication is achieved by modifying shared variables in the game module.

starting point of the game: main.py
the entry point of the code. everything started from this file.

basic outline of this game code: 
main.py
  to start the game, run the main.py
  to stop the game, press 'q' or stop the current python execution thread.
vislayers.py
  visual display of the game
models.py
  manage values related to each classes, grid, monsters etc.
runners.py
  create instances of classes from models.py, towers, monsters, etc.
pathfinder.py
  take a grid, start, goal and roadblocks, calculate best path using astar algorithms.
  return the path to caller.
game.py
  includes variables related to the game, task may need to update/change values to communicate
  with other tasks using these variables. 

how to read the code?
to read this code you will need to trace the code, so expect to jump across different files, 
linking different ideas togther.

main.py - start from main.py you can see draw method is called for Background and Foreground, 
find the definition of Background and Foreground and you can see the files lived in vislayers.py

Some design principles
1. Make changes at one place, then move the changes to their designated modules.
2. Keep it simple, don't try to cater for the future. Anyone comes later can make changes for the future.
3. this code was entirely written in one file when first started, then broken into smaller/seperate 
modules afterwards, so if a file gets too big, it can then be split into smaller files in folders for
easier read/find/modification.
4. There are many await asyncio.sleep(0) calls in each task, this means the task can yield its execution
time to another task with the minimum waiting time, so nothing gets held up. 

vislayers.py - the vislayers module maintains everything that can be described by shapes, position(x,y),
width, height, buttons, text, colour, animations, pictures. This class also observe the Game variables 
to change states accordingly. This class manages how everything 'looks' in the game. 



