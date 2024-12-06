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
restart_UI_orig = pygame.image.load('Restart1.png')
start_UI_orig = pygame.image.load('Start1.png')
quit_UI_orig = pygame.image.load('Quit1.png')
restart_UI_resize = pygame.transform.scale(restart_UI_orig, ((restart_UI_orig.get_width() * 3), (restart_UI_orig.get_height() * 3)))
start_UI_resize = pygame.transform.scale(start_UI_orig, ((start_UI_orig.get_width() * 3), (start_UI_orig.get_height() * 3)))
quit_UI_resize = pygame.transform.scale(quit_UI_orig, ((quit_UI_orig.get_width() * 3), (quit_UI_orig.get_height() * 3)))
title_logo_orig  = pygame.image.load('logo2.png')
title_logo_resize = pygame.transform.scale(title_logo_orig, ((title_logo_orig.get_width() / 1.5), (title_logo_orig.get_height() / 1.5)))

#Group variables for obs & goal sprites.
mov_obs = pygame.sprite.Group()
static_obs = pygame.sprite.Group()
goal_rocket = pygame.sprite.Group()

def draw_grid():
    for line in range(0, 15):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (750, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, 750))

#Class handles all UI buttons throughout the game. 
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):

        was_clicked = False

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                was_clicked = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return was_clicked

#Class handles the world the game is built on.
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
                #Following if statements determines what tile to place depending on value.
                #1 for cloud, 2 for star, 3 & 4 for moving and static obstacles, and 5 for exit.
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
                if tile == 5:
                    goal = Exit(col_count * tile_size, row_count * tile_size)
                    goal_rocket.add(goal)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

#Class handles all player actions and logic.
class Player():
    def __init__(self, x, y):
        self.reset(x,y)

    def update(self, death_state, win_state):
        dx = 0
        dy = 0

        #Section gets the key pressed to preform actions of left-right movement and jumping. Makes sure player is not dead in order to execute.
        if death_state == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -4
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 1
                self.direction = -1 #Handles sprite flpping.   
            if key[pygame.K_RIGHT]:
                dx += 1
                self.direction = 1 #Handles sprite flpping.
            
            #Following statement handles the logic of flipping the sprite.
            if self.direction == -1:
                self.image = pygame.transform.flip(self.pc_char_scaled, True, False)
            elif self.direction == 1:
                self.image = self.pc_char_scaled


        #Applies gravity to PC.
        self.vel_y += 0.05
        if self.vel_y > 1:
            self.vel_y = 1
        dy += self.vel_y

        #Applies collision to blocks
        for tile in world.tile_list:
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

        #Applies collison/win to exit.
        if pygame.sprite.spritecollide(self, goal_rocket, False):
            win_state = 1

        #Gets player coordinates.
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > 750:
            self.rect.bottom = 750
            dy = 0

        #Renders the player but only if death_state and win_state is inactive.
        if death_state == 0 and win_state == 0:
            screen.blit(self.image, self.rect)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return death_state, win_state

    #Function stores all the necessary values needed for reset on player death.
    def reset(self, x, y):
        pc_char = pygame.image.load('pc_final.png')
        self.pc_char_scaled = pygame.transform.scale(pc_char, (40, 60))
        self.image = self.pc_char_scaled
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

#Class handles all logic for moving blackhole obstacle.
class MovingObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        blackhole_image = pygame.image.load('blackhole.png')
        self.image = pygame.transform.scale(blackhole_image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.move = 0
    
    def update(self):
        self.rect.x += self.direction
        self.move += 1
        if abs(self.move) > 25:
            self.direction *= -1
            self.move *= -1

#Class handles all logic for static blackhole obstacle.     
class StaticObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        blackhole_image = pygame.image.load('blackhole.png')
        self.image = pygame.transform.scale(blackhole_image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Class handles the goal at the end of the game.
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        rocket_image = pygame.image.load('rocket.png')
        self.image = pygame.transform.scale(rocket_image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Following data set constitutes the level design. Inputs values along a grid to determine where objects are placed. Consult the World() class for further info.
world_data = [
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 1],
[1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 4, 0, 0, 2, 2, 4, 4, 4, 1],
[1, 0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data) #Code doesn't work unless this variable is here, I don't know why.

def main():
    pygame.init()

    #Preliminary variables needed for game.
    player = Player(50, 750 - 130)
    death_state = 0
    win_state = 0
    main_menu = True
    win_menu = False

    #Creates objects for each of the buttons.
    restart = Button(screen.get_width() // 2 - 90, screen.get_height() // 2 - 90, restart_UI_resize)
    start_button = Button(screen.get_width() // 2 - 350, screen.get_height() // 2, start_UI_resize)
    exit_button = Button(screen.get_width() // 2 + 150, screen.get_height() // 2, quit_UI_resize)
    exit_button2 = Button(screen.get_width() // 2 - 90, screen.get_height() // 2 - 30, quit_UI_resize)

    running = True
    while running:
        internal_clock.tick(fps)
        screen.blit(bg_img, (0, 0))

        #If player won, it'll display win menu.
        if win_menu:
            if restart.draw():
                player.reset(100, 750 - 110)
                win_state = 0
                win_menu = False 
            if exit_button2.draw():
                running = False
        #At beginning of game, it'll show main menu.
        elif main_menu:
            screen.blit(title_logo_resize, (screen.get_width() / 2 - 220, screen.get_height() / 2 - 315))
            if start_button.draw():
                main_menu = False
            if exit_button.draw():
                running = False
        else:
            world.draw()

            if death_state == 0 and win_state == 0:
                mov_obs.update()

            #Draws objects to screen.
            mov_obs.draw(screen)
            static_obs.draw(screen)
            goal_rocket.draw(screen)

            #Updates player info depending on current game state.
            death_state, win_state = player.update(death_state, win_state)

            if death_state == 1:
                if restart.draw():
                    player.reset(100, 750 - 110)
                    death_state = 0
            if win_state == 1:
                win_menu = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main() 