import pygame as pg

class Overlay: #mesma lógica para criar tela de fim de jogo
    def __init__(self, jogador):
        self.jogador = jogador
        self.tela = pg.display.get_surface()
        self.health_surf = pg.image.load("graphics/health.png").convert_alpha()

    def display(self):
        for h in range(self.jogador.health):
            x = 10 + h * (self.health_surf.get_width() * 1.5)
            y = 10
            self.tela.blit(self.health_surf, (x,y))