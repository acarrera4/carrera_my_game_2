#file created by Alec Carrera


'''
My goal is:

to add a lives left system 
*when you touch particles you lose life*
add sound when touch particles

'''

import pygame as pg
import os

# import settings 
from settings import *
from sprites import *
from images import *
from pygame import mixer
from sounds import *

mixer.init()
mixer.music.load("rock.win.wav")
mixer.music.set_volume(0.7)







# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")
# create game class in order to pass properties to the sprites file

class Game:
    def __init__(self):
        # init game window etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("my game")
        self.clock = pg.time.Clock()
        self.running = True
        print(self.screen)
    

    def new(self):
        # starting a new game
        self.score = 4
        self.score_player2 = 4

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.player_2 = Player2(self)
    
    
        self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        

        # self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        self.all_sprites.add(self.plat1)
    

        self.platforms.add(self.plat1)
        
        self.all_sprites.add(self.player_2)

        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat) 
            self.all_sprites.add(p)
            self.platforms.add(p)
        for i in range(0,10):
            m = Mob(20,20,(0,255,0))
            self.all_sprites.add(m)
            self.enemies.add(m)
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
                if event.key == pg.K_w:
                    self.player.jump()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player_2.jump()



    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # is this a method or a function?
        pg.display.flip()

        player1img = pg.image.load(os.path.join(img_folder, 'player_1_life_image.jpg')).convert()
        player1img_rect = player1img.get_rect()
        self.screen.blit(player1img, player1img_rect)
        player1img_rect.y = 1


        player2img = pg.image.load(os.path.join(img_folder, 'player_2_life_image.jpg')).convert()
        player2img_rect = player2img.get_rect()
        self.screen.blit(player2img, player2img_rect)



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
    
    def hurt_se(self):
        play_hurt_se = False
        if pg.sprite.spritecollide(self.player, self.enemies, False):
                mixer.music.play("rock.win.wav")

    def update(self):
        self.all_sprites.update()

        player_death = pg.sprite.spritecollide(self.player, self.enemies, False)
        if player_death:
            self.score -= 1
            print (self.score)
        
        player2_death = pg.sprite.spritecollide(self.player_2, self.enemies, False)
        if player2_death:
            self.score_player2 -= 1
            print (self.score_player2)
        
       # if self.score == 4:
       #     self.draw_text(60,"4", WHITE, 'arial', 50)



        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if hits[0].variant == "bouncey":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -PLAYER_JUMP
                else:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
        if self.player_2.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player_2, self.platforms, False)
            if hits:
                if hits[0].variant == "bouncey":
                    self.player_2.pos.y = hits[0].rect.top
                    self.player_2.vel.y = -PLAYER_JUMP
                else:
                    self.player_2.pos.y = hits[0].rect.top
                    self.player_2.vel.y = 0
    

    def hpbar(self):
        while self.score - 1:
            "bouncey"._vel*= -20
            
    


    

    clock = pg.time.Clock()
 


# instantiate the game class...
g = Game()

# kick off the game loop
while g.running:
    g.new()

pg.quit()