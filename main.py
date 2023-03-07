import pygame as pg, sys
from configuraçoes import *
from pytmx.util_pygame import load_pygame
from tile import *
from jogador import *
from bullet import *
from enemy import Enemy
from overlay import Overlay
from pygame.math import Vector2 as vector


class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.tela = pg.display.get_surface()
        self.offset = vector()

        # sky
        self.fg_sky = pg.image.load("graphics/sky/fg_sky.png").convert_alpha()
        self.bg_sky = pg.image.load("graphics/sky/bg_sky.png").convert_alpha()
        self.sky_comp = self.bg_sky.get_width()

        self.padding = comprimento_tela/2
        tmx_map = load_pygame("level/mapa_contra.tmx")
        mapa_comp = tmx_map.tilewidth * tmx_map.width + (2*self.padding)
        self.sky_num = int(mapa_comp//self.sky_comp)


    def custom_draw(self, jogador):
        self.offset.x = jogador.rect.centerx - comprimento_tela/2
        self.offset.y = jogador.rect.centery - altura_tela/2


        for x in range(self.sky_num):
            x_pos = -self.padding + (x * self.sky_comp)
            self.tela.blit(self.bg_sky,(x_pos - self.offset.x/2.5, 850 - self.offset.y/2.5))
            self.tela.blit(self.fg_sky,(x_pos - self.offset.x/2, 850 - self.offset.y/2))

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.z ):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.tela.blit(sprite.image, offset_rect)

class Jogo:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode((comprimento_tela, altura_tela))
        pg.display.set_caption("Clone do Contra")
        self.clock = pg.time.Clock()


        self.all_sprites = AllSprites()
        self.collision_sprites = pg.sprite.Group()
        self.platform_sprites = pg.sprite.Group()
        self.bala_sprites = pg.sprite.Group()
        self.vulnerable_sprites = pg.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.jogador)


    #imagem das balas
        self.bala_surf = pg.image.load("graphics/bullet.png").convert_alpha()
        self.fire_surf = [pg.image.load("graphics/fire/0.png").convert_alpha(), pg.image.load("graphics/fire/1.png").convert_alpha()]
    
        #musica
        self.music = pg.mixer.Sound("audio/music.wav")
        self.music.play(loops= -1)

    def setup(self):
        tmx_mapa = load_pygame("level/mapa_contra.tmx")


        # collision tiles
        for x,y, surf in tmx_mapa.get_layer_by_name("Level").tiles():
           CollisionTile((x * 64, y * 64), surf, [self.all_sprites, self.collision_sprites])
        
        # tiles
        for layer in ["Background", "Bg details", "Fg detail top", "Fg detail bottom" ]:
            for x,y, surf in tmx_mapa.get_layer_by_name(layer).tiles():
                Tile((x * 64, y * 64), surf, self.all_sprites, Camadas["Level"])
        
        # objetos
        for obj in tmx_mapa.get_layer_by_name("Personagens"):
            if obj.name == "Player":
                self.jogador = Jogador(pos =(obj.x, obj.y),
                                       groups= [self.all_sprites, self.vulnerable_sprites],
                                        path= "graphics/player",
                                        collision_sprites= self.collision_sprites,
                                        atirar= self.atirar)
            if obj.name == "Enemy":
                Enemy(pos = (obj.x, obj.y),
                      path= "graphics/enemies/standard",
                        groups= [self.all_sprites, self.vulnerable_sprites],
                        atirar= self.atirar,
                        jogador= self.jogador, 
                        collision_sprites = self.collision_sprites)


        # plataformas
        self.platform_border_rects = []
        for obj in tmx_mapa.get_layer_by_name("Plataformas"):
            if obj.name == "Platform":
                MovingPlatform((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.platform_sprites])
            else: # border
                border_rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border_rects.append(border_rect)
    
    def platform_collisions(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0 :
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else:
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1
            
            if platform.rect.colliderect(self.jogador.rect) and self.jogador.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.jogador.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1

    def bala_colisao(self):
        # obstaculos
        for obstacle in self.collision_sprites.sprites():
            pg.sprite.spritecollide(obstacle, self.bala_sprites, True)

        # entidades
        for sprite in self.vulnerable_sprites.sprites():
            if pg.sprite.spritecollide(sprite, self.bala_sprites, True, pg.sprite.collide_mask):
                sprite.dano()        

    def atirar(self, pos, direction, personagem):
        Bala(pos, self.bala_surf, direction, [self.all_sprites, self.bala_sprites])
        FireAnimation(personagem, self.fire_surf, direction, self.all_sprites)

    def play(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            
            deltatime = self.clock.tick()/1000
            self.tela.fill((249,131,103))

            self.platform_collisions()
            self.all_sprites.update(deltatime)
            self.bala_colisao()
            #self.all_sprites.draw(self.tela)
            self.all_sprites.custom_draw(self.jogador)
            self.overlay.display()      

            pg.display.update()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.play()        