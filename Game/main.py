import pygame
import random
import pygame_gui
import modules.game_objects as g_obj
import modules.gui as gui
import modules.game_algos as algo
import modules.calibration as calib

DAMAGE_FACTOR = 1

#accelerometer data
atot_index = 0
counter_1=1

with open('./Game/acc_data.txt') as acc_data:
    line_count = 0
    atot = []
    for row in acc_data:
        column = row.split()
        if not row.startswith('#'):
            atot.append(column[4])
        if counter_1> 4504:
            break
        counter_1+=1
    atot.remove('atotal')
    n_atot = len(atot)

class Shooting_Game():
    def __init__(self):
        
        self.calibration = calib.Calibration()

        #Pygame Setup
        pygame.init()
        pygame.display.set_caption("Game Simulation")
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.disp_w, self.disp_h = pygame.display.get_surface().get_size()
        self.fps = 60

        #GUI
        self.gui = gui.GUI(self.disp_w, self.disp_h, self.calibration)
        self.font = pygame.font.Font('freesansbold.ttf', 26)

        self.background = pygame.Surface((self.disp_w, self.disp_h))
        self.background.fill((255,255,255), (0, 0, self.disp_w/6, self.disp_h)) #white background
        self.background.fill((0,0,0), (self.disp_w/6, 0, 4, self.disp_h)) #black line at 160-163 pixels
        self.background.fill((200,104,65), (self.disp_w/6+4, 0, self.disp_w, self.disp_h)) #orange starting at 163

        self.clock = pygame.time.Clock()
        self.timer1 = 1000
        self.deltat = 0

        self.player = g_obj.Player(800,500, size=3, png_image="./Game/Graphics/player.png")
        self.enemy = [  g_obj.Enemy(800,150, size=2, png_image="./Game/Graphics/enemy.png"),
                        g_obj.Enemy(500,790, size=2, png_image="./Game/Graphics/enemy.png"),
                        g_obj.Enemy(1200,150, size=2, png_image="./Game/Graphics/enemy.png"),
                        g_obj.Enemy(1300,750, size=2, png_image="./Game/Graphics/enemy.png"),
                        g_obj.Enemy(380,320, size=2, png_image="./Game/Graphics/enemy.png"),
                        ]
        
        self.run = True
        self.play()

    def timer(self):
        
        self.timer1 -= self.deltat
        
        if self.timer1 <= 0:  # Ready to fire.
            counter = random.randint(0,4)
            self.enemy[counter].bullets.append(g_obj.Bullets(self.display, self.enemy[counter].x, self.enemy[counter].y, 
                                                            self.player.x, self.player.y, self.gui.slider_value))
            self.timer1 = self.gui.bullet_rate[self.gui.bullet_rate_ind]  # Reset the timer.
            
        self.deltat = self.clock.tick(self.fps) #milliseconds
    
    def pygame_event_check(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.gui.lvl_diff:
                    self.gui.bullet_rate_ind = self.gui.diff_list.index(event.text)
            
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.gui.speed_slider:
                    self.gui.slider_value = event.value
                    self.gui.speed_label.set_text("<font color='#FFFFFF'  size=2>"
                                        "Bullet Speed:"+str(self.gui.slider_value*5)+ " Km/h")
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.calibration.current_temp = round(self.calibration.current_temp - 0.3, 2)
                    self.calibration.temp_ratio = abs(((self.calibration.current_temp - self.calibration.base_temp)/self.calibration.base_temp))
                    if self.calibration.temp_ratio > self.calibration.prev_temp_ratio:
                        self.player.damage(10)
                    else:
                        self.player.regain_health(10)
                    self.calibration.prev_temp_ratio = self.calibration.temp_ratio
                    self.gui.skin_temp_label.set_text("<font color='#FFFFFF' size=2>"
                                            "Skin Temperature: <br>"
                                            "<font size=3>"
                                            "      "+str(self.calibration.current_temp)+" &deg;C")
                    self.gui.skin_temp_label.scroll_bar.hide()
                if event.key == pygame.K_UP:
                    self.calibration.current_temp = round(self.calibration.current_temp + 0.3, 2)
                    self.calibration.temp_ratio = abs(((self.calibration.current_heart - self.calibration.base_heart)/self.calibration.base_heart))
                    if self.calibration.temp_ratio > self.calibration.prev_temp_ratio:
                        self.player.damage(10)
                    else:
                        self.player.regain_health(10)
                    self.calibration.prev_temp_ratio = self.calibration.temp_ratio
                    self.gui.skin_temp_label.set_text("<font color='#FFFFFF' size=2>"
                                            "Skin Temperature: <br>"
                                            "<font size=3>"
                                            "      "+str(self.calibration.current_temp)+" &deg;C")
                    self.gui.skin_temp_label.scroll_bar.hide()
                if event.key == pygame.K_0:
                    self.calibration.current_heart = round(self.calibration.current_heart - 1,3)
                    self.calibration.heart_ratio = abs(((self.calibration.current_heart - self.calibration.base_heart)/self.calibration.base_heart))
                    if self.calibration.heart_ratio > self.calibration.prev_heart_ratio:
                        self.player.damage(10)
                    else:
                        self.player.regain_health(10)
                    self.calibration.prev_heart_ratio = self.calibration.heart_ratio
                    self.gui.heart_rate_label.set_text("<font color='#FFFFFF' size=2>"
                                        "Heart Rate: <br>"
                                        "<font size=3>"
                                        "      "+str(self.calibration.current_heart)+" bpm")
                    self.gui.movement_label.set_text("<font color='#FFFFFF' size=2.5>"
                                            "Movement Speed:<br>"
                                            "<font size=3>"
                                            "      "+str(round(int(self.gui.movement_speed*5)))+" km/h")
                    self.gui.movement_label.scroll_bar.hide()
                if event.key == pygame.K_1:
                    self.calibration.current_heart = round(self.calibration.current_heart + 1,3)
                    self.calibration.heart_ratio = abs(((self.calibration.current_heart - self.calibration.base_heart)/self.calibration.base_heart))
                    if self.calibration.heart_ratio > self.calibration.prev_heart_ratio:
                        self.player.damage(10)
                    else:
                        self.player.regain_health(10)
                    self.gui.heart_rate_label.set_text("<font color='#FFFFFF' size=2>"
                                        "Heart Rate: <br>"
                                        "<font size=3>"
                                        "      "+str(self.calibration.current_heart)+" bpm")
                    self.gui.movement_label.set_text("<font color='#FFFFFF' size=2.5>"
                                            "Movement Speed:<br>"
                                            "<font size=3>"
                                            "      "+str(round(int(self.gui.movement_speed*5)))+" km/h")
                    self.gui.movement_label.scroll_bar.hide()
                
                if event.key == pygame.K_ESCAPE:
                    self.run = False  # Set running to False to end the while loop.
                    
            self.gui.manager.process_events(event)
    
    def check_for_collisions(self):
        for enemy in self.enemy:
            for bullet in enemy.bullets:
                if self.player.sword.swinging:
                    if bullet.check_sword_collide(self.player.sword):
                        self.player.sword.swinging  = False
                elif bullet.check_player_collide(self.player):
                    enemy.bullets.remove(bullet)
                    self.player.damage(self.gui.slider_value*DAMAGE_FACTOR)
                bullet.draw(self.display)
    
    def draw(self):
        self.player.draw(self.display)
        self.player.sword.draw(self.display, x=self.player.x+20, y=self.player.y+5)
        self.player.health_bar.draw(self.display, self.player.current_health)

        for enemy in self.enemy:
            enemy.draw(self.display)
    
    def check_keys(self):
        global atot_index

        keys = pygame.key.get_pressed()
        
        self.gui.movement_speed = algo.calculate_player_speed(self.calibration.current_heart, self.calibration.base_heart)
        
        if keys[pygame.K_a]:
            self.player.x -= self.gui.movement_speed
        if keys[pygame.K_d]:
            self.player.x += self.gui.movement_speed
        if keys[pygame.K_w]:
            self.player.y -= self.gui.movement_speed
        if keys[pygame.K_s]:
            self.player.y += self.gui.movement_speed
            
        #SWORD SWING from Accelerometer    
        for x in range(2):
            if atot_index >= (n_atot-1):
                atot_index = 0
            else:
                atot_index+=1
            if float(atot[atot_index]) > 65:
                self.player.sword.swing()
                self.player.sword.x = self.player.x+20
                self.player.sword.y = self.player.y+5
        
    def play(self):
        global slider_value
        #Setup
        
        while(self.run):
            
            self.deltat_s = self.deltat/1000 #seconds
            
            self.check_keys()
            
            self.draw()

            self.check_for_collisions()

            
            self.timer()
            
            pygame.display.update()
            
            #TODO
            health_score = int(((self.player.current_health/self.player.health_bar.health_ratio)/self.player.health_bar.health_bar_length*100))
            percent_txt = self.font.render(str(health_score)+'%', False, (0, 0, 0))
            
            self.display.blit(self.background, (0, 0))
            self.display.blit(percent_txt, (960,25))
            self.gui.manager.draw_ui(self.display)
            self.gui.manager.update(self.deltat_s)
            
            self.pygame_event_check()
                
        pygame.quit()

if __name__ == '__main__':
    Shooting_Game()
    