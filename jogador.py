import pygame as pg, sys
from configuraçoes import *
from pygame.math import Vector2 as vector
from entidade import Entidade

class Jogador(Entidade):
    def __init__(self, pos, groups, path, collision_sprites, atirar): 
        super().__init__(pos, path, groups, atirar)
        #colisão
        self.collision_sprites = collision_sprites

        # vertical
        self.gravity = 15
        self.jump_speed = 1400
        self.on_floor = False
        self.moving_floor = None

        self.health = 10


    def get_status(self):
        #idle
        if self.direction.x == 0 and self.on_floor:
            self.status = self.status.split('_')[0] + "_idle" 

        #jump
        if self.direction.y != 0 and not self.on_floor:
            self.status = self.status.split('_')[0] + "_jump"
        
        if self.on_floor and self.duck:
            self.status = self.status.split('_')[0] + "_duck"

        #duck
    
    def check_contact(self): # corrigir o problema da animação do pulo
        bottom_rect = pg.Rect(0,0,self.rect.width, 5)
        bottom_rect.midtop = self.rect.midbottom
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True
                if hasattr(sprite, "direction"):
                    self.moving_floor = sprite

    def comandos(self):
        key = pg.key.get_pressed()

        if key[pg.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif key[pg.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0

        if key[pg.K_UP] and self.on_floor:
            self.direction.y = -self.jump_speed #o jogador vai mover para cima muito rápido
        
        if key[pg.K_DOWN]:
            self.duck = True
        else:
            self.duck = False

        if key[pg.K_SPACE] and self.can_shoot:
            direction = vector(1,0) if self.status.split("_")[0] == "right" else vector(-1,0)
            pos = self.rect.center + direction * 60
            y_offset = vector(0,-16) if not self.duck else vector(0,10)
            self.atirar(pos + y_offset, direction, self)

            self.can_shoot = False
            self.shoot_time = pg.time.get_ticks()
            self.shoot_sound.play()

        # if key[pg.K_UP]:
        #     self.direction.y = -1
        # elif key[pg.K_DOWN]:
        #     self.direction.y = 1
        # else:
        #     self.direction.y = 0

    def colisao(self, direction):
         for sprite in self.collision_sprites.sprites():
             if sprite.rect.colliderect(self.rect):

                 if direction == "horizontal":
                    # colisão na esquerda
                     if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right: # primeiro, checamos se há colisão e onde ela vai ser. Depois, checamos de que direção ela veio
                        self.rect.left = sprite.rect.right
                    # colisão na direita
                     if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left: 
                        self.rect.right = sprite.rect.left
                     self.pos.x = self.rect.x
                   
                 else:
                    # colisão em baixo
                     if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top: 
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                    # colisão em cima    
                     if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom: 
                        self.rect.top = sprite.rect.bottom
                     self.pos.y = self.rect.y
                     self.direction.y = 0

         if self.on_floor and self.direction.y !=0:
                    self.on_floor = False
    
    def movimento(self, deltatime):
        if self.duck and self.on_floor:
            self.direction.x = 0


        self.pos.x += self.direction.x * self.speed * deltatime
        self.rect.x = round(self.pos.x)
        self.colisao("horizontal")

        # gravity
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * deltatime

        if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0:
            self.direction.y = 0
            self.rect.bottom = self.moving_floor.rect.top
            self.pos.y = self.rect.y
            self.on_floor = True
        
        self.rect.y = round(self.pos.y)
        self.colisao("vertical")
        self.moving_floor = None

    def check_death(self):
        if self.health <= 0:
            pg.quit()
            sys.exit()
    
    def update(self, deltatime):
        self.old_rect = self.rect.copy()
        self.comandos()
        self.get_status()
        self.movimento(deltatime)
        self.check_contact()
        
        self.animar(deltatime)
        self.blink()

        self.shoot_timer()
        self.invul_timer()

        #morte
        self.check_death()