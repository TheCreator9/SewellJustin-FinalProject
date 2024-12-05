import pygame
from pygame.locals import *

#Intializes system information/debug.
resolution = (750, 750)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('To the Stars!')
tile_size = 50


#Loads in necessary images
bg_img = pygame.image.load('bg_img.jpg')

def draw_grid():
    for line in range(0, 15):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (750, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, 750))

class World():
    def __init__(self, data):
        self.tile_list = []

        #Loads in necessary images
        cloud_img = pygame.image.load('cloud.png.png')
        star_img = pygame.image.load('star.png.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(cloud_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(star_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

#Class handles all player actions and logic.
class Player():
    def __init__(self, x, y):
        pc_char = pygame.image.load('pc_final.png')
        self.image = pygame.transform.scale(pc_char, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False

    def update(self):
        dx = 0
        dy = 0

        #Section gets the key pressed to preform actions of left-right movement and jumping.
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -3
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 1
        if key[pygame.K_RIGHT]:
            dx += 1


        #Applies gravity to PC.
        self.vel_y += 0.007
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #Applies collision to blocks
        for tile in world.tile_list:
            #check for collision in x direction
            if tile[1].colliderect(pygame.Rect(self.rect.x + dx, self.rect.y, self.width, self.height)):
                dx = 0
            if tile[1].colliderect(pygame.Rect(self.rect.x, self.rect.y + dy, self.width, self.height)):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        

        #Gets player coordinates.
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > 750:
            self.rect.bottom = 750
            dy = 0

        #Renders the player.
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


world_data = [
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
]

world = World(world_data)


def main():
    pygame.init()

    player = Player(100, 750 - 110)
    

    running = True
    while running:
        screen.blit(bg_img, (0,0))
        world.draw()
        player.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main() 