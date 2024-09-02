import pygame
import random
import math
from pygame import mixer
# inicia um jogo
pygame.init()
# cria o a tela  800 é o eixo x e 600 o eixo y
tela = pygame.display.set_mode((800, 600))

# titulo
pygame.display.set_caption("Space Invaders!")
# icone
icon = pygame.image.load("space-ship (1).png")
pygame.display.set_icon(icon)
# background
background = pygame.image.load("Prancheta 1.png")

#musica
mixer.music.load("universe_on_fire.wav")
mixer.music.play(-1)
# imagem do jogador
jogador_imagem = pygame.image.load("spaceship.png")
# definindo os eixos que a imagem irá aparecer
eixox = 370
eixoy = 450
variacao = 0

inimigo_imagem = []
inimigox = []
inimigoy = []
variacao_inimigox = []
variacao_inimigoy = []
num = 6
for i in range(num):
    inimigo_imagem.append(pygame.image.load("alien.png"))
    inimigox.append(random.randint(0, 735))
    inimigoy.append(random.randint(50, 150))
    variacao_inimigox.append(2)
    variacao_inimigoy.append(30)

# bala
bala_imagem = pygame.image.load("bullet.png")
balax = 0
balay = 430
variacao_balax = 0
variacao_balay = 4
bala_iniciar = "ready"

score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textox = 10
textoy = 10

over_font =  pygame.font.Font("freesansbold.ttf", 128)

def pontuação(x, y):
    pontos = font.render("Pontuação: " + str(score), True, (255, 255, 255))
    tela.blit(pontos, (x, y))

def game_over():
    over = font.render(" GAME OVER ", True, (0,0,0))
    tela.blit(over,  (200, 250))


def atirar(x, y):
    global bala_iniciar
    bala_iniciar = "atirando"
    tela.blit(bala_imagem, (x + 16, y + 10))


def jogador(x, y):
    # define a imagem e seus eixos
    tela.blit(jogador_imagem, (x, y))


def inimigo(x, y, i):
    tela.blit(inimigo_imagem[i], (x, y))


def colisao(balax, balay, inimigox, inimigoy):
    distancia = math.sqrt((math.pow(inimigox - balax, 2)) + (math.pow(inimigoy - balay, 2)))
    if distancia < 27:
        return True


# game loop
running = True
while running:
    # Red, Green, Blue cores em respectivas posições que vao ate 255.A tela deve ser colorida antes para não sobescrever as outras imagens
    tela.fill((0, 30, 30))
    tela.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                variacao = - 5
            if event.key == pygame.K_RIGHT:
                variacao = 5
            if event.key == pygame.K_SPACE:
                if bala_iniciar == "ready":
                    balax = eixox
                    atirar(balax, balay)
                    tiro_som = mixer.Sound("laser.wav")
                    tiro_som.play()
        if event.type == pygame.KEYUP:
            variacao = 0
        # verifica o evento de uma tecla ser pressionada ou não, depois verifica se sao as setas. caso sim, move a nave
        if event.type == pygame.QUIT:
            running = False
    eixox += variacao
    if eixox <= 0:
        eixox = 0
    if eixox >= 734:
        eixox = 734
    for i in range(num):
        if inimigoy[i] > 430:
            for a in range(num):
                inimigox[a] = 2000
                game_over()
        inimigox[i] += variacao_inimigox[i]
        if inimigox[i] <= 0:
            variacao_inimigox[i] = 2
            inimigoy[i] += variacao_inimigoy[i]

        if inimigox[i] >= 734:
            variacao_inimigox[i] = -2
            inimigoy[i] += variacao_inimigoy[i]

        colidiu = colisao(balax, balay, inimigox[i], inimigoy[i])
        if colidiu:
            explosao = mixer.Sound("explosion.wav")
            explosao.play()
            balay = 430
            bala_iniciar = "ready"
            score += 1
            inimigox[i] = random.randint(0, 735)
            inimigoy[i] = random.randint(50, 150)
        inimigo(inimigox[i], inimigoy[i], i)
    if balay <= 0:
        balay = 430
        bala_iniciar = "ready"

    if bala_iniciar == "atirando":
        atirar(balax, balay)
        balay -= variacao_balay

    jogador(eixox, eixoy)

    pontuação(textox, textoy)

    # é necessário dar uptade
    pygame.display.update()
