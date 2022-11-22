import pygame
import datetime 
import os
import json
import sys

class Leaderboard_Button():
    def __init__(self, image, bg_size:list, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.img_size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.img_size[0]*bg_size[0]), int(self.img_size[1]*bg_size[1])))
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Leaderboard(pygame.font.Font):
    def __init__(self, new_name, new_score):
        self.file_name = "highscore.json"
        self.score = 0
        self.font = pygame.font.Font("./Game/assets/font.ttf", 26)
        self.new_score = int(new_score) 
        self.new_name = new_name 

        if not os.path.isfile(self.file_name):
            self.on_empty_file()

    # So here's a check if the highscore file exists or not, and if
    # it doesn't it creates a file with an empty list in it (so the JSON-parser doesn't go bananans).
    def on_empty_file(self):
        empty_score_file = open(self.file_name,"w")
        empty_score_file.write("[]")
        empty_score_file.close()

    # Here we save the score as JSON.
    # At this point we should have loaded the previous scores already (but if we haven't, it will do it "again").
    # Then we append *this* score to the list of previous scores, then we sort it in a separate method by highest score,
    # and finally we write it to the highscore.json-file. Tada!
    def save_score(self):
        if not self.scores == None: # Make sure the prev. scores are loaded.
            new_json_score = { # Create a JSON-object with the score, name and a timestamp.
                    "name":self.new_name,
                    "score":self.new_score,
                    "time":str(datetime.datetime.now().time())
                    }

            self.scores.append(new_json_score) # Add the score to the list of scores.

            with open(self.file_name, 'w') as highscore_file:
                highscore_file.seek(0)
                json.dump(self.scores, highscore_file, indent=2) # Save the list of scores to highscore.json
                highscore_file.truncate()

            self.scores = self.sort_scores(self.scores) # Sort the scores.
            print(self.scores)

        else:
            self.load_previous_scores() # This is reeeally bad practice...
            self.save_score() # ...and lets hope loading works! 

    def sort_scores(self, json):
        # A somewhat dirty method for sorting the JSON entries... It works though!
        scores_dict = dict() # Create a dictionary object.
        sorted_list = list() # Create a list object.

        for obj in json:
            scores_dict[obj["score"]]=obj # Add every score to a dictionary with its score as key. Key collisions ensue...

        for key in sorted(scores_dict.keys(), reverse=True): # Read the sorted dictionary in reverse order (highest score first)...
            sorted_list.append(scores_dict[key]) # ...and add it to a list.

        return sorted_list # Tada! Returns a sorted list.

    # Reads the previous scores from the highscores.json-file
    # and adds it to a list (a python list object, that is).
    def load_previous_scores(self):
        with open(self.file_name) as highscore_file:
           self.scores = json.load(highscore_file)
           self.scores = self.scores

    # Just like every other draw method, this
    # paints the list. But this paints every score
    # in the list with a 20px padding to the next one.
    def draw(self, screen):
        padding_y = 0
        max_scores = 8 # We *could* paint every score, but it's not any good if you can't see them (because we run out of the screen).
        nbr_scores = 1
        for score in self.scores:
            if nbr_scores <= max_scores:
                leaderboard_txt = '{0:<20} {1:>15}'.format((str(nbr_scores)+". "+str(score["name"])), (str(score["score"])))
                leaderboard_txt = self.font.render(leaderboard_txt, True, pygame.Color('white'))
                leaderboard_txt_rect = leaderboard_txt.get_rect(center=(screen.get_width()/2,325+padding_y))
                screen.blit(leaderboard_txt, leaderboard_txt_rect)
                padding_y += 50
                nbr_scores += 1

class Leaderboard_Screen:
    def __init__(self, player_name, score):

        pygame.mixer.music.load('./Game/assets/Dance_of_the_Decorous.mp3')
        pygame.mixer.music.play(100)

        self.score = score

        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()
        pygame.display.set_caption("Menu")

        self.font = pygame.font.Font("./Game/assets/font.ttf", 40)
        self.font_large = pygame.font.Font("./Game/assets/font.ttf", 72)
        self.font_underline = self.font
        self.font_underline.set_underline(True)

        picture = pygame.image.load("./Game/assets/Background.png")
        self.bg = pygame.transform.scale(picture, (self.width, self.height))

        self.leaderboard = Leaderboard(player_name, score)
        self.leaderboard.load_previous_scores()
        self.leaderboard.save_score()

        self.end_game()

    def end_game(self):

        self.your_score_label = self.font_large.render('YOUR SCORE: ', True, pygame.Color('white'))
        self.your_score_rect = self.your_score_label.get_rect(center=(self.width/2-200, 125))

        self.score_label = self.font_large.render(str(self.score), True, pygame.Color('white'))
        self.score_rect = self.score_label.get_rect(center=(self.width/2+300, 125))

        self.leaderboard_label = self.font_underline.render('LEADERBOARD', True, pygame.Color('white'))
        self.leaderboard_label_rect = self.leaderboard_label.get_rect(center=(self.width/2, 250))

        self.main_menu_button = Leaderboard_Button(image=None, 
                                    bg_size=(1,1),
                                    pos=(self.width/2, self.height-100), 
                                    text_input="MAIN MENU",
                                    font=self.font, 
                                    base_color="#d7fcd4",
                                    hovering_color="White")

        while True:
                self.leader_mouse_pos = pygame.mouse.get_pos()
                
                pygame.display.update()

                self.display.blit(self.bg, (0, 0))
                self.display.blit(self.your_score_label, self.your_score_rect)
                self.display.blit(self.score_label, self.score_rect)
                self.display.blit(self.leaderboard_label, self.leaderboard_label_rect)
                self.leaderboard.draw(self.display)

                self.main_menu_button.update(self.display)
                self.main_menu_button.changeColor(self.leader_mouse_pos)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.main_menu_button.checkForInput(self.leader_mouse_pos):
                            pygame.display.quit()
                            return