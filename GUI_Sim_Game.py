import pygame
import math
import random
import pygame_gui
import gauge
import numpy

#Pygame Setup
pygame.init()
FPS = 60

#accelerometer data
atot_index = 0
counter_1=1

with open('acc_data.txt') as acc_data:
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
        

#Base Readings
base_heart = 0;
base_temp = 0;

for t in range(30):
    base_heart = base_heart + random.randrange(50,110,1)
    base_temp = base_temp + random.randrange(33,37,1)

base_heart = round(base_heart/30,2)    # average
base_temp = round(base_temp/30,2)
current_heart = base_heart
current_temp = base_temp
step_heart = 80/base_heart
step_temp = 500/base_temp
prev_heart_ratio = 0
heart_ratio = 0
prev_temp_ratio = 0
temp_ratio = 0



timer1 = 1000
deltat = 0
deltat_s = 0

WIDTH, HEIGHT = 1225, 600
FONT = pygame.font.SysFont('Franklin Gothic Heavy', 33)
font = pygame.font.Font('freesansbold.ttf', 20)

display = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.Surface((WIDTH, HEIGHT))
background.fill((200,104,65), (163, 0, display.get_width(), display.get_height())) #orange starting at 163
background.fill((0,0,0),(160,0, 3, display.get_height())) #black line at 160-163 pixels
background.fill((255,255,255), (0, 0, 160, display.get_height())) #white background
background.fill((0,0,0),(900,0, 3, display.get_height())) #black line at 900-903 pixels
background.fill((202,228,241), (903, 0, 500, display.get_height())) #teal background

pygame.display.set_caption("Game Simulation")
clock = pygame.time.Clock()

player_image=pygame.image.load("player.png")
enemy_image=pygame.image.load("enemy.png")

#Pygame GUI Setup
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

bullet_rate_ind = 1 #medium difficulty
diff_list = ['Easy', 'Medium', 'Hard', 'Very Hard']
bullet_rate = [1000, 500, 150, 50] #in milliseconds
bullet_rate_ind = 1 #start difficulty of medium
slider_value = 6 #start speed
movement_speed = 5

#GUI Adjustable Game propreties

diff_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF'>"
                                            'Difficulty',
                                            relative_rect=pygame.Rect((3, 0), (152, 35)),
                                            manager=manager)

lvl_diff=pygame_gui.elements.UIDropDownMenu(options_list= diff_list,
                                   starting_option='Medium',
                                   relative_rect=pygame.Rect((3, 35), (152, 50)),
                                   manager=manager)

speed_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF'  size=2>"
                                            "Bullet Speed:"+str(slider_value*5)+ " Km/h",
                                            relative_rect=pygame.Rect((3, 100), (152, 30)),
                                            manager=manager)

speed_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((3, 130), (152, 50)),
                                                      start_value = 6, 
                                                      value_range = (2,15), 
                                                      manager=manager)

skin_temp_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=2>"
                                            "Skin Temperature: <br>"
                                            "<font size=3>"
                                            "      "+str(base_temp)+" &deg;C",
                                            relative_rect=pygame.Rect((3, 220), (152, 50)),
                                            manager=manager)

heart_rate_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=2>"
                                            "Heart Rate: <br>"
                                            "<font size=3>"
                                            "      "+str(base_heart)+" bpm",
                                            relative_rect=pygame.Rect((3, 280), (152, 55)),
                                            manager=manager)

movement_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=2.5>"
                                            "Movement Speed:<br>"
                                            "<font size=3>"
                                            "      "+str(movement_speed*5)+" km/h",
                                            relative_rect=pygame.Rect((3, 345), (152, 50)),
                                            manager=manager)

baseline_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=3>"
                                            "<strong>Baseline Readings</strong><br>"
                                            "<font size=2>"
                                            "Skin Temperature="+str(base_temp)+"<br>"
                                            "Heart Rate="+str(base_heart)+"bpm",
                                            relative_rect=pygame.Rect((3, 500), (152, 90)),
                                            manager=manager)

voltage_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=5>"
                                            '<strong> ERM Voltage Input',
                                            relative_rect=pygame.Rect((950, 0), (225, 40)),
                                            manager=manager)
left_gauge_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=4>"
                                            ' Left Arm',
                                            relative_rect=pygame.Rect((1100, 117), (100, 35)),
                                            manager=manager)

chest_gauge_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=4>"
                                            '  Chest',
                                            relative_rect=pygame.Rect((1100, 293), (95, 35)),
                                            manager=manager)
