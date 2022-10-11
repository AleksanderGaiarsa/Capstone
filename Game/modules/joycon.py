import pyjoycon
import pygame
import time
import threading
import collections

class Controller:
    def __init__(self):

        self.joycon_id = {}
        self.joycon = {}
        self.status = {}
        self.analog_stick_ref=collections.defaultdict(dict)
        for side in ('right', 'left'):
            for axe in ('x', 'y'):
                self.analog_stick_ref[side][axe] = 0


        self.joycon_id['right'] = pyjoycon.get_R_id()
        self.joycon_id['left']= pyjoycon.get_L_id()
        
        if None not in self.joycon_id['right']:
            self.joycon['right'] = pyjoycon.JoyCon(*self.joycon_id['right'])
        if None not in self.joycon_id['left']:
            self.joycon['left'] = pyjoycon.JoyCon(*self.joycon_id['left'])

        for key,value in self.joycon.items():
            while (self.analog_stick_ref[key]['x'] == 0 or self.analog_stick_ref[key]['y'] == 0):
                self.status[key] = value.get_status()
                self.analog_stick_ref[key]['x'] = self.status[key]['analog-sticks'][key]['horizontal']
                self.analog_stick_ref[key]['y'] = self.status[key]['analog-sticks'][key]['vertical']

        self.accel_event = pygame.event.Event(pygame.USEREVENT)

        self.run = True
        threading.Thread(target = self.monitor_joycon).start()

    def monitor_joycon(self):
        while self.run:
            for key in list(self.joycon.keys()):
                self.status[key] = self.joycon[key].get_status()
                #print(self.status[key])

                if self.status[key]['analog-sticks'][key]['horizontal'] > (self.analog_stick_ref[key]['x']*1.2):
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d)
                    pygame.event.post(event)
                
                elif self.status[key]['analog-sticks'][key]['horizontal'] < (self.analog_stick_ref[key]['x']*0.8):
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)
                    pygame.event.post(event)

                if self.status[key]['analog-sticks'][key]['vertical'] > (self.analog_stick_ref[key]['y']*1.2):
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
                    pygame.event.post(event)
                
                elif self.status[key]['analog-sticks'][key]['vertical'] < (self.analog_stick_ref[key]['y']*0.8):
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s)
                    pygame.event.post(event)
                
                for axes in self.status[key]['accel'].values():
                    if abs(axes) > 6000:
                        pygame.event.post(self.accel_event)
                        break
                
                if (self.status[key]['buttons'][key]['sr'] == 1 and self.status[key]['buttons'][key]['sr'] == 1 and
                    (self.status[key]['buttons']['shared']['minus'] == 1 or self.status[key]['buttons']['shared']['plus'] == 1)):
                    del self.joycon[key]

            time.sleep(0.01667)