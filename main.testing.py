# File created by: Chris Cozort
# Agenda:
# gIT GITHUB    
# Build file and folder structures
# Create libraries
# testing github changes
# I changed something - I changed something else tooooo!

# This file was created by: Chris Cozort
# Sources: http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
# Sources: 

'''
Game structure:
GOALS; RULES; FEEDBACK; FREEDOM
My goal is:

Slime mob (need to create new mob class that jumps)

A mob that bounces along the floor...
Player gets bounced away when colliding 

Feature Creep

Reach goal:
use images and animated sprites...
create rotating that rotates only when it goes in a direction

'''

# import libs
import pygame as pg
import os
# import settings 
from settings import *
from sprites import *
from math import *
from math import ceil
from os import path
# from pg.sprite import Sprite

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")



# create game class in order to pass properties to the sprites file

class Cooldown():
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
        # print(self.delta)
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)


class Game:
    def __init__(self):
        # init game window etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("my game")
        self.clock = pg.time.Clock()
        self.running = True
        self.score = 0
        self.win = False
        self.lose = False
    
    # to add images sounds etc copy below...and add this to the new method below...
  
    def new(self):
        # starting a new game
        self.score = 0

        # added to load data

        self.cd = Cooldown()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.plat_list = []
        self.enemies = pg.sprite.Group()
        self.attached_items = pg.sprite.Group()
        self.player = Player(self)
        self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        # self.coin1 = Coin(asdfasdf)
        # self.all_sprites.add(coin1)
        # self.coins.add(coin1)
        # self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        self.all_sprites.add(self.player)

        self.all_sprites.add(self.plat1)
        self.platforms.add(self.plat1)
        
        
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for i in range(0,15):
            p = Platform(randint(0,WIDTH-50), randint(0,HEIGHT-50), 100, 25, BLACK, "normal")
            self.all_sprites.add(p)
            self.platforms.add(p)
            self.plat_list.append(p)
            if i != 0:
                print(abs(self.plat_list[i-1].rect.x - self.plat_list[i].rect.x) > 25 and
                      abs(self.plat_list[i-1].rect.y - self.plat_list[i].rect.y) > 25)  
                if (abs(self.plat_list[i-1].rect.x - self.plat_list[i].rect.x) > 100 and
                      abs(self.plat_list[i-1].rect.y - self.plat_list[i].rect.y) > 100):
                    print("i need to adjust this platform...") 
                    p.image.fill(RED)
                    p.rect.x -= 50
                    p.rect.y -= 50
                self.all_sprites.add(p)
                self.platforms.add(p)
                self.plat_list.append(p)
            
        for i in range(0,10):
            m = Mob(self, 20,20,(0,255,0))
            self.all_sprites.add(m)
            self.enemies.add(m)
        self.start_score = len(self.platforms)
        self.cd.timer()
        self.run()
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
    def update(self):
        self.all_sprites.update()
        self.cd.ticking()
        # checking to see if timer has run out  
        if self.cd.delta > 10:
            pass
            # print("you ran out of time and you lose!")
        
        # check to see if we collide with enemyd
        mhits = pg.sprite.spritecollide(self.player, self.enemies, False)
        if mhits:
            self.player.health -= 10
            mhits[0].attached_now = True
            self.enemies.remove(mhits[0])
            self.attached_items.add(mhits[0])
            self.score -= 1
        # if mhits:
        #     if self.player.vel.x < 0:
        #         self.player.pos.x += 5
        #     if self.player.vel.x > 0:
        #         self.player.pos.x -= 5
        #     if self.player.vel.y > 0:
        #         self.player.pos.y -= 5
            
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if abs(self.player.vel.x) > abs(self.player.vel.y):
                    if self.player.vel.x > 0:
                        pass
                        # print("Im going faster on the x and coming from the left...")
                if hits[0].variant == "disappearing":
                    hits[0].kill()
                elif hits[0].variant == "bouncey":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -PLAYER_JUMP
                elif hits[0].variant == "winner" and len(self.enemies) == 0:
                    self.win = True
                else:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
    
    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_health_bar(self.screen, self.player.rect.x, self.player.rect.y, self.player.health)
        self.draw_text(str(self.cd.delta), 24, WHITE, 50, 50)
        if self.cd.delta > 10:
            if self.score > 5:
                self.draw_text("if you win...", 24, WHITE, WIDTH/2, 100)
            else:
                self.draw_text("you lose...", 24, WHITE, WIDTH/2, 100)

        if not self.win:
            # self.draw_text(str(self.player.rot), 24, WHITE, WIDTH/2, HEIGHT/2)
            self.draw_text(str(self.score), 24, WHITE, WIDTH/2, HEIGHT/2)
        else:
            self.draw_text("You win!", 24, WHITE, WIDTH/2, HEIGHT/2)

        # is this a method or a function?
        pg.display.flip()
    def draw_health_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(surf, CYAN, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)

# instantiate the game class...
g = Game()

# kick off the game loop
while g.running:
    g.new()

pg.quit()