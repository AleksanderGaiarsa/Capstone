#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:15:59 2022

@author: aleksandergaiarsa
"""

import pygame
import math
import os

class Agent(pygame.sprite.Sprite):
    def __init__(self, start_x:int, start_y:int, size:int, png_image:str):
        #position and size
        self.x = start_x
        self.y = start_y
        self.size = size
        
        self.image = pygame.image.load(png_image).convert()
        img_size = self.image.get_size()
        # create a factorial x bigger image than self.image
        self.image = pygame.transform.scale(self.image, (int(img_size[0]*self.size), int(img_size[1]*self.size)))
        
    def draw(self, display):
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        display.blit(self.image,(self.x,self.y))

class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, sword_png, angle=15, stabtime=30):
        super().__init__()

        self.x = x
        self.y = y
        self.angle = angle

        self.image = pygame.image.load(sword_png).convert()
        img_size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(img_size[0]*1.8), int(img_size[1]*1.8)))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.reset_image = self.image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.stabtime = stabtime
        self.swinging = False
        self.y_counter = 0
        self.x_counter = 0

    def draw(self, display, x, y):
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if self.swinging:
            display.blit(self.image,(self.x,self.y))

            if self.stabtime <= 0:
                self.reset_swing()
            self.stabtime -= 1
            if self.stabtime <=10:
                self.angle+=5
                self.y_counter+=10
            if self.stabtime >= 11 and self.stabtime <=20:
                self.angle+=7
                self.x_counter-=7
            else:
                self.angle+=5
                self.y_counter-=6
            self.x = x + self.x_counter
            self.y = y + self.y_counter
            self.image = pygame.transform.rotate(self.reset_image, self.angle) 

    def swing(self, x, y):
        if not self.swinging:
            self.angle = -65
            self.image = pygame.transform.rotate(self.reset_image, self.angle)
            self.swinging = True
            self.x = x
            self.y = y

    def reset_swing(self):
        self.x_counter = 0
        self.y_counter = 0
        self.stabtime = 30
        self.image = self.reset_image
        self.angle = -65
        self.swinging = False

class Bullets(pygame.sprite.Sprite):
        def __init__(self, display, x, y, player_x, player_y, speed):
            self.x = x
            self.y = y
            self.speed = speed
            self.angle = math.atan2(y-player_y, x-player_x)
            self.x_vel = math.cos(self.angle) * self.speed
            self.y_vel = math.sin(self.angle) * self.speed
            self.rect = pygame.draw.circle(display, (0,0,0), (self.x, self.y), 7)
            self.reverse = 1

        def draw(self, display):
            self.x -= int(self.x_vel) * self.reverse
            self.y -= int(self.y_vel) * self.reverse
            #TODO
            if (self.x < display.get_width()/6):
                del self
            else:
                self.rect = pygame.draw.circle(display, (0,0,0), (self.x, self.y), 7)

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
        pygame.draw.rect(display,(255,0,0),(display.get_width()/6+4,0, health/self.health_ratio, 75))
        pygame.draw.rect(display,(255,255,255),(display.get_width()/6+4,0, self.health_bar_length, 75),4) # white border

class Player(Agent):
    def __init__(self, start_x:int, start_y:int, size:int, png_image:str):
        super().__init__(start_x, start_y, size, png_image)

        #Health
        self.maximum_health = 1000 # (in number)
        self.current_health = self.maximum_health
        self.health_bar = Health_Bar(self.maximum_health)

        #Sword
        self.sword = Sword(self.x, self.y, sword_png="./Game/assets/sword.png")

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
    def __init__(self, start_x:int, start_y:int, size:int, png_image:str):
        super().__init__(start_x, start_y, size, png_image)

        self.bullets = []