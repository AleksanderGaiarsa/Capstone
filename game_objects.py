#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:15:59 2022

@author: aleksandergaiarsa
"""

import pygame

class Agent():
    def __init__(self, start_x:int, start_y:int, width:int, height:int, png_image:pygame.surface.Surface):
        #position and size
        self.x = start_x
        self.y = start_y
        self.width = width
        self.height = height
        
        
        self.image = png_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def draw(self, display):
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # return a width and height of an image
        self.size = self.image.get_size()
        
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        display.blit(self.bigger_img,(self.x,self.y))
        
class Player(Agent):
    def __init__(start_x, start_y, width, height, png_image):
        super.__init__(start_x, start_y, width, height, png_image)
        
    
class Enemy(Agent):
    def __init__(start_x, start_y, width, height, png_image):
        super.__init__(start_x, start_y, width, height, png_image)