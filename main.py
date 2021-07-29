import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atire neles!")

# Imagens - aliens
RED_ALIEN = pygame.image.load(os.path.join("assets", "alien-red.png"))
BLUE_ALIEN = pygame.image.load(os.path.join("assets", "alien-blue.png"))
GREEN_ALIEN = pygame.image.load(os.path.join("assets", "alien-green.png"))
RED_ALIEN = pygame.image.load(os.path.join("assets", "alien-red.png"))

# Nave do jogador
YELLOW_SHIP = pygame.image.load(os.path.join("assets", "ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Plano de fundo
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

#Classe abstrata para criar itens (aliens e nave)
class Item:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, window):
        #desenho de um retângulo para teste 
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))


def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    velocidade_jogador = 5

    ship = Item(300,650)

    clock = pygame.time.Clock()

    #Desenho do jogo
    def redraw_window():
        WIN.blit(BG, (0,0))
        #Texto
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        ship.draw(WIN)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        #Fechar o programa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #Ação dos botões
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship.x - velocidade_jogador > 0: #esquerda
            ship.x -= velocidade_jogador
        if keys[pygame.K_RIGHT] and ship.x + velocidade_jogador < WIDTH: #direita
            ship.x += velocidade_jogador
        if keys[pygame.K_UP] and ship.y - velocidade_jogador > 0: #para cima
            ship.y -= velocidade_jogador
        if keys[pygame.K_DOWN] and ship.y + velocidade_jogador <HEIGHT: #para baixo
            ship.y += velocidade_jogador
        
main()