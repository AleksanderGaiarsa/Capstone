#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:15:59 2022

@author: aleksandergaiarsa
"""

import pygame
import math

class Agent():
    def __init__(self, start_x:int, start_y:int, width:int, height:int, size:int, png_image:str):
        #position and size
        self.x = start_x
        self.y = start_y
        self.width = width
        self.height = height
        self.size = size
        
        self.image = pygame.image.load(png_image).convert()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def draw(self, display):
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # return a width and height of an image
        self.size = self.image.get_size()
        
        # create a factorial x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*self.size), int(self.size[1]*self.size)))
        display.blit(self.bigger_img,(self.x,self.y))

class Bullets(pygame.sprite.Sprite):
        def __init__(self,x,y, player_x, player_y):
            self.x = x
            self.y = y
            self.speed = slider_value
            self.angle = math.atan2(y-player_y, x-player_x)
            self.x_vel = math.cos(self.angle) * self.speed
            self.y_vel = math.sin(self.angle) * self.speed
            self.rect = pygame.draw.circle(display, (0,0,0), (self.x, self.y), 5)
            self.reverse = 1

        def draw(self, display):
            self.x -= int(self.x_vel) * self.reverse
            self.y -= int(self.y_vel) * self.reverse
            if (self.x > 160) & (self.x<900): 
                self.rect = pygame.draw.circle(display, (0,0,0), (self.x, self.y), 5)

        def sword_collide(self, test_sprite):
            if pygame.sprite.collide_rect(self, test_sprite):
                self.reverse = (-self.reverse)
                return True

        def player_collide(self, test_sprite):
            if pygame.sprite.collide_rect(self, test_sprite):
                return True

class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, sword_png, angle=15, stabtime=30):
        super().__init__()

        self.activate = False
        self.x = x
        self.y = y
        self.angle = angle

        self.image = pygame.image.load(sword_png).convert()
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.reset_image = self.image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.stabtime = stabtime
        self.swinging = False
        self.y_counter = 0
        self.x_counter = 0

    def update(self, display, x, y):
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        if self.swinging:
            display.blit(self.image,(self.x,self.y))

            if self.stabtime <= 0:
                self.reset_stab()
            self.stabtime -= 1
            if self.stabtime <=10:
                self.angle+=5
                self.y_counter+=8
            if self.stabtime >= 11 and self.stabtime <=20:
                self.angle+=7
                self.x_counter-=5
            else:
                self.angle+=5
                self.y_counter-=4
            self.x = x + self.x_counter
            self.y = y + self.y_counter
            self.image = pygame.transform.rotate(self.reset_image, self.angle) 

    def swing(self):
        self.angle = -65
        self.image = pygame.transform.rotate(self.reset_image, self.angle)
        self.swinging = True
        self.activate = True

    def reset_swing(self):
        self.x_counter = 0
        self.y_counter = 0
        self.stabtime = 30
        self.image = self.reset_image
        self.angle = -65
        self.swinging = False
        self.activate = False

class Bullets(pygame.sprite.Sprite):
        def __init__(self, display, x, y, player_x, player_y):
            self.x = x
            self.y = y
            self.speed = slider_value
            self.angle = math.atan2(y-player_y, x-player_x)
            self.x_vel = math.cos(self.angle) * self.speed
            self.y_vel = math.sin(self.angle) * self.speed
            self.rect = pygame.draw.circle(display, (0,0,0), (self.x, self.y), 5)
            self.reverse = 1

        def draw(self, display):
            self.x -= int(self.x_vel) * self.reverse
            self.y -= int(self.y_vel) * self.reverse
            if (self.x > 160) & (self.x<900): 
                self.rect = pygame.draw.circle(display, (0,0,0), (self.x, self.y), 5)

        def check_sword_collide(self, test_sprite):
            if pygame.sprite.collide_rect(self, test_sprite):
                self.reverse = (-self.reverse)
                return True

        def check_player_collide(self, test_sprite):
            if pygame.sprite.collide_rect(self, test_sprite):
                return True
        
class Health_Bar():
    def __init__(self, max_health):
        self.health_bar_length = 900 - 215 # (in pixel) about half the size of the screen
        self.health_ratio = max_health /self.health_bar_length

    def draw(self, display, health):
        pygame.draw.rect(display,(255,0,0),(163,0, health/self.health_ratio, 50))
        pygame.draw.rect(display,(255,255,255),(163,0,self.health_bar_length, 50),4) # white border

class Player(Agent):
    def __init__(self, start_x:int, start_y:int, width:int, height:int, size:int, png_image:str):
        super().__init__(start_x, start_y, width, height, size, png_image)

        #Health
        self.maximum_health = 1000 # (in number)
        self.current_health = self.maximum_health
        self.health_bar = Health_Bar(self.maximum_health)

        #Sword
        self.sword = Sword(self.x, self.y, sword_png="./Graphics/sword.png")

    def damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0

    def regain_health(self, amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health
    
class Enemy(Agent):
    def __init__(self, start_x:int, start_y:int, width:int, height:int, size:int, png_image:str):
        super().__init__(start_x, start_y, width, height, size, png_image)

        self.bullets = []