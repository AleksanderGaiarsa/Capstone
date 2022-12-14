import other_files.main_menu as main_menu
import other_files.leaderboard as main_leader
import other_files.game as main_game
import pygame
import sys

def main():
    pygame.init()

    run = True

    while(run):
        menu = main_menu.menu()
        
        if not menu.run:
            run = False
            break
        
        game = main_game.Shooting_Game(menu.bullet_rate_ind)
        leaderboard = main_leader.Leaderboard_Screen(menu.player_name, game.score)

        del menu, game, leaderboard

if __name__ == '__main__':
    main()

try:
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)

except Exception:
    import traceback
    traceback.print_exec()
print("end")