import pygame
import random
import pygame_gui
import modules.game_objects as g_obj
        
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


WIDTH, HEIGHT = 1225, 600
FONT = pygame.font.SysFont('Franklin Gothic Heavy', 33)
font = pygame.font.Font('freesansbold.ttf', 20)

player_image=pygame.image.load("./Graphics/player.png")
enemy_image=pygame.image.load("./Graphics/enemy.png")


bullet_rate_ind = 1 #medium difficulty
diff_list = ['Easy', 'Medium', 'Hard', 'Very Hard']
bullet_rate = [1000, 500, 150, 50] #in milliseconds
bullet_rate_ind = 1 #start difficulty of medium
slider_value = 6 #start speed
movement_speed = 5

#Other
DAMAGE_FACTOR = 1

enemy1_bullets = []
enemy2_bullets = []
enemy3_bullets = []
enemy4_bullets = []
enemy5_bullets = []


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
   
def check_for_collisions():
    global stabbing_flag, slider_value
    
    for bullet in enemy1_bullets:
        if stabbing_flag == True:
            if bullet.sword_collide(sword):
                stabbing_flag = False
        
        if bullet.player_collide(player):
            enemy1_bullets.remove(bullet)
            player.get_damage(slider_value*DAMAGE_FACTOR) 
        
        bullet.draw(display)
        
    for bullet in enemy2_bullets:
        if stabbing_flag:
            if bullet.sword_collide(sword):
                stabbing_flag = False
        
        if bullet.player_collide(player):
            enemy2_bullets.remove(bullet)
            player.get_damage(slider_value*DAMAGE_FACTOR)

        bullet.draw(display)
        
    for bullet in enemy3_bullets:
        if stabbing_flag:
            if bullet.sword_collide(sword):
                stabbing_flag = False
        
        if bullet.player_collide(player):
            enemy3_bullets.remove(bullet)
            player.get_damage(slider_value*DAMAGE_FACTOR)
        
        bullet.draw(display)
        
    for bullet in enemy4_bullets:
       if stabbing_flag:
           if bullet.sword_collide(sword):
               stabbing_flag = False
               
       if bullet.player_collide(player):
           enemy4_bullets.remove(bullet)
           player.get_damage(slider_value*DAMAGE_FACTOR)

       bullet.draw(display)
        
    for bullet in enemy5_bullets:
        if stabbing_flag:
            if bullet.sword_collide(sword):
                stabbing_flag = False
        
        if bullet.player_collide(player):
            enemy5_bullets.remove(bullet)
            player.get_damage(slider_value*DAMAGE_FACTOR)
        
        bullet.draw(display)

def draw():
    
    sword.update(x=player.x+20, y=player.y+5)
    player.draw(display)
    enemy1.draw(display)
    enemy2.draw(display)
    enemy3.draw(display)
    enemy4.draw(display)
    enemy5.draw(display)
    
    check_for_collisions()
    
    
    

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

class Shooting_Game():
    def __init__(self):
        #Pygame Setup
        self.pygame = pygame.init()
        pygame.display.set_caption("Game Simulation")
        self.fps = 60

        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill((200,104,65), (163, 0, self.display.get_width(), self.display.get_height())) #orange starting at 163
        self.background.fill((0,0,0),(160,0, 3, self.display.get_height())) #black line at 160-163 pixels
        self.background.fill((255,255,255), (0, 0, 160, self.display.get_height())) #white background

        self.clock = pygame.time.Clock()
        self.timer1 = 1000
        self.deltat = 0

        self.player = g_obj.Player(500,350,32,32, size=2, png_image="./Graphics/player.png")
        self.enemy = (  g_obj.Enemy(200,150,32,32, size=1.3, png_image="./Graphics/enemy.png"),
                        g_obj.Enemy(200,450,16,16, size=1.3, png_image="./Graphics/enemy.png"),
                        g_obj.Enemy(800,60,16,16, size=1.3, png_image="./Graphics/enemy.png"),
                        g_obj.Enemy(200,150,32,32, size=1.3, png_image="./Graphics/enemy.png"),
                        )
        
        self.run = True
        self.play()

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
        
    deltat = clock.tick(self.fps) #milliseconds

def play(self):
    global slider_value
    #Setup
    
    while(self.run):
        
        self.deltat_s = self.deltat/1000 #seconds
        
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
    Shooting_Game()
    