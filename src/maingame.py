import pygame
from pygame.locals import *

#Intializes system information/debug.
resolution = (750, 750)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('To the Stars!')
tile_size = 50
internal_clock = pygame.time.Clock()
fps = 60


#Loads in necessary images
bg_img = pygame.image.load('bg_img.jpg')

mov_obs = pygame.sprite.Group()
static_obs = pygame.sprite.Group()

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
                if tile == 3:
                    mov_blackhole = MovingObstacle(col_count * tile_size, row_count * tile_size + 15)
                    mov_obs.add(mov_blackhole)
                if tile == 4:
                    blackhole = StaticObstacle(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    static_obs.add(blackhole)
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

    def update(self, death_state):
        dx = 0
        dy = 0

        #Section gets the key pressed to preform actions of left-right movement and jumping. Makes sure player is not dead in order to execute.
        if death_state == 0:
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

        #Applies collision/death to enemies.
        if pygame.sprite.spritecollide(self, mov_obs, False):
            death_state = 1
        if pygame.sprite.spritecollide(self, static_obs, False):
            death_state = 1

        #Gets player coordinates.
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > 750:
            self.rect.bottom = 750
            dy = 0

        #Renders the player but only if death_state is inactive.
        if death_state == 0:
            screen.blit(self.image, self.rect)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return death_state


class MovingObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('blackhole.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.move = 0
    
    def update(self):
        self.rect.x += self.direction
        self.move += 1
        if abs(self.move) > 50:
            self.direction *= -1
            self.move *= -1
    
class StaticObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        blackhole_image = pygame.image.load('blackhole.png')
        self.image = pygame.transform.scale(blackhole_image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
[0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0],
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
]

world = World(world_data)

def main():
    pygame.init()

    player = Player(100, 750 - 110)
    death_state = 0

    running = True
    while running:
        internal_clock.tick(fps)
        screen.blit(bg_img, (0,0))
        world.draw()

        if death_state == 0:
            mov_obs.update()
        
        mov_obs.draw(screen)
        static_obs.draw(screen)


        death_state = player.update(death_state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main() 