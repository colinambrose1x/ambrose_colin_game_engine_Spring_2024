# This file was created by Colin Ambrose

# importing a items from a file

# rules, freedom, verb
# scrolling map
#jumping, breaking walls
# another player
'''
Sources:
Kids can code: https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2001 
Stack overflow
Redit
TechwithTim

BETA Goals:
*animated spirtes

Primary Goal: add player 2

'''
import pygame as pg
from setting import *
from sprites import *
from utils import *
from random import randint
import sys
from os import path
# added this math function to round down the clock
from math import floor
import random
clock = pg.time.Clock()
#cooldown class
# class Cooldown():
#     def __init__(self):
#         self.current_time = 0
#         self.event_time = 0
#         self.delta = 0
#     def ticking(self):
#         self.current_time = floor((pg.time.get_ticks())/1000)
#         self.delta = self.current_time - self.event_time
#     def countdown(self, x):
#         x = x - self.delta
#         if x != None:
#             return x
#     def event_reset(self):
#         self.event_time = floor((pg.time.get_ticks())/1000)
#     def timer(self):
#         self.current_time = floor((pg.time.get_ticks())/1000)

# create a game class 
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.all_sprites = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.snd_folder = path.join(game_folder, 'sounds')
        # pull images from folders 
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'theBell.png')).convert_alpha()
        self.player2_img = pg.image.load(path.join(img_folder, 'testImage.png')).convert_alpha()
        self.map_data = []
        self.cooldown = Timer(self)
        self.cooling = False

        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    # Create run method which runs the whole GAME
  

    def new(self):

         # loading sound for use...not used yet
        # pg.mixer.music.load(path.join(self.sound_folder, 'soundtrack2.mp3'))
        self.collect_sound = pg.mixer.Sound(path.join(self.snd_folder, 'mixkit-arcade-video-game-bonus-2044.mp3'))
        
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.deathblocks = pg.sprite.Group()
        self.speedboost = pg.sprite.Group()
        self.speedbump = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        self.pew_pews2 = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.player2 = pg.sprite.Group()
        self.dividers = pg.sprite.Group()
        # self.mob2 = pg.sprite.Group()
        # self.player2 = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            # use a variable and it shows up on the game where it has it in map.txt
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'p':
                    #finds thepalyers starting coordinates
                    self.p1col = col
                    self.p1row = row
                    self.p1 = Player(self, self.p1col, self.p1row)
                if tile == 'P':
                    #finds thepalyers starting coordinates
                    self.p2col = col
                    self.p2row = row
                    self.p2 = Player2(self, self.p2col, self.p2row)
                if tile == 'd':
                    Deathblock(self, col, row)
                if tile == 'S':
                    Speedboost(self, col, row)
                if tile == 'B':
                    Speedbump(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'D':
                    Divider(self, col, row)
                # if tile == 'm':
                #     Mob2(self, col, row)

    # AI
    def respawn_coins(self):
        num_coins = len(self.coins)
        respawn_threshold = 3  # Adjusted threshold for testing
        print("Number of coins:", num_coins)
        if num_coins < respawn_threshold:
            for _ in range(respawn_threshold - num_coins):
                max_attempts = 100  # Maximum number of attempts for generating a valid position
                attempts = 0
                while attempts < max_attempts:
                    x = random.randint(0, WIDTH // TILESIZE)
                    y = random.randint(0, HEIGHT // TILESIZE)
                    print("Attempting to respawn coin at:", x, y)
                    wall_collision = any(isinstance(sprite, Wall) for sprite in self.all_sprites.sprites())
                    coin_collision = any(sprite.rect.collidepoint(x, y) for sprite in self.coins.sprites())
                    if not wall_collision and not coin_collision:
                        print("Valid position found for new coin.")
                        Coin(self, x, y)
                        break  # Break out of the while loop once a valid position is found
                    else:
                        print("Position occupied. Trying another position.")
                        attempts += 1
                else:
                    print("Maximum attempts reached. Cannot respawn coin.")
                    break  # Break out of the for loop if maximum attempts are reached



    
    def run(self):         
        # runs game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.dt = clock.tick(60) / 1000  # Convert milliseconds to seconds

            self.all_sprites.update()
            self.events()
            self.update()
            self.draw()
    def quit(self):
         pg.quit()
         sys.exit()


    def update(self):
        
        self.respawn_coins()  # Call the method to respawn coins
        self.all_sprites.update()
        # self.test_timer.ticking()

    # makes grid appear on screen
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    #start screen
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press any button to begin/shoot the other player can collect coins to to win", 24, WHITE, 2, 3)
        pg.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    # shows clock on screen
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)
    def draw(self):
        # draws the screen of the game
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, str(self.p1.moneybag), 64, WHITE, 30, 21)
            self.draw_text(self.screen, str(self.p2.moneybag), 64, WHITE, 1, 0.75)
            #self.draw_text(self.screen, str(self.test_timer.countdown(45)), 24, WHITE, WIDTH/2 - 32, 2)
            pg.display.flip()


    # def draw_text(self, surface, text, size, color, x, y):
    #     font_name = pg.font.match('arial')
    #     font = pg.font.Font(font_name, size)
    #     text_surface = font.render(text, True, color)
    #     text_rect = text_surface.get_rect()
    #     text_rect.topleft = (x,y)
    #     surface.blit(text_surface, text_rect)

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
        
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
####################### Instantiate game... ###################
g = Game()
g.show_start_screen()
# g.show_go_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()
    