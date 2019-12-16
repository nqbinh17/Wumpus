import numpy as np
from random import random
class Agent:
    def __init__(self,x,y,z,h_breeze=10,h_stench=10,h_explore=1,h_back=1,prob_shot=0.1):
        self.h_breeze=h_breeze
        self.h_stench=h_stench
        self.h_back=1
        self.prob_shot=prob_shot
        self.x=x
        self.y=y
        self.a=x # original x
        self.b=y # original y
        self.enviroment=np.array([[float(h_explore)]*10 for _ in range(10)])
        self.stench=np.array([[-1]*10 for _ in range(10)])
        self.heuristics=np.array([[float(0)]*10 for _ in range(10)]) # heuristics of where it passed
        self.logical_analogy(z) # z takes initial value in real_world
        self.isVisited=np.array([[False]*10 for _ in range(10)])
        self.isVisited[(x,y)]=True
        self.shot_cnt=0
        self.rooms=150
    def decision(self):
        # decision function return whether it moves or shots in which location
        # example : 1,2,1 => shots to axis (1,2)
        arr=self.take_moves(self.x,self.y)
        location=0
        value=1e9+7
        turn_back=abs(self.a-self.x) +abs(self.b-self.y)
        for i in arr:
            if turn_back<20:
                dis=abs(self.a-i[0])+abs(self.b-i[1])
                if dis<value and self.isVisited[i]==True:
                    value=dis
                    location=i
                    continue
            h=float(self.enviroment[i])*0.75 + float(self.heuristics[i])*0.25
            if h<value:
                value=h
                location=i
            if self.enviroment[i]!=0 and self.stench[i]==1 and random()>1-self.prob_shot:
                self.shot_cnt+=1
                return i[0],i[1],1
        self.isVisited[location]=True
        return location[0],location[1],0
    def update_heuristic(self,x,y,z=0):
        if z==1:
            self.heuristics[(x,y)]+=100
            self.stench[(x,y)]=0
        else:
            if self.isVisited[(x,y)]==True:
                self.heuristics[(x,y)]+=self.h_back
            
    def take_moves(self,x,y):
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
    def logical_analogy(self,states):
        arr=self.take_moves(self.x,self.y)
        self.enviroment[(self.x,self.y)]=0
        if states=='-':
            for i in arr:
                self.enviroment[i]=0
                self.stench[i]=0
        elif states=='B':
            for i in arr:
                if self.enviroment[i]==0:
                    continue
                else :
                    self.enviroment[i]=self.h_breeze
        elif states=='S':
            for i in arr:
                if self.enviroment[i]==0:
                    continue
                else:
                    self.enviroment[i]=self.h_stench
                    self.stench[i]=1

    def position(self):
        return self.x,self.y
    def update_pos(self,x,y):
        self.x=x
        self.y=y
        self.rooms-=1
