import pygame

class New_obj:
    def __init__(self, jogo):
        #Inicializa a espaçonave e defina a sua posição inicial
        self.screen = jogo.screen
        self.tela_retangulo = jogo.screen.get_rect()
        
        #Sobe a imagem da espaçonave e obtém seu react
        self.image = pygame.image.load('images/alien.bmp')
        self.retangulo = self.image.get_rect()
        
        #Começa cada espaçonave nova no centro inferior da tela
        self.retangulo.midbottom = self.tela_retangulo.midbottom
    def time(self):
        """Desenha a espaçonave em sua localização atual"""
        self.screen.blit(self.image, self.retangulo)