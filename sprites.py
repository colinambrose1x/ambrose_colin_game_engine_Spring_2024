# This file was created by: Colin Ambrose

# write a player class
from os import path
import pygame as pg
from setting import *
from utils import *
import random
from random import randint
vec =pg.math.Vector2

# needed for animated sprite
SPRITESHEET = "theBell.png"
SPRITESHEET2 = "testImage.png"
# needed for animated sprite
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
# needed for animated sprite

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image
    


# _________ Player Class___________
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # self.shoot_delay = 500000  # Time between shots in milliseconds
        # self.last_shot = pg.time.get_ticks()  # Time when the player last shot
        self.last_shot_time = 0 
         # Initialize the last shot time
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image = game.player_img
        #self.image.fill(GREEN)
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        # needed for animated sprite
        self.load_images()  
        self.image = self.standing_frames[0]              
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 200
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        self.material = True
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False
        #finds player spawn
    def detath(self):
        self.x = self.game.p1col*TILESIZE
        self.y = self.game.p1row*TILESIZE
        print("You Died")
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vx = -self.speed  
        if keys[pg.K_RIGHT]:
            self.vx = self.speed  
        if keys[pg.K_UP]:
            self.vy = -self.speed 
        if keys[pg.K_DOWN]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        if keys[pg.K_RSHIFT]:
            # when rihtshift is pressed then it shoots
            self.shoot()
    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy
    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
            

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.
    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    
    def shoot(self):
        current_time = pg.time.get_ticks() 
         # Get the current time in milliseconds
        if current_time - self.last_shot_time >= 120:  
            p = PewPews(self.game, self.rect.x, self.rect.y)
            self.last_shot_time = current_time 
             # Update the last shot time
            print("Player shot!")
        else:
            print("Cannot shoot yet. Cooldown in progress.")
            
    #player wall collisions 
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y


#PLAYER DIVIDER
    def collide_with_dividers(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.dividers, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.dividers, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y


    # player group collisions
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            for hit in hits:
                if str(hit.__class__.__name__) == "Coin":
            # if str(hits[0].__class__.__name__) == "Coin":
                    self.moneybag += 2
                    self.game.collect_sound.play()
                    hit.respawn() 
            # if str(hits[0].__class__.__name__) == "Projectile":
            #     self.moneybag += 1
            if str(hits[0].__class__.__name__) == "Deathblock":
                self.detath()
            if str(hits[0].__class__.__name__) == "Speedboost":
                self.speed += 200
            if str(hits[0].__class__.__name__) == "Speedbump":
                self.speed -= 200
            if str(hits[0].__class__.__name__) == "Mob":
                self.detath()
            if str(hits[0].__class__.__name__) == "PewPews2":
                self.detath()
                self.moneybag -= 1

        # def collide_with_group(self, group, kill):
        #     hits = pg.sprite.spritecollide(self, group, kill)
        # if hits:
        #     for hit in hits:
        #         if str(hit.__class__.__name__) == "Coin":
        #             self.moneybag += 1
        #             self.game.collect_sound.play()
        #             hit.respawn() 
            

    def update(self):

        #    # Check if enough time has passed since the last shot
        # now = pg.time.get_ticks()
        # if now - self.last_shot >= self.shoot_delay:
        #     # Handle shooting logic here
        #     self.get_keys()  # Check for shooting input
        #     if pg.key.get_pressed()[pg.K_RSHIFT]:
        #         self.last_shot = now  

        self.animate()
        self.get_keys()
        self.get_keys()

        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        self.collide_with_walls('x')

        self.rect.y = self.y
        self.collide_with_walls('y')

        self.rect.x = self.x
        self.collide_with_dividers('x')

        self.rect.y = self.y
        self.collide_with_dividers('y')

        self.collide_with_group(self.game.coins, True)
        # self.collide_with_group(self.game.projectiles, True)
        self.collide_with_group(self.game.deathblocks, False)
        self.collide_with_group(self.game.speedboost, True)
        self.collide_with_group(self.game.speedbump, True)
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.pew_pews2, False)
        # self.collide_with_group(self.game.dividers, False)

        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")




# _________________________ Player 2 Class_____________________________
class Player2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.last_shot_time = 0
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image = game.player_img
        #self.image.fill(GREEN)
        self.spritesheet2 = Spritesheet(path.join(img_folder, SPRITESHEET2))
        # needed for animated sprite
        self.load_images()  
        self.image = self.standing_frames[0]              
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 200
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        self.material = True
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False
        #finds player spawn
    def detath(self):
        self.x = self.game.p2col*TILESIZE
        self.y = self.game.p2row*TILESIZE
        print("You Died")
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vx = -self.speed  
        if keys[pg.K_d]:
            self.vx = self.speed  
        if keys[pg.K_w]:
            self.vy = -self.speed 
        if keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        if keys[pg.K_e]:
            self.shoot2()
   
    def shoot2(self):
        current_time = pg.time.get_ticks()  # Get the current time in milliseconds
        if current_time - self.last_shot_time >= 120:  # Check if it's been at least 2 seconds
            p = PewPews2(self.game, self.rect.x, self.rect.y)
            self.last_shot_time = current_time  # Update the last shot time
            print("Player shot!")
        else:
            print("Cannot shoot yet. Cooldown in progress.")

    def load_images(self):
        self.standing_frames = [self.spritesheet2.get_image(0,0, 32, 32), 
                                self.spritesheet2.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.
    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    #player wall collisions 
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

#PLAYER DIVIDER
    def collide_with_dividers(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.dividers, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.dividers, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # player group collisions
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 2
                self.game.collect_sound.play()
            # if str(hits[0].__class__.__name__) == "Projectile":
            #     self.moneybag += 1
            if str(hits[0].__class__.__name__) == "Deathblock":
                self.detath()
            if str(hits[0].__class__.__name__) == "Speedboost":
                self.speed += 200
            if str(hits[0].__class__.__name__) == "Speedbump":
                self.speed -= 200
            if str(hits[0].__class__.__name__) == "Mob":
                self.detath()
            if str(hits[0].__class__.__name__) == "PewPews":
                self.detath()
                self.moneybag -= 1
    def update(self):

        # needed for animated sprite
        self.animate()
        self.get_keys()
        self.get_keys()

        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
       
        self.collide_with_walls('x')
        self.rect.y = self.y
        
        self.collide_with_walls('y')

        self.rect.x = self.x
       
        self.collide_with_dividers('x')
        self.rect.y = self.y
        
        self.collide_with_dividers('y')

        self.collide_with_group(self.game.coins, True)
        # self.collide_with_group(self.game.projectiles, True)
        self.collide_with_group(self.game.deathblocks, False)
        self.collide_with_group(self.game.speedboost, True)
        self.collide_with_group(self.game.speedbump, True)
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.pew_pews, False)
        # self.collide_with_group(self.game.dividers, False)

        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")



#___________________________________________ Mob Class ___________________________________

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        #self.image = self.game.mob_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1

    # mob colliosn method
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        #mob movement
        if self.rect.x < self.rect.x:
            self.vx = 100
        # if self.rect.x > self.game.player.rect.x:
        #     self.vx = -100    
        if self.rect.y < self.rect.y:
            self.vy = 100
        # if self.rect.y > self.game.player.rect.y:
        #     self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')







# ___________________________________wall class_______________________________
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    
class Divider(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.dividers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    

#__________________________________________PewPews___________________________________
class PewPews(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.vx, self.vy = 200, 200
        self.speed = 200
        self.moneybag = 0
        print("I created a pew pew...")
        # when the pew pew is shot it will say it is shot to show that it is happening


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y


    def collide_with_group(self, group, kill):
     hits = pg.sprite.spritecollide(self, group, kill)
     if hits:
        for hit in hits:
            if isinstance(hit, Mob):
                self.kill()
            if isinstance(hit, Wall):
                self.kill()
            elif isinstance(hit, Coin):
                self.kill
            # elif isinstance(hit, Player2):
            #      hit.moneybag += 1
            #      self.kill()

                
    def update(self):
        self.collide_with_group(self.game.mobs, True)
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.walls, False)
        self.rect.y -= self.speed
        # self.rect.x += self.speed
        # will destory mobs when it hits it
        # self.x += self.vx * self.game.dt
        self.y -= self.vy * self.game.dt
        self.rect.x = self.x
       
        self.collide_with_walls('x')
        self.rect.y = self.y
        
        self.collide_with_walls('y')
        # self.collide_with_group(self.game.player2, False)
        

#______________________PEWPEWS 2_____________________________________
class PewPews2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pew_pews2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.vx, self.vy = 200, 200
        self.speed = 100
        moneybag = 0
        print("I created a pew pew...")
        # creating the design of the pew pew
        # when the pew pew is shot it will say it is shot to show that it is happening

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_group(self, group, kill):
     hits = pg.sprite.spritecollide(self, group, kill)
     if hits:
        for hit in hits:
            if isinstance(hit, Mob):
                self.kill()
            if isinstance(hit, Wall):
                self.kill()
            elif isinstance(hit, Coin):
                 self.kill
            # elif isinstance(hit, Player):
            #     self.kill()

    def update(self):
        self.collide_with_group(self.game.mobs, True)
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.walls, False)
        self.rect.y += self.speed
        # self.rect.x -= self.speed
        # will destory mobs when it hits it
        # self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
       
        self.collide_with_walls('x')
        self.rect.y = self.y
        
        self.collide_with_walls('y')
        # self.collide_with_group(self.game.player, True)


#________________________________________Coin class______________________________________
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.cooling = False
            # Add a timer for the next spawn
        # self.spawn_delay = random.randint(10000, 50000) 
        #  # Random delay between 1 to 5 seconds
        # self.spawn_timer = 0  
        # Timer to count the time passed since last spawn

    def respawn(self):
        # Respawn the coin at a new position
        self.rect.x = random.randint(0, WIDTH // TILESIZE) * TILESIZE
        self.rect.y = random.randint(0, HEIGHT // TILESIZE) * TILESIZE

    # def update(self):
        # Increment the timer
        # if not self.cooling:
        #     self.spawn_timer = 0  # Reset timer
    
        #     self.spawn(random.randint(0, WIDTH // TILESIZE), random.randint(0, HEIGHT // TILESIZE))
        #     self.game.cooldown.cd = 4
        #     self.cooling= True
        # if self.game.cooldown.cd < 1:
        #     self.cooling = False

#_________________________ Deathblock_________________________________________________
class Deathblock(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.deathblocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


#___________________________________________Speed changers____________________________________
class Speedboost (pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.speedboost
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Speedbump (pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.speedbump
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# class Mob2(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.mobs
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         # self.image = game.mob_img
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(ORANGE)
#         # self.image = self.game.mob2_img
#         # self.image.set_colorkey(BLACK)
#         self.rect = self.image.get_rect()
#         # self.hit_rect = MOB_HIT_RECT.copy()
#         self.hit_rect.center = self.rect.center
#         self.pos = vec(x, y) * TILESIZE
#         self.vel = vec(0, 0)
#         self.acc = vec(0, 0)
#         self.rect.center = self.pos
#         self.rot = 0
#         self.chase_distance = 500
#         # added
#         self.speed = 100
#         self.chasing = True
#         # self.health = MOB_HEALTH
#         self.hitpoints = 100
#     def sensor(self):
#         if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
#             self.chasing = True
#         else:
#             self.chasing = False
#     def update(self):
#         if self.hitpoints <= 0:
#             self.kill()
#         # self.sensor()
#         if self.chasing:
#             self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
#             self.image = pg.transform.rotate(self.game.mob2_img, self.rot)
#             self.rect = self.image.get_rect()
#             self.rect.center = self.pos
#             self.acc = vec(self.speed, 0).rotate(-self.rot)
#             self.acc += self.vel * -1
#             self.vel += self.acc * self.game.dt
#             # equation of motion
#             self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
#             # hit_rect used to account for adjusting the square collision when image rotates
#             self.hit_rect.centerx = self.pos.x
#             collide_with_walls(self, self.game.walls, 'x')
#             self.hit_rect.centery = self.pos.y
#             collide_with_walls(self, self.game.walls, 'y')
#             self.rect.center = self.hit_rect.center