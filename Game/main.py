import modules.main_menu as main_menu
import modules.leaderboard as main_leader
import modules.game as main_game
import pygame
import sys

def main():
    pygame.init()
    run = True

    while(run):
        menu = main_menu.menu()
        
        if not menu.run:
            run = False

        game = main_game.Shooting_Game(menu.bullet_rate_ind)
        leaderboard = main_leader.Leaderboard_Screen(menu.player_name, game.score)
    
    pygame.display.quit()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()