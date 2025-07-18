import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from aguia import Alien
class AlienInvasion:
    """Classe geral para gerenciar ativos e comportamentos"""
    def __init__(self):
        """Inicializa o jogo e crie recursos do jogo"""
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_heigth = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        #Cria uma instância para armazenar estatísticas do jogo
        self.stats = GameStats(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #Inicializa Invasão Alienígena no modo inativo
        self.game_active = False
        #Cria o botão Play
        self.play_button = Button(self, "Play")
        
    def _create_fleet(self):
        """Cria a frota de alienígenas"""
        #Cria um alienígena e continuar adicionando alienígenas
        #até que não haja mais espaço
        #O distanciamento entre alienígenas é a largura de um alienígena
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y  = alien_width, alien_height
        while current_y < (self.settings.screen_heigth - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            #Termina uma fileira; redefine o valor de x, e incrementa o valor de y
            current_x = alien_width
            current_y += 2 * alien_height
    def _create_alien(self,x_position, y_position):        
            new_alien = Alien(self)
            new_alien.x = x_position
            new_alien.rect.x = x_position
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)
            
    def _check_fleet_edges(self):
        """Responde apropriadamente se algum alienígena alcaçou uma borda"""    
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Faz toda a frota descer e mudar de direção"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def run_game(self):
        """inicia o loop principal do jogo"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()      
            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self):
            """Responde as teclas pressionadas e a eventos de mouse"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)   
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
    def _check_play_button(self, mouse_pos):
        """Inicia um jogo novo quando o jogador clicar em Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #Redefine as configurações do jogo
            self.settings.initialize_dynamic_settings()
            #Redefine as estatísticas do jogo
            self.stats.reset_stats()
            self.game_active = True
            #Descarta quaisquer projéteis restantes e alienígenas
            self.aliens.empty()
            self.bullets.empty()
            #Cria uma nova frota e centraliza a nave
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)                        
    def _check_keydown_events(self, event):
        """Responde a teclas pressionadas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_rigth = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
                            
    def _fire_bullet(self):
        """Cria um novo projétil e o adiciona ao grupo projéteis"""
        if len(self.bullets ) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_aliens(self):
        """Verifica se a frota está na borda e, em seguida, atualiza as posições"""
        self._check_fleet_edges()
        self.aliens.update()
        #Detecta coliões entre alienígenas e a nave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #Procura por alienígenas que atingiram a parte inferior da tela
        self._check_alien_bottom()
    def _ship_hit(self):
            """Responde ao fato de a nave ter sido atingida por um alienígena"""
            #Decrementa ships_left
            if self.stats.ships_left > 0:
                self.stats.ships_left -= 1
                
                #Limpa a tela de alienígenas e projéteis restantes
                self.aliens.empty()
                self.bullets.empty()
                
                #Cria uma nova frota e centraliza a nave
                self._create_fleet()
                self.ship.center_ship()
                
                #Faz uma pausa
                sleep(0.5)
            else:
                self.stats.game_active = False
            
        
    def _check_keyup_events(self, event):
        """Responde a teclas soltas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_rigth = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
             
    def _update_bullets(self):
        """Atualiza a posição dos projetéis e descarta os projetéis antigos"""
        #Atualiza as posições dos projetéis
        self.bullets.update()
        #Descarta os projetéis que desapareceram
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        self._check_bullet_collisions()
                
    def _check_bullet_collisions(self):            
        """Responde à colisões alienígenas"""
        """Remove todos os projetéis e os alienígenas que tenham colidido"""
        collisions = pygame.sprite.groupcollide(self.bullets,
                self.aliens, False, True)
        if not self.aliens:
            #Destrói os projetéis esxistentes e crias uma frota nava
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()    
    def _update_screen(self):                    
        """Atualiza as imagens na tela e mude para a nova tela"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()   
        self.ship.blitme()
        self.aliens.draw(self.screen)
        #Desenha o botão se o jogo estiver inativo
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
    def _check_alien_bottom(self):
        """Verifica se algum alienígena alcançou a parte inferior da tela"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break    
        
        
            
if __name__ == '__main__':
    #Cria uma instância do jogo e execute o jogo
    qualquer = AlienInvasion()
    qualquer.run_game() 
    

                
                      