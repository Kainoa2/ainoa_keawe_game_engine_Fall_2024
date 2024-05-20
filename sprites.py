# This file was created by: Keawe Ainoa
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *
import random

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, controls):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 7  # Adjusted speed for smoother movement
        self.health = 10
        self.has_speed = False
        self.has_coin = False
        self.money_multiplier = 1
        self.account = ""
        self.controls = controls
        print("player created at", self.x, self.y)

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[self.controls['up']]:
            self.vy = -self.speed
        if keys[self.controls['down']]:
            self.vy = self.speed
        if keys[self.controls['left']]:
            self.vx = -self.speed
        if keys[self.controls['right']]:
            self.vx = self.speed

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

    def collide_with_disappear_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.disappear_walls, False)
            for hit in hits:
                if not hit.disappeared:
                    if self.vx > 0:
                        self.x = hit.rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hit.rect.right
                    self.vx = 0
                    self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.disappear_walls, False)
            for hit in hits:
                if not hit.disappeared:
                    if self.vy > 0:
                        self.y = hit.rect.top - self.rect.height
                    if self.vy < 0:
                        self.y = hit.rect.bottom
                    self.vy = 0
                    self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.collide_with_disappear_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_disappear_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)

    def collide_with_group(self, group, remove):
        hits = pg.sprite.spritecollide(self, group, remove)
        for hit in hits:
            if isinstance(hit, Coin):
                self.moneybag += 1
            elif isinstance(hit, PowerUp):
                self.speed += 2
                self.has_speed = True

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class DisappearWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.disappear_walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.disappeared = False

    def update(self):
        if pg.sprite.spritecollide(self.game.player, self.game.platforms, False):
            self.disappeared = True
            self.image.set_alpha(0)
        else:
            self.disappeared = False
            self.image.set_alpha(255)

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE // 2, TILESIZE // 2))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x * TILESIZE + TILESIZE // 2, y * TILESIZE + TILESIZE // 2)
        self.value = 1

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE // 2, TILESIZE // 2))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x * TILESIZE + TILESIZE // 2, y * TILESIZE + TILESIZE // 2)
        self.speed_boost = 2

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


    # def update(self):
    #     self.x += self.vx * self.game.dt
    #     self.y += self.vy * self.game.dt

    #     if self.rect.x < self.game.player.rect.x:
    #         self.vx = 100
    #     if self.rect.x > self.game.player.rect.x:
    #         self.vx = -100    
    #     if self.rect.y < self.game.player.rect.y:
    #         self.vy = 100
    #     if self.rect.y > self.game.player.rect.y:
    #         self.vy = -100
    #     self.rect.x = self.x
    #     self.collide_with_walls('x')
    #     self.rect.y = self.y
    #     self.collide_with_walls('y')

    # def update(self):
    #     # self.rect.x += 1
    #     self.x += self.vx * self.game.dt
    #     self.y += self.vy * self.game.dt
        
    #     if self.rect.x < self.game.player.rect.x:
    #         self.vx = 100
    #     if self.rect.x > self.game.player.rect.x:
    #         self.vx = -100    
    #     if self.rect.y < self.game.player.rect.y:
    #         self.vy = 100
    #     if self.rect.y > self.game.player.rect.y:
    #         self.vy = -100
    #     self.rect.x = self.x
    #     self.collide_with_walls('x')
    #     self.rect.y = self.y
    #     self.collide_with_walls('y')

# class Interactable_platform(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.walls
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TIjun76hLESIZE, TILESIZE))
#         self.image.fill(PURPLE)
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE


        