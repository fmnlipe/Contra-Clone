import pygame as pg
from configuraçoes import *
from pygame.math import Vector2 as vector
from os import walk
from math import sin

class Entidade(pg.sprite.Sprite):
    def __init__(self, pos, path, groups, atirar):
        super().__init__(groups)

        # setup gráfico
        self.importar_imagem(path)
        self.frame_index = 0
        self.status = "right"

        # imagem
        self.imagem = self.animation[self.status][self.frame_index]
        self.rect = self.imagem.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = Camadas['Level']
        self.mask = pg.mask.from_surface(self.imagem)

        self.direction = vector()
        self.pos = vector(self.rect.topleft)
        self.speed = 400

        self.atirar = atirar
        self.can_shoot = True
        self.shoot_time = None
        self.cooldown = 200
        self.duck = False

        self.health = 3

         #invulnerabilidade pós dano
        self.is_vulnerable = True
        self.hit_time = None
        self.invul_duration = 500

        self.hit_sound = pg.mixer.Sound("audio/hit.wav")
        self.hit_sound.set_volume(0.2)
        self.shoot_sound = pg.mixer.Sound("audio/bullet.wav")
        self.shoot_sound.set_volume(0.2)
    
    def blink(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pg.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0,0,0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return True
        else: 
            return False

    def dano(self):
        if self.is_vulnerable:
            self.health -= 1
            self.is_vulnerable = False
            self.hit_time = pg.time.get_ticks()
            self.hit_sound.play()
    
    def check_death(self):
        if self.health <= 0:
            self.kill()
    
    def animar(self, deltatime):
        self.frame_index += 7 * deltatime
        if self.frame_index >= len(self.animation[self.status]):
            self.frame_index = 0
        
        self.image = self.animation[self.status][int(self.frame_index)]
        self.mask = pg.mask.from_surface(self.image)

    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pg.time.get_ticks()
            if current_time - self.shoot_time > self.cooldown:
                self.can_shoot = True
    
    def invul_timer(self):
        if not self.is_vulnerable:
            current_time = pg.time.get_ticks()
            if current_time - self.hit_time > self.invul_duration:
                self.is_vulnerable = True

    def importar_imagem(self, path):
        self.animation = {}
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animation[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda string: int(string.split(".")[0])):
                    path = folder[0].replace("\\", "/") + "/" + file_name
                    surf = pg.image.load(path).convert_alpha()
                    key = folder[0].split("\\")[1]
                    self.animation[key].append(surf)
    
