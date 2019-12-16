import numpy as np
from random import random
class World:
    def __init__(self,pit=5,wumpus=5,gold=5):
        self.real_world=np.array([['-']*10 for _ in range(10)])
        self.rate_pit=float(pit)/100
        self.rate_wumpus=float(wumpus)/100
        self.rate_gold=float(gold)/100
        self.rate_agent=0.01
        self.n_pit=0
        self.n_wumpus=0
        self.n_gold=0
        self.generate_world()
    def take_move(self,x,y):
        arr=[]
        if x-1>=0:#and self.isVisited[(x-1,y)]==False:
            arr.append((x-1,y))
        if y-1>=0:#and self.isVisited[(x,y-1)]==False:
            arr.append((x,y-1))
        if x+1<10:# and self.isVisited[(x+1,y)]==False:
            arr.append((x+1,y))
        if y+1<10:# and self.isVisited[(x,y+1)]==False:
            arr.append((x,y+1))
        return arr
    
    def Print_World(self):
        print('Number of Pit: %d' %self.n_pit)
        print('Number of Wumpus: %d'%self.n_wumpus)
        print('Number of Gold: %d'%self.n_gold)
        cnt=0
        for i in range(10):
            for j in range(10):
                if self.real_world[(i,j)]!='-':
                    cnt+=1
        cnt=str(cnt)+'%'
        print('Percentage of Coverage: %s'%cnt)
	cnt=100-(self.n_pit+self.n_wumpus+self.n_gold)
	cnt=str(cnt)+'%'
	print('Percentage of Explorable: %s' %cnt)
        print(*self.real_world,sep='\n')
        return self.real_world
    def generate_world(self):
        is_agent=False
        
        while is_agent==False:
            real_world=np.array([['-']*10 for _ in range(10)])
            n_pit=0
            n_gold=0
            n_wumpus=0
            for i in range(10):
                for j in range(10):
                    p=random() < self.rate_pit
                    w=random() < self.rate_wumpus
                    g=random() < self.rate_gold
                    agent=random() < self.rate_agent
                    if is_agent==False and agent:
                        is_agent=True
                        real_world[(i,j)]='A'
                    elif g:
                        n_gold+=1
                        real_world[(i,j)]='G'
                    elif p:
                        n_pit+=1
                        real_world[(i,j)]='P'
                    elif w:
                        n_wumpus+=1
                        real_world[(i,j)]='W'
        self.real_world=real_world
        self.n_pit=n_pit
        self.n_gold=n_gold
        self.n_wumpus=n_wumpus
        real_world=[list(i) for i in self.real_world]
        for i in range(10):
            for j in range(10):
                if 'W' in real_world[i][j]:
                    arr=self.take_move(i,j)
                    for x,y in arr:
                        if 'S' not in real_world[x][y]:
                            if '-' not in real_world[x][y]:
                                real_world[x][y]+='S'
                            else:
                                real_world[x][y]='S'
                if 'P' in real_world[i][j]:
                    arr=self.take_move(i,j)
                    for x,y in arr:
                        if 'B' not in real_world[x][y]:
                            if '-' not in real_world[x][y]:
                                real_world[x][y]+='B'
                            else:
                                real_world[x][y]='B'
        self.real_world=np.array(real_world)
w=World()
real_world=w.Print_World()
