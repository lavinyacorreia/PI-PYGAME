 
import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Invasão ao planeta PI")

# Imagens - aliens
RED_ALIEN = pygame.image.load(os.path.join("assets", "alien-red.png"))
BLUE_ALIEN = pygame.image.load(os.path.join("assets", "alien-blue.png"))
GREEN_ALIEN = pygame.image.load(os.path.join("assets", "alien-green.png"))

# Nave do jogador
YELLOW_SHIP = pygame.image.load(os.path.join("assets", "yellow_ship.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Plano de fundo
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


#Botão inicial
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,WIN,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(WIN, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(WIN, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            WIN.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

#Classe abstrata para criar itens (aliens e nave)
class Item:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.fora_janela(HEIGHT):
                self.lasers.remove(laser)
            elif laser.colisao(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    #Obter largura e altura do item
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def atirar(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


#Player - Herdando a classe Item
class Player(Item):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health=health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.fora_janela(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.colisao(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    #Barra de vida da nave espacial
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Alien(Item):

    #dicionário de cores
    COLOR_ALIEN = {
        "red": (RED_ALIEN, RED_LASER),
        "green": (GREEN_ALIEN, GREEN_LASER),
        "blue": (BLUE_ALIEN, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_ALIEN[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel
    
    def atirar(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-25, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    #Retorna se o laser saiu da janela do jogo
    def fora_janela(self, height):
        return not(self.y < height and self.y >= 0)

    def colisao(self, obj):
        return colidir(self, obj)


#Colisão dos objetos de acordo com os pixels preenchidos das imagens
def colidir(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    perdeu_font = pygame.font.SysFont("serif", 25)

    velocidade_jogador = 6
    perdeu = False
    perdeu_conta = 0

    laser_vel =5
    #aliens
    inimigos = []
    onda_inimigos = 5
    velocidade_inimigo = 2

    player = Player(300, 575)

    clock = pygame.time.Clock()

    #Desenho do jogo
    def redraw_window():
        WIN.blit(BG, (0,0))
        #Texto
        lives_label = main_font.render(f"Invasões: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for inimigo in inimigos:
            inimigo.draw(WIN)

        player.draw(WIN)

        if perdeu:
            perdeu_label2 = main_font.render("VOCÊ PERDEU!", 1, (255,255,255))
            WIN.blit(perdeu_label2, (WIDTH/2 - perdeu_label2.get_width()/2, 300))
            
            perdeu_label = perdeu_font.render("- Sempre foi mais fácil destruir do que criar.", 1, (255,255,255))
            WIN.blit(perdeu_label, (WIDTH/2 - perdeu_label.get_width()/2, 350))
            

        pygame.display.update()
   
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            perdeu = True
            perdeu_conta += 1
        
        #Fechar o jogo após perda e contagem de 3 segundos
        if perdeu:
            if perdeu_conta > FPS * 3:
                run = False
            else:
                continue
       
        if len(inimigos) == 0:
            level += 1
            onda_inimigos += 5
            #Todos os aliens com mesma velocidade, porém com posições iniciais diferentes
            for i in range(onda_inimigos):
                # __init__(self, x, y, color, health=100):
                inimigo = Alien(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                inimigos.append(inimigo)


        #Fechar o programa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
        #Ação dos botões
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - velocidade_jogador > 0: #esquerda
            player.x -= velocidade_jogador
        if keys[pygame.K_RIGHT] and player.x + velocidade_jogador +  player.get_width() < WIDTH: #direita
            player.x += velocidade_jogador
        if keys[pygame.K_UP] and player.y - velocidade_jogador > 0: #para cima
            player.y -= velocidade_jogador
        if keys[pygame.K_DOWN] and player.y + velocidade_jogador + player.get_height() + 15<HEIGHT: #para baixo
            player.y += velocidade_jogador
        if keys[pygame.K_SPACE]: #atirar
            player.atirar()

        for inimigo in inimigos:
            inimigo.move(velocidade_inimigo)
            inimigo.move_lasers(laser_vel, player)
            #Alien atira na nave
            if random.randrange(0, 4*60) == 1:
                inimigo.atirar()

            if colidir(inimigo, player):
                player.health -= 10
                inimigos.remove(inimigo)

            #se o alien estiver fora da tela - remover
            if inimigo.y + inimigo.get_height() > HEIGHT:
                lives -=1
                inimigos.remove(inimigo)

        player.move_lasers(-laser_vel, inimigos)

def main_menu():
    run = True
    BotaoVerde = button((0,255,0), 275, 480, 150, 100, 'PLAY')
    title_font = pygame.font.SysFont("comicsans", 35)
    title_font2 = pygame.font.SysFont("serif", 35)
    while run:
        WIN.blit(BG, (0,0))

        title_label = title_font.render("REGRAS DO JOGO", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 100))

        title_label2 = title_font.render("1.ATIRE NELES! Pressione a barra de espaço.", 1, (255,255,255))
        WIN.blit(title_label2, (WIDTH/2 - title_label2.get_width()/2, 150))

        title_label3 = title_font.render("2.MOVA-SE! Utilize as setas de direção.", 1, (255,255,255))
        WIN.blit(title_label3, (WIDTH/2 - title_label3.get_width()/2, 200))

        title_label4 = title_font.render("3.CUIDADO! Laser causa dano na espacionave.", 1, (255,255,255))
        WIN.blit(title_label4, (WIDTH/2 - title_label4.get_width()/2, 250))

        title_label5 = title_font.render("4.ATENÇÃO! Limite de invasões: 5 aliens.", 1, (255,255,255))
        WIN.blit(title_label5, (WIDTH/2 - title_label5.get_width()/2, 300))

        title_label6 = title_font.render("5.PERDEU! Invasões ou barra de vida zerados.", 1, (255,255,255))
        WIN.blit(title_label6, (WIDTH/2 - title_label6.get_width()/2, 350))

        title_label6 = title_font.render("6.PRÓXIMO NÍVEL! O número de aliens aumenta.", 1, (255,255,255))
        WIN.blit(title_label6, (WIDTH/2 - title_label6.get_width()/2, 400))

        title_label7 = title_font2.render("- Vida longa e próspera.", 1, (255,255,255))
        WIN.blit(title_label7, (WIDTH/1.5 - title_label7.get_width()/2, 640))

        BotaoVerde.draw(WIN, (0,0,0))
        pygame.display.update() 

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if BotaoVerde.isOver(pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()
            if event.type == pygame.MOUSEMOTION:
                if BotaoVerde.isOver(pos):
                    BotaoVerde.color = (0,187,45)
                else:
                    BotaoVerde.color = (0,0,255)
    pygame.quit()

main_menu()