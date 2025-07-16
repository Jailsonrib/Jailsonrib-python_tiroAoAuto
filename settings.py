class Settings:
    """Classe para armazenar as configurações do jogo Invasão Alienígena"""
    def __init__(self):
        """Inicializa as configurações do jogo"""
        #Configurações da tela
        self.screen_width = 1200
        self.screen_heigth = 800
        self.bg_color = (230,230,230)
        self.ship_speed = 15
        self.ship_limit = 3
        
        #Configurações do projétil
        self.bullet_speed = 10
        self.bullet_width = 3
        self.bullet_height = 5
        self.bullet_color = (60,60,60)
        
        self.bullets_allowed = 3
        
        #Configuração do alienígena
        self.alien_speed = 2
        self.fleet_drop_speed = 10
        
        #Fleet_direction de 1 representa a direita; -1 representa a esquerda
        self.fleet_direction = 1
        #A rapidez com que a velocidade do jogo aumenta
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Inicializa as configurações que mudam no decorrer do jogo"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        
        #fleet_direction de 1 representa a direita; -1 representa a esquerda
        self.fleet_direction = 1
    def increase_speed(self):
        """Aumenta as configurações de velocidade"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale