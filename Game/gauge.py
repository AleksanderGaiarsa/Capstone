import pygame
import pygame.gfxdraw
import math

class Gauge():
    def __init__(self, screen, FONT, x_cord, y_cord, thickness, radius, circle_colour, glow=True):
        self.screen = screen
        self.Font = FONT
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.thickness = thickness
        self.radius = radius
        self.circle_colour = circle_colour
        self.glow = glow

    def draw(self, percent):
        fill_angle = int(percent*270/100)
        per=percent
        ac = [int(per*255/100), int(255-per*255/100), int(0), 255]
        for indexi in range(len(ac)):
            if ac[indexi] < 0:
                ac[indexi] = 0
            if ac[indexi] > 255:
                ac[indexi] = 255
        # print(ac)
        volt = per/20
        pertext = self.Font.render('%.2f' %volt + " V", True, ac) #str(volt) + "%", True, ac
        pertext_rect = pertext.get_rect(center=(int(self.x_cord), int(self.y_cord)))
        self.screen.blit(pertext, pertext_rect)

        for i in range(0, self.thickness):

            pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, 45, self.circle_colour)
            pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, fill_angle - 225, ac)

