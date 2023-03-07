import pygame as pg
from configuraçoes import *
from pygame.math import Vector2 as vector

class Bala(pg.sprite.Sprite):
    def __init__(self, pos, surf, direction, groups):
        super().__init__(groups)
        self.image = surf
        if direction.x < 0:
            self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = pos)
        self.z = Camadas["Level"]

        self.direction = direction
        self.speed = 1200
        self.pos = vector(self.rect.center)

        self.start_time = pg.time.get_ticks()
        self.mask = pg.mask.from_surface(self.image)
    
    def update(self, deltatime):
        self.pos += self.direction * self.speed * deltatime
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if pg.time.get_ticks() - self.start_time > 1000:
            self.kill()

class FireAnimation(pg.sprite.Sprite):
    def __init__(self, entity, surf_list, direction, groups):
        super().__init__(groups)
        self.entity = entity
        self.frames = surf_list
        if direction.x < 0:
            self.frames = [pg.transform.flip(frame, True, False) for frame in self.frames]

        #image
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        #offset
        x_offset = 60 if direction.x > 0 else -60
        y_offset = 10 if entity.duck else -10
        self.offset = vector(x_offset, y_offset)

       #position 
        self.rect = self.image.get_rect(center = self.entity.rect.center + self.offset)
        self.z = Camadas["Level"]
    
    def animar(self, deltatime):
        self.frame_index += 15 * deltatime
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    
    def movimento(self):
        self.rect.center = self.entity.rect.center + self.offset

    def update(self, deltatime):
        self.animar(deltatime)
        self.movimento()