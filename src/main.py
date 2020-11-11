import pygame
import time
from src.observer import Observer

if __name__ == "__main__":
    pygame.init()
    observer = Observer()
    game_display = pygame.display.set_mode((observer.width, observer.height))
    observer.add_game_display(game_display)

    run = True
    target_fps = 60
    prev_time = time.time()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        observer.update()



        # Handle time
        curr_time = time.time()
        diff = curr_time - prev_time
        delay = max(1.0 / target_fps - diff, 0)
        time.sleep(delay)
        fps = 1.0 / (delay + diff)
        prev_time = curr_time

    pygame.quit()
    quit()
