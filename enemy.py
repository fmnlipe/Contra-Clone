import pygame as pg
from configuraçoes import *
from pygame.math import Vector2 as vector
from entidade import Entidade

class Enemy(Entidade):
    def __init__(self, pos, path, groups, atirar, jogador, collision_sprites):
        super().__init__(pos, path, groups, atirar)
        self.jogador = jogador
        for sprite in collision_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top

        self.cooldown = 1000

        self.health = 4
    
    def get_status(self):
        if self.jogador.rect.centerx < self.rect.centerx:
            self.status = "left"
        else: 
            self.status = "right"

    def check_fire(self):
        enemy_pos = vector(self.rect.center)
        jogador_pos = vector(self.jogador.rect.center)

        distance = (jogador_pos - enemy_pos).magnitude()
        same_y =True if self.rect.top - 20 < jogador_pos.y < self.rect.bottom + 20 else False

        if distance < 600 and same_y and self.can_shoot:
            bala_direction = vector(1, 0) if self.status == "right" else vector (-1, 0)
            y_offset = vector(0,-16)
            pos = self.rect.center + bala_direction * 80           
            self.atirar(pos + y_offset, bala_direction, self)

            self.can_shoot = False
            self.shoot_time = pg.time.get_ticks()
            self.shoot_sound.play()
    
    def update(self,deltatime):
        self.get_status()
        self.animar(deltatime)
        self.blink()
        self.shoot_timer()
        self.invul_timer()
        self.check_fire()

        #morte
        self.check_death()