class Wumpus:
    def __init__(self,world,debug=0):
        self.real_world=np.array(world)
        self.KB=list()
        x,y=self.agent_location() # this function have removed symbol "A" in real_world
        self.a=x
        self.b=y
        self.agent=Agent(x,y,self.real_world[(x,y)]) # agenttt
        self.score=0
        self.rooms=150
        self.states=True
        self.debug=debug
        self.debug_cnt=0
        self.debug_report=list()
        self.report_move=list()
        self.true_shot=0
        self.gold_cnt=0
        self.turn_base=False
    def debugger(self):
        dd=[]
        print('STEP %d'%self.debug_cnt)
        dd.append(self.debug_cnt)
        print('Real world in Wumpus class:')
        debug_metrix=np.array(self.real_world)
        debug_metrix[(self.agent.x,self.agent.y)]='A'
        print(*debug_metrix,sep='\n')   
        dd.append(debug_metrix)
        print('Agent Perception Metrix:')
        print(*self.agent.enviroment,sep='\n')   
        dd.append(self.agent.enviroment)
        print('Rooms Left: %d' % self.rooms)
        dd.append(self.rooms)
        print('Score : %d'%self.score)
        dd.append(self.score)
        print('Agent Position at ({},{})'.format(self.agent.x,self.agent.y))
        dd.append((self.agent.x,self.agent.y))
        self.debug_report.append(dd)
    def move_to(self,x,y):
        a,b=self.agent.position()
        if abs(a-x)+abs(b-y)<=1:
            1
        else:
            raise ValueError('Agent must move to local squares')
        encounter=self.real_world[x][y]
        if encounter in ['W','P']:
            return False
        else: 
            return encounter
    def shot_to(self,x,y):
        self.score-=100
        if 'W' in self.real_world[(x,y)]:
            self.real_world[(x,y)].replace('W','-')
            arr=self.take_moves(x,y)
            for i in arr:
                if len(self.real_world[i])==1:
                    self.real_world[i]='-'
                else:
                    self.real_world[i]=self.real_world[i].replace('S','')
            return True
        return False
    def take_moves(self,x,y):
        arr=[]
        if x-1>=0:
            arr.append((x-1,y))
        if y-1>=0:
            arr.append((x,y-1))
        if x+1<10:
            arr.append((x+1,y))
        if y+1<10:
            arr.append((x,y+1))
        return arr       
    def agent_location(self):
        for i in range(10):
            for j in range(10):
                if 'A' in self.real_world[(i,j)]:
                    if len(self.real_world[(i,j)])==1:
                        self.real_world[(i,j)]='-'
                    else:
                        self.real_world[(i,j)]=self.real_world[(i,j)].replace('A','')
                    return i,j
    def game_play(self): # testing TODO
        #x,y,z=self.agent.decision()
        while self.states and self.rooms:
            x,y,z=self.agent.decision()
            self.report_move.append([x,y,z])
            if z==1: # shots
                check=self.shot_to(x,y)
                if check == True:
                    x,y=self.agent.position()
                    self.true_shot+=1
                    self.agent.logical_analogy(self.real_world[x,y])
                else:
                    self.agent.update_heuristic(x,y,1)
            else:
                check=self.move_to(x,y)
                if check==False:
                    self.states=False
                    self.score-=10000
                else:
                    self.agent.update_pos(x,y)
                    self.rooms-=1
                    self.agent.update_heuristic(x,y)
                    for i in check:
                        if i=='G':
                            self.score+=100
                            self.gold_cnt+=1
                            if len(check)==1:
                                self.real_world[(x,y)]='-'
                                i='-'
                            else:
                                self.real_world[(x,y)]=self.real_world[(x,y)].replace('G','')
                        self.agent.logical_analogy(i)
            if self.rooms==0:
                x,y=self.agent.position()
                if x==self.a and y==self.b:
                    self.turn_base=True
                    self.score+=10
            if self.debug==1:
                self.debugger()
                self.debug_cnt+=1
    def GamePlay_report(self,z=0):
        x=' '
        print(x*20+'GAMEPLAY REPORT')
        isVisited=self.agent.isVisited
        cnt=0
        for i in isVisited:
            for j in i:
                cnt+=j*1
        cnt=str(cnt)+'%'
        score=self.score
        moves=self.agent.rooms
        isDead=self.states
        if isDead==True:
            isDead='True'
        else:
            isDead='No'
        num_shots=self.agent.shot_cnt
        if num_shots!=0:
            true_shots=float(self.true_shot)/num_shots *100
            true_shots=str(true_shots)+'%'
        else:
            true_shots='100%'
        print('Is Dead? : %s' % isDead)
        if self.turn_base==True:
            ss='True'
        else:
            ss='False'
        print('Is Climbing out? : %s' %ss)
        print('Moves left: %d' %moves)
        print('Percent of Map Exploration : %s' %cnt)
        print('Score : %d' %score)
        print('Number of Gold: %d' %self.gold_cnt)
        print('Number of shooting : %d' %num_shots)
        print('Shooting Precision: %s' %true_shots)
        
        if z==0:
            return
        
        print(x*20+'AGENT ATTRIBUTION REPORT ')
        breeze=self.agent.h_breeze
        stench=self.agent.h_stench
        back=self.agent.h_back
        percent_shoot=self.agent.prob_shot*100
        percent_shoot=str(percent_shoot)+'%'
        import pandas as pd
        heuristics=pd.DataFrame(self.agent.heuristics,dtype='int')
        environment=pd.DataFrame(self.agent.enviroment,dtype='int')
        print('Heuristic when meet Breeze : %d' %breeze)
        print('Heuristic when Stench : %d' %stench)
        print('Heuristic when Back : %d' %back)
        print('Probability of Shooting : %s'%percent_shoot)
        print('Agent Enviornment  Recognition :')
        print(environment)
        print('Agent Heuristics Result :')
        print(heuristics)