left_gauge_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=4>"
                                            ' Right Arm',
                                            relative_rect=pygame.Rect((1100, 470), (100, 35)),
                                            manager=manager)

#Hide Scroll Bars
skin_temp_label.scroll_bar.hide()
movement_label.scroll_bar.hide()


#Create Gauge
bg_c = (56, 56, 56)
circle_c = (55, 77, 91)

left_gauge = gauge.Gauge(
    screen=display,
    FONT=FONT,
    x_cord= 1000,
    y_cord= 135,
    thickness=20,
    radius=85,
    circle_colour=circle_c,
    glow=False)

chest_gauge = gauge.Gauge(
    screen=display,
    FONT=FONT,
    x_cord= 1000,
    y_cord= 310,
    thickness=20,
    radius=85,
    circle_colour=circle_c,
    glow=False)

right_gauge = gauge.Gauge(
    screen=display,
    FONT=FONT,
    x_cord= 1000,
    y_cord= 485,
    thickness=20,
    radius=85,
    circle_colour=circle_c,
    glow=False)

# parameters for gauge
max_value = 100

target_value = numpy.zeros(3)
present_value = numpy.zeros(3)
pressed_value = 0

up_inc = 0

up_time = 0.1
up_frames = up_time * FPS

max_down_time = 0.7
down_time = numpy.zeros(3)
down_frames = numpy.tile([1,1,1],1)

inc = numpy.zeros(3)

needle_value = numpy.zeros(3)
gauge_flag = numpy.array([False, False, False])

#Load Images
PLAYER_IMAGE = pygame.image.load("player.png").convert()
SWORD_IMAGE = pygame.image.load("sword.png").convert()
ENEMY_IMAGE = pygame.image.load("enemy.png").convert()
HEART_IMAGE = pygame.image.load("heart.png").convert()
hearti_size = HEART_IMAGE.get_size()
HEART_IMAGE = pygame.transform.scale(HEART_IMAGE, (int(hearti_size[0]*0.19), int(hearti_size[1]*0.19)))

#Other
DAMAGE_FACTOR = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.current_health = 900 # we can pick whatever (in number)
        self.maximum_health = 1000 # (in number)
        self.health_bar_length = 900 - 215 # (in pixel) about half the size of the screen
        self.health_ratio = self.maximum_health /self.health_bar_length
        self.heart_image = HEART_IMAGE
    def draw(self, display):
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # return a width and height of an image
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        display.blit(self.bigger_img,(self.x,self.y))
        self.draw_health_bar()
    def get_damage(self,amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
    def get_health(self,amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health
    def draw_health_bar(self):
        pygame.draw.rect(display,(255,0,0),(163,0, self.current_health/self.health_ratio, 50))
        pygame.draw.rect(display,(255,255,255),(163,0,self.health_bar_length, 50),4) # white border

stabbing_flag = False
class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=15, stabtime=30):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.transform.rotate(SWORD_IMAGE, self.angle)
        self.orig_image = self.image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.stabtime = stabtime
        self.stabbing = False
        self.y_counter = 0
        self.x_counter = 0
        if self.stabbing == True:
            display.blit(self.image,(self.x,self.y))
    def update(self, x, y):
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        if self.stabbing:
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
            self.image = pygame.transform.rotate(self.orig_image, self.angle)       
    def stab(self):
        global stabbing_flag
        
        self.angle = -65
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.stabbing = True
        stabbing_flag = True
    def reset_stab(self):
        global stabbing_flag
        
        self.x_counter = 0
        self.y_counter = 0
        self.stabtime = 30
        self.image = self.orig_image
        self.angle = -65
        self.stabbing = False
        stabbing_flag = False

class Enemy:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def draw(self, display):
        self.enemy_image = ENEMY_IMAGE
        # return a width and height of an image
        self.size = self.enemy_image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.enemy_image, (int(self.size[0]*1.3), int(self.size[1]*1.3)))
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
                

player = Player(500,350,32,32)
sword = Sword(player.x, player.y)
enemy1 = Enemy(200,150,32,32)
enemy2 = Enemy(200,450,16,16)
enemy3 = Enemy(800,60,16,16)
enemy4 = Enemy(800,350,16,16)
enemy5 = Enemy(500,550,16,16)
enemy1_bullets = []
enemy2_bullets = []
enemy3_bullets = []
enemy4_bullets = []
enemy5_bullets = []

def calculate_player_speed():
    
    temp_ratio = abs(((current_heart - base_heart)/base_heart)*5)
    
    speed = 5 - (5*temp_ratio)
    
    if speed < 0:
        speed = 0
    
    return speed

def check_keys():
    global atot_index, movement_speed
    
    keys = pygame.key.get_pressed()
    
    movement_speed = calculate_player_speed()
    
    if keys[pygame.K_a]:
        player.x -= movement_speed
    if keys[pygame.K_d]:
        player.x += movement_speed
    if keys[pygame.K_w]:
        player.y -= movement_speed
    if keys[pygame.K_s]:
        player.y += movement_speed
        
    #SWORD SWING from Accelerometer    
    for x in range(2):
        if atot_index >= (n_atot-1):
            atot_index = 0
        else:
            atot_index+=1
        if float(atot[atot_index]) > 65:
            sword.stab()
            sword.x = player.x+20
            sword.y = player.y+5
            
def needle_algo(gauge_index):
    global present_value, target_value, inc 
    
    heart_rate_ratio = (current_heart - base_heart)/base_heart
    
    pressed_value = (((slider_value-2)/13)*75) + (heart_rate_ratio*25) #75% is based on bullet speed, other 25% is based on heart rate
        
    target_value[gauge_index] = present_value[gauge_index] + pressed_value
    inc[gauge_index] = pressed_value / up_frames


def update_needle():
    global down_time, down_frames, inc
    
    for index in range(3):
        if present_value[index] >= target_value[index] and present_value[index] != 0:
            test = (present_value[index] / max_value) * max_down_time
            down_time[index] = float(test)
            down_frames[index] = down_time[index] * FPS
            inc[index] = - (present_value[index] / down_frames[index])
    
        present_value[index] += inc[index]
    
        if present_value[index] <= 0 and inc[index] < 0:
            present_value[index] = 0
            inc[index] = 0
            target_value[index] = 0
    
        needle_value[index] = present_value[index]
        
        if needle_value[index] >= 100:
            needle_value[index] = 100

    left_gauge.draw(percent=needle_value[0])
    chest_gauge.draw(percent=needle_value[1])
    right_gauge.draw(percent=needle_value[2])
   
def check_for_collisions():
    global stabbing_flag, slider_value
    
    for bullet in enemy1_bullets:
        if stabbing_flag == True:
            if bullet.sword_collide(sword):
                stabbing_flag = False
        
        if bullet.player_collide(player):
            enemy1_bullets.remove(bullet)
            player.get_damage(slider_value*DAMAGE_FACTOR) 
            gauge_index = random.randint(0,2)
            needle_algo(gauge_index)
        
        bullet.draw(display)
        
    for bullet in enemy2_bullets:
        if stabbing_flag:
            if bullet.sword_collide(sword):
                stabbing_flag = False
        
        if bullet.player_collide(player):
            enemy2_bullets.remove(bullet)
            player.get_damage(slider_value*DAMAGE_FACTOR)
            gauge_index = random.randint(0,2)
            needle_algo(gauge_index)

        bullet.draw(display)
        
    for bullet in enemy3_bullets:
        if stabbing_flag:
            if bullet.sword_collide(sword):
                stabbing_flag = False
        
        if bullet.player_collide(player):
            enemy3_bullets.remove(bullet)
            player.get_damage(slider_value*DAMAGE_FACTOR) 
            gauge_index = random.randint(0,2)
            needle_algo(gauge_index)
        
        bullet.draw(display)
        
    for bullet in enemy4_bullets:
       if stabbing_flag:
           if bullet.sword_collide(sword):
               stabbing_flag = False
               
       if bullet.player_collide(player):
           enemy4_bullets.remove(bullet)
           player.get_damage(slider_value*DAMAGE_FACTOR)
           gauge_index = random.randint(0,2)
           needle_algo(gauge_index)
           
       bullet.draw(display)
        
    for bullet in enemy5_bullets:
        if stabbing_flag:
            if bullet.sword_collide(sword):
                stabbing_flag = False
        
        if bullet.player_collide(player):
            enemy5_bullets.remove(bullet)
            player.get_damage(slider_value*DAMAGE_FACTOR)
            gauge_index = random.randint(0,2)
            needle_algo(gauge_index)
        
        bullet.draw(display)

def draw():
    
    sword.update(x=player.x+20, y=player.y+5)
    player.draw(display)
    enemy1.draw(display)
    enemy2.draw(display)
    enemy3.draw(display)
    enemy4.draw(display)
    enemy5.draw(display)
    
    update_needle()
    
    check_for_collisions()
    
    
        
def timer():
    global timer1, deltat, bullet_rate_ind
    
    timer1 -= deltat
    
    if timer1 <= 0:  # Ready to fire.
        counter = random.randint(1,5)
        if counter == 1:
            enemy1_bullets.append(Bullets(enemy1.x, enemy1.y, player.x, player.y))
        if counter == 2:
            enemy2_bullets.append(Bullets(enemy2.x, enemy2.y, player.x, player.y))
        if counter == 3:
            enemy3_bullets.append(Bullets(enemy3.x, enemy3.y, player.x, player.y))
        if counter == 4:
            enemy4_bullets.append(Bullets(enemy4.x, enemy4.y, player.x, player.y))
        if counter == 5:
            enemy5_bullets.append(Bullets(enemy5.x, enemy5.y, player.x, player.y))
        timer1 = bullet_rate[bullet_rate_ind]  # Reset the timer.
        
    deltat = clock.tick(FPS) #milliseconds
    

def pygame_event_check():
    global run, bullet_rate_ind, slider_value, current_temp, current_heart, movement_speed, heart_ratio, prev_heart_ratio, temp_ratio, prev_temp_ratio
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == lvl_diff:
                bullet_rate_ind = diff_list.index(event.text)
        
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == speed_slider:
                slider_value = event.value
                speed_label.set_text("<font color='#FFFFFF'  size=2>"
                                     "Bullet Speed:"+str(slider_value*5)+ " Km/h")
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                current_temp = round(current_temp - 0.3, 2)
                temp_ratio = abs(((current_temp - base_temp)/base_temp))
                if temp_ratio > prev_temp_ratio:
                    player.get_damage(10)
                else:
                    player.get_health(10)
                prev_temp_ratio = temp_ratio
                skin_temp_label.set_text("<font color='#FFFFFF' size=2>"
                                        "Skin Temperature: <br>"
                                        "<font size=3>"
                                        "      "+str(current_temp)+" &deg;C")
                skin_temp_label.scroll_bar.hide()
            if event.key == pygame.K_UP:
                current_temp = round(current_temp + 0.3, 2)
                temp_ratio = abs(((current_heart - base_heart)/base_heart))
                if temp_ratio > prev_temp_ratio:
                    player.get_damage(10)
                else:
                    player.get_health(10)
                prev_temp_ratio = temp_ratio
                skin_temp_label.set_text("<font color='#FFFFFF' size=2>"
                                        "Skin Temperature: <br>"
                                        "<font size=3>"
                                        "      "+str(current_temp)+" &deg;C")
                skin_temp_label.scroll_bar.hide()
            if event.key == pygame.K_0:
                current_heart = round(current_heart - 1,3)
                heart_ratio = abs(((current_heart - base_heart)/base_heart))
                if heart_ratio > prev_heart_ratio:
                    player.get_damage(10)
                else:
                    player.get_health(10)
                prev_heart_ratio = heart_ratio
                heart_rate_label.set_text("<font color='#FFFFFF' size=2>"
                                     "Heart Rate: <br>"
                                     "<font size=3>"
                                     "      "+str(current_heart)+" bpm")
                movement_label.set_text("<font color='#FFFFFF' size=2.5>"
                                        "Movement Speed:<br>"
                                        "<font size=3>"
                                        "      "+str(round(int(movement_speed*5)))+" km/h")
                movement_label.scroll_bar.hide()
            if event.key == pygame.K_1:
                current_heart = round(current_heart + 1,3)
                heart_ratio = abs(((current_heart - base_heart)/base_heart))
                if heart_ratio > prev_heart_ratio:
                    player.get_damage(10)
                else:
                    player.get_health(10)
                heart_rate_label.set_text("<font color='#FFFFFF' size=2>"
                                     "Heart Rate: <br>"
                                     "<font size=3>"
                                     "      "+str(current_heart)+" bpm")
                movement_label.set_text("<font color='#FFFFFF' size=2.5>"
                                        "Movement Speed:<br>"
                                        "<font size=3>"
                                        "      "+str(round(int(movement_speed*5)))+" km/h")
                movement_label.scroll_bar.hide()
                
        manager.process_events(event)

def main_pygame():
    global deltat_s, run, slider_value
    #Setup
    run = True
    
    while run:
        
        deltat_s = deltat/1000 #seconds
        
        check_keys()
        
        draw()
        
        timer()
        
        pygame.display.update()
        
        health_score = int(((player.current_health/player.health_ratio)/player.health_bar_length*100))
        percent_txt = font.render(str(health_score)+'%', False, (0, 0, 0))
        
        display.blit(background, (0, 0))
        display.blit(percent_txt, (855,15))
        manager.draw_ui(display)
        manager.update(deltat_s)
        
        pygame_event_check()
            
    pygame.quit()

if __name__ == '__main__':
    main_pygame()
    