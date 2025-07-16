import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        #self.settings = Settings()
        # Cria um bullet rect em (0,0) e, em seguida, define a posição correta
        self.rect = pygame.Rect(0,0, self.settings.bullet_width,self.settings.bullet_height)
        
        
        self.rect.midbottom = ai_game.ship.rect.midtop
        
        #Armazena a posição do projetil como um float
        self.y = float(self.rect.y)
    def update(self):
        """Desloca o projétil verticalmente pela tela"""
        #Atualiza a posição exata do projétil
        self.y -= self.settings.bullet_speed
        #Atualiza a posição do rect
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Desenha o projétil na tela"""
        pygame.draw.rect(self.screen, self.color, self.rect)
        
    