from wumpus_environment import Wumpus
f=open(r'D:\My_stuffs\ML\AI&ML\input.txt','r')
data=f.read()
lines=data.split('\n')
world=[line.split('.') for line in lines]
game=Wumpus(world)
game.game_play()
game.GamePlay_report(True)
"""
Tutorial
-> return
--> call function
Class Wumpus -> function game_play --> Agent.decision --> Wumpus.move_to --> Agent.logical_analogy.
Class Agent -> function decision-> position, logical_analogy-> heuristic metrix  

"""