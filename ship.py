import pygame

class Ship:
    """CLasse para cuidar da espaçonave"""
    def __init__(self, ai_game):
        
        #Inicializa a espaçonave e defina a sua posição inicial
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
       
        #Sobe a imagem da espaçonave e obtém seu react
        self.image = pygame.image.load('images/atirador.png')
        self.rect = self.image.get_rect()
        
        #Flag de movimento; começa com uma espaçonave que não esta se movendo
        self.moving_left = False
        self.moving_rigth = False
        
        #Começa cada espaçonave nova no centro inferior da tela
        self.rect.midbottom = self.screen_rect.midbottom
        
        #Armazena um float para a posição horizontal exata da espaçonave
        self.x = float(self.rect.x)
        
        
    def blitme(self):
        """Desenha a espaçonave em sua localização atual"""
        self.screen.blit(self.image,self.rect)
        
    def update(self):
        
        """Atualiza a posição da espaçonave com base na flag de movimento"""
        if self.moving_rigth and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
        
    def center_ship(self):
        """Centraliza a espaçonave na tela"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)