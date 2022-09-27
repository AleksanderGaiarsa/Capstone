#GUI Adjustable Game propreties
import pygame
import pygame_gui
import modules.calibration as calib


class GUI():
    def __init__(self, width, height, calibration:calib.Calibration):

        #Pygame GUI Setup
        self.manager = pygame_gui.UIManager((width, height))

        self.bullet_rate_ind = 1 #medium difficulty
        self.diff_list = ['Easy', 'Medium', 'Hard', 'Very Hard']
        self.bullet_rate = [1000, 500, 150, 50] #in milliseconds
        self.bullet_rate_ind = 1 #start difficulty of medium
        self.slider_value = 6 #start speed
        self.movement_speed = 5

        self.diff_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF'>"
                                                    'Difficulty',
                                                    relative_rect=pygame.Rect((3, 0), (width/6-8, 50)),
                                                    manager=self.manager)

        self.lvl_diff=pygame_gui.elements.UIDropDownMenu(options_list= self.diff_list,
                                        starting_option='Medium',
                                        relative_rect=pygame.Rect((3, 50), (width/6-8, 50)),
                                        manager=self.manager)

        self.speed_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF'  size=2>"
                                                    "Bullet Speed:"+str(self.slider_value*5)+ " Km/h",
                                                    relative_rect=pygame.Rect((3, 125), (width/6-8, 30)),
                                                    manager=self.manager)

        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((3, 145), (width/6-8, 50)),
                                                            start_value = 6, 
                                                            value_range = (2,15), 
                                                            manager=self.manager)

        self.skin_temp_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=2>"
                                                    "Skin Temperature: <br>"
                                                    "<font size=3>"
                                                    "      "+str(calibration.base_temp)+" &deg;C",
                                                    relative_rect=pygame.Rect((3, 220), (width/6-8, 50)),
                                                    manager=self.manager)
        self.skin_temp_label.scroll_bar.hide()

        self.heart_rate_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=2>"
                                                    "Heart Rate: <br>"
                                                    "<font size=3>"
                                                    "      "+str(calibration.base_heart)+" bpm",
                                                    relative_rect=pygame.Rect((3, 280), (width/6-8, 55)),
                                                    manager=self.manager)

        self.movement_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=2.5>"
                                                    "Movement Speed:<br>"
                                                    "<font size=3>"
                                                    "      "+str(self.movement_speed*5)+" km/h",
                                                    relative_rect=pygame.Rect((3, 345), (width/6-8, 50)),
                                                    manager=self.manager)
        self.movement_label.scroll_bar.hide()

        self.baseline_label = pygame_gui.elements.UITextBox(html_text="<font color='#FFFFFF' size=3>"
                                                    "<strong>Baseline Readings</strong><br>"
                                                    "<font size=2>"
                                                    "Skin Temperature="+str(calibration.base_temp)+"<br>"
                                                    "Heart Rate="+str(calibration.base_heart)+"bpm",
                                                    relative_rect=pygame.Rect((3, 500), (width/6-8, 90)),
                                                    manager=self.manager)