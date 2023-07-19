import pygame
import pygame.mixer
from SpectralEscape import main


#  Initialize pygame and mixer (for sound)
pygame.init()
pygame.mixer.init()

# Window
HEIGHT = 600
WIDTH = 800

#  Initialize clock (for FPS)
clock = pygame.time.Clock()

#  ---The Game---
def menu():
    #  Initialize screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Main menu")
    #  Load images
    img_menu = pygame.image.load("interface/menu.png")
    img_instructions = pygame.image.load("interface/instructions.png")
    img_pre_game = pygame.image.load("interface/pre_game.png")
    #  Set First image
    img = img_menu
    #  Initialize control variable
    game_over = False
    while not game_over:
        pygame.display.update()
        screen.blit(img, (0, 0)) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Click on buttons
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if img == img_menu:
                    if x > 0 and x < 800 and y > 0 and y < 600:
                        if x > 238 and x < 553 and y > 243 and y < 293:
                            img = img_pre_game
                        if x > 238 and x < 553 and y > 317 and y < 365:
                            print("Instructions")
                            img = img_instructions
                        if x > 238 and x < 553 and y > 392 and y < 440:
                            print("Quit")
                            game_over = True
                elif img == img_instructions:
                    if x > 0 and x < 800 and y > 0 and y < 600:
                        if x > 28 and x < 110 and y > 496 and y < 570:
                            img = img_menu
                elif img == img_pre_game:
                    if x > 0 and x < 800 and y > 0 and y < 600:
                        if x > 160 and x < 380 and y > 209 and y < 435:
                            main(1)
                            img = img_menu
                        if x > 470 and x < 688 and y > 209 and y < 435:
                            main(2)
                            img = img_menu
                        if x > 28 and x < 110 and y > 496 and y < 570:
                            img = img_menu
        # Hover effect on buttons
        if img == img_menu:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if x > 0 and x < 800 and y > 0 and y < 600:
                    if x > 238 and x < 553 and y > 243 and y < 293:
                        img_pong_buton = pygame.image.load("interface/play_button.png")
                        screen.blit(img_pong_buton, (238, 240))
                        pygame.display.update()
                    if x > 238 and x < 553 and y > 317 and y < 365:
                        img_maze_buton = pygame.image.load("interface/inst_button.png")
                        screen.blit(img_maze_buton, (238, 315))
                        pygame.display.update()    
                    if x > 238 and x < 553 and y > 392 and y < 440:
                        img_quit_buton = pygame.image.load("interface/quit_button.png")
                        screen.blit(img_quit_buton, (238, 390))
                        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    pygame.mixer.quit()
    

if __name__ == "__main__":
    menu()