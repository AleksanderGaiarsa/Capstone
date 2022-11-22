import modules.main_menu as main_menu
import modules.leaderboard as main_leader
import modules.game as main_game
import modules.ble as ble
import pygame
import sys
import threading
import asyncio
import queue

#Queue to ble: {'Command':'disconnect', 'Service':None, 'Characteristic':None, 'Value':None}

def thread_func(q_to_ble, q_from_ble, loop):
    loop.run_until_complete(ble.ble_main(q_to_ble, q_from_ble))


def main():
    pygame.init()
    pygame.mixer.init()

    q_to_ble = queue.Queue()
    q_from_ble = queue.Queue()

    loop = asyncio.get_event_loop()
    ble_thread = threading.Thread(target=thread_func, args=(q_to_ble, q_from_ble, loop)).start()

    run = True

    while(run):
        menu = main_menu.menu()
        
        if not menu.run:
            run = False
            break
        
        game = main_game.Shooting_Game(menu.bullet_rate_ind, q_to_ble, q_from_ble)
        
        leaderboard = main_leader.Leaderboard_Screen(menu.player_name, game.score)

        del menu, game, leaderboard
        
    q_to_ble.put({'Command':'disconnect', 'Service':None, 'Characteristic':None, 'Value':None})

    try:
        ble_thread.join()
    except:
        pass

    try:
        pygame.display.quit()
        pygame.quit()
        sys.exit(0)
    except Exception:
        import traceback
        traceback.print_exec()

    print("end")


if __name__ == '__main__':
    main()