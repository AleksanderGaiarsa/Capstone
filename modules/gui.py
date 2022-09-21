#GUI Adjustable Game propreties
import pygame
import pygame_gui

WIDTH, HEIGHT = 1225, 600

#Pygame GUI Setup
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

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