# This file was created by: Keawe Ainoa 

# import libraries and modules


import pygame as pg
from settings import *
from sprites import *
import random
import sys
from os import path

HEALTH = 10
#def create_account():


# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        # self.load_data()
    def load_data(self):
        global map_choice
        game_folder = path.dirname(__file__)
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, map_choice), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    # Create run method which runs the whole GAME
    def new(self):
        self.load_data()
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        #Loops through all the positions in the grid
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)   
                if tile == 'M':
                    Mob(self, col, row)
                if tile != '1':
                    number = random.randint(1,80)
                    if number == 4:
                        PowerUp(self, col, row)
                        #self.power_ups.count += 1
                if tile == "C":
                    Coin(self,col,row)
                if tile != '1':
                    number = random.randint(1,100)
                    if number == 4:
                        Coin(self, col, row)
                        #Coin.count += 1
                #if self.coins.count < 5:
                    #print ("I have less than 5 coins")

    #Define the run function that will run the game
    def run(self):
        # 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    #define a quit function
    def quit(self):
         pg.quit()
         sys.exit()
    #runs all code that draws sprites and updates their position
    def update(self):
        self.all_sprites.update()
    
    #draw a grid for the map
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    #define function to draw text in draw() function
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)

    #define function for future uses to choose/change maps
    def change_level(self, lvl):
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # reset criteria for changing level
        self.player.moneybag = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        # repopulate the level with stuff
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)   
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'L':
                    Interactable_platform(self,col,row)
                if tile != '1':
                    number = random.randint(1,80)
                    if number == 4:
                        PowerUp(self, col, row)
                if tile != '1':
                    number = random.randint(1,100)
                    if number == 4:
                        Coin(self, col, row)




    #defining function to draw everything on the screen
    def draw(self):
            keys = pg.key.get_pressed()
            if keys[pg.K_1]:
                HEALTH -= 1
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, "Coins  " + str(self.player.moneybag), 24, WHITE, WIDTH/2 - 32, 2)
            pg.draw.rect(self.screen, LIGHTGREY, pg.Rect(0,0,320,32))
            pg.draw.rect(self.screen, RED, pg.Rect(0,0,self.player.health *32,32))
            #self.draw_text(self.screen,str(HEALTH), 21 + int((HEALTH/3)) , WHITE, HEALTH * 16 - 13, 1 + int((10+HEALTH/12)/HEALTH))
            self.draw_text(self.screen,str(self.player.health), 24, WHITE, self.player.health * 16 - (self.player.health*0.05 * 20),3)
            self.draw_text(self.screen,"Multiplier: " + str(self.player.money_multiplier) + " x", 30, WHITE, 800,0)
            pg.display.flip()
            
    
    # Define a function to quit
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
                
    
                
    #Define a function to create Start screen
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press mouse button to play", 24, WHITE, WIDTH/2 - 230, HEIGHT/2 - 150)
        self.draw_text(self.screen, "For map 1 click 1     For map 2 click 2     For map 3 click 3", 24, WHITE, WIDTH/2 - 250, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

       
    #Define a function to create Start screen
    def wait_for_key(self):
        keys = pg.key.get_pressed()
        waiting = True
        while waiting:
            # if keys[pg.K_1]:
            #     map_choice = 'map.txt'
            #     #g = Game()
            # if keys[pg.K_2]:
            #     map_choice = 'map1.txt'
            #     #g = Game()
            #     print ('You Chose map 2')
            # if keys[pg.K_3]:
            #     map_choice = 'map2.txt'
        
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    waiting = False
                # if event.type == keys[pg.K_1]:
                #     map_choice = 'map.txt'
                #     waiting = False
                # #g = Game()
                # if event.type == keys[pg.K_2]:
                #     map_choice = 'map1.txt'
                #     waiting = False
                #     #g = Game()
                #     print ('You Chose map 2')
                # if event.type == keys[pg.K_3]:
                #     map_choice = 'map2.txt'
                #     waiting = False


# Instantiate the game... 
g = Game()

# use game method run to run
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()
    print (HEALTH)