# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 16:53:25 2022

@author: nguye
https://medium.com/data-science-in-your-pocket/game-development-using-pygame-reinforcement-learning-with-example-f5b78c768610
"""
import pygame, sys
from pygame.locals import *
import random
import numpy as np

# Not necessary since we just want to find angles
# pygame.init()
# DISPLAYSURF = pygame.display.set_mode((500,500),0,32)
# clock = pygame.time.Clock()

class game_env:
    def __init__(self,suffix):  
        self.q_table = np.zeros((100,4))
        self.reward_map = {'player.png':100,'missed':-20,'enemy.png':-10,'invalid':-100} # in our case, we should just make it based on heathbar
        self.dir = range(0,359) # all the angles for us, used to be a dictionary of Left/right/up/down
        self.alpha = 0.75  #used in q-learning formula
        self.beta = 0.75   #used in q learning formula
        self.greedy = 0.6  #epsilon-greedy, greedy 
        self.random = 0.4  #epsilon greedy, epsilon
        self.delta = 0.005  #rate of change for epsilon & greedy
        self.game_dim = (500,650) #window size
        self.text_space = 150     #Window size for printing stats
        self.initial_cood = (0,0+self.text_space) # state 0 position
        self.rows,self.columns = 10,10
        self.start_state = 0
        self.end_state = 99
        self.cell_dim = self.game_dim[0]/self.rows #side of each cell in grid
        self.final_cood = (self.game_dim[0]-self.cell_dim, self.game_dim[1]-self.cell_dim)  #state 99 position  
        self.game_grid = self.new_game_env() #declared below
        self.suffix = suffix  
        self.action_space = {0:{'x':-1*self.cell_dim,'y':0}, 2:{'x':self.cell_dim,'y':0}, 1:{'x':0,'y':self.cell_dim},3:{'x':0,'y':-1*self.cell_dim}}  
        try:
            with open('env_weights\\weights_{}.npy'.format(self.suffix),'rb') as f:
                                self.q_table = np.load(f)
            with open('env_weights\\env_{}.npy'.format(self.suffix),'rb') as f:
                                self.game_grid = np.load(f)
        except Exception as e:
            print('No such files pre-exists. Starting a new environment')
            with open('env_weights\\env_{}.npy'.format(self.suffix),'wb') as f:
                                np.save(f,self.game_grid)
            with open('env_weights\\weights_{}.npy'.format(self.suffix),'wb') as f:
                                np.save(f,self.q_table)
            pass
        
####

def new_game_env(self):
        matrix = random.choices (['missed.png'], weights=[0.55,0.15,0.15,0.15], k=self.rows*self.columns)
        matrix = np.asarray(matrix).reshape(self.rows,self.columns)
        matrix[0][0] = 'enemy.png'
        matrix[self.rows-1][self.columns-1] = 'player.png'
        return matrix
    
    # Aleks' Pygame stuff goes here to display
    # the enemies original position and player 
    # initial position
    
# State-coordinates
# cell_dim is dimensions of each cell of the grid

def cood_state_calc(self,cood):
        state = int((self.rows*(cood[1]-self.text_space)/self.cell_dim)+(cood[0]/self.cell_dim)) 
        return state
    
def state_cood_calc(self, state):
        cood = int((state%self.rows)*self.cell_dim),int((state//self.rows)*self.cell_dim+self.text_space)
        return cood    
    
# Check move validity
    # The enemy cannot run into another enemy (enemy does not move)
    # Change the "already_visited"

def is_valid_move(self, cood, already_visited): #remove this, not relevant
    if cood in already_visited:
        return False
    
    if self.initial_cood[0]<=cood[0]<=self.final_cood[0] and self.initial_cood[1]<=cood[1]<=self.final_cood[1]:
            return True
    return False

# Q table update (VERY IMPORTANT)

def q_table_update(self,  state, action, already_visited):
    curr_cood = self.state_cood_calc(state)
    new_cood = (int(curr_cood[0] + self.action_space[action]['x']), int(curr_cood[1] + self.action_space[action]['y']))
    new_state = self.cood_state_calc(new_cood)
    is_valid = self.is_valid_move(new_cood, already_visited)
                                 
  
    if is_valid:
        reward = self.reward_map[self.game_grid[int(new_state//self.rows)][int(new_state%self.rows)]]
    elif new_cood in enemy:
        reward = self.reward_map['enemy']
    else:
        reward = self.reward_map['invalid']
            
    try:
        state_value_diff = max(self.q_table[new_state]) - self.q_table[state][action]
    except:
        state_value_diff = 0
    self.q_table[state][action]+=self.alpha*(reward + self.beta*state_value_diff)
                                 
    return is_valid, new_state, new_cood,reward

# Each episode

def episode(self, current_state, is_valid):
    pygame.event.get()
    cood = self.state_cood_calc(current_state)
    already_visited = [cood]
    self.steps_visualizer(cood)
    
    while current_state!=self.end_state and is_valid==True:
        pygame.draw.rect(DISPLAYSURF,(0,0,0),(0,100,self.game_dim[0],50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==QUIT:
                            pygame.quit()
                            raise Exception('training ended')
        choice = random.choices([True,False],weights=[self.greedy,self.random],k=1)
        if choice[0]:
                 action = np.argmax(self.q_table[current_state])
        else:
                 action = random.choices([0,1,2,3],weights=[0.25,0.25,0.25,0.25],k=1)
                 action = action[0]
        self.print_summary('State:{}'.format(current_state),(10,100),15)
        self.print_summary('Action:{}'.format(self.dir[action]),(110,100),15)
        is_valid, current_state, cood, reward = self.q_table_update(current_state, action, already_visited)
        
        self.print_summary('Reward:{}'.format(reward),(220,100),15)
        
        if is_valid==False and cood not in already_visited:
            self.print_summary('INVALID MOVE !!',(330,100),15)
        elif is_valid==False:
            self.print_summary('ALREADY VISITED',(330,100),15)
        else:
            self.print_summary('New State:{}'.format(current_state),(330,100),15)
        
        pygame.display.update()
        clock.tick(0.9)
        already_visited.append(cood)
        if is_valid:
            self.steps_visualizer(cood)
        else:
            break

### NOW ONTO TRAINING ITSELF

def training(self, epoch):
    state=random.randint(self.start_state,self.end_state)
    self.initial_state()
    self.print_summary(' Episode:{}'.format(epoch),(200,60),20)
    self.episode(state, True)  
    print('episode {} ---->'.format(epoch))
    pygame.display.set_caption('greedy={}, random={}'.format(round(self.greedy,4),round(self.random,4)))
    if epoch%50==0:
        if self.random>0:
                self.greedy+=self.delta
                self.random-=self.delta
                self.greedy = min(self.greedy,1)
                self.random= max(self.random,0)
        
    if epoch%2000==0:
        self.delta*=2
        with open('env_weights\\weights_{}.npy'.format(self.suffix),'wb') as f:
            np.save(f,self.q_table)
    
    clock.tick(1)
    
#### TESTING PORTION

def testing(self,initial_state=0):
            self.greedy = 1
            self.random = 0
            with open('env_weights\\env_{}.npy'.format(self.suffix),'rb') as f:
                self.game_grid = np.load(f)
            
            with open('env_weights\\weights_{}.npy'.format(self.suffix),'rb') as f:
                self.q_table = np.load(f)
            
            self.initial_state()
            self.episode(initial_state,True)