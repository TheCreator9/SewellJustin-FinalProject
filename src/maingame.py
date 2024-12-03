import pygame
from pygame.locals import *


def main():
   #Intializes pygame and screen information
   pygame.init()
   resolution = (1920, 1080)
   screen = pygame.display.set_mode(resolution)
   pygame.display.set_caption('To the Stars!')

   #Loads in necessary images

   bg_img = pygame.image.load('bg_img.jpg')


   running = True
   while running:
      screen.blit(bg_img, (0,0))


      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            pygame.display.update()

pygame.quit()


if __name__ == "__main__":
    main()

    
