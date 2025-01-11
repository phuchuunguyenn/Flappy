import pygame
import random
import math
import sys

pygame.init()
pygame.font.init()

# color assign
Black = (0, 0, 0)
White = (255, 255, 255)

# font & screen
mfont = pygame.font.SysFont('Consolas', 30)
screen = pygame.display.set_mode((1000, 700))

# texts
PlayButton = mfont.render("PLAY", True, White)
LoseMenu = mfont.render("LOSE", True, White)

# variable
running = True
menu = True
losed = False
ingame = False

BirdY = 350
LefI = 0
RigI = 1000
Tunnel = []

def LoseAd ():
    pygame.draw.rect(screen, Black, (400, 250, 200, 200))
    pygame.draw.rect(screen, White, (400, 250, 200, 200))
    pygame.draw.rect(screen, Black, (405, 255, 190, 190))
    screen.blit(LoseMenu, (465, 335))

def DrawTunnel (height, l, r):
    # l, r, 0, height
    global ingame, losed
    pygame.draw.rect(screen, White, (l, 0, r - l, height))
    pygame.draw.rect(screen, Black, (l + 5, 0, r - l - 10, height - 5))
    if (BirdY <= height) and ((100 <= l and l <= 150) or (100 <= r and r <= 150)):
        ingame = False
        losed = True
    # l, r, height + 150, 70
    pygame.draw.rect(screen, White, (l, height + 150, r - l, 550 - height))
    pygame.draw.rect(screen, Black, (l + 5, height + 155, r - l - 10, 550 - height))
    if (BirdY >= height + 100) and ((100 <= l and l <= 150) or (100 <= r and r <= 150)):
        ingame = False
        losed = True

def OutTunnel (l, r):
    screen.fill(Black)
    for i in range(100):
        left = max((i + 1) * 300, l)
        right = min((i + 1) * 300 + 50, r)
        if (left <= right) and (right - left <= 50):
            DrawTunnel(Tunnel[i], left - l, right - l)

def OutBird ():
    pygame.draw.rect(screen, White, (100, BirdY, 50, 50))
    pygame.draw.rect(screen, White, (105, BirdY + 5, 40, 40))


Tunnel.append(275)
for i in range(100):
    j = Tunnel[len(Tunnel) - 1]
    Tunnel.append(random.randint(max(1, j - 275), min(j + 275, 550)))

while running == True:
    if losed == True:
        LoseAd()
    else: 
        if menu == True:
            screen.fill(Black)
            pygame.draw.rect(screen, White, (400, 250, 200, 200))
            pygame.draw.rect(screen, Black, (405, 255, 190, 190))
            screen.blit(PlayButton, (465, 335))
        else: 
            if ingame == True:
                LefI += 0.2
                RigI += 0.2
                BirdY += 0.1
                if BirdY > 700:
                    BirdY = 700
                OutTunnel(LefI, RigI)
                OutBird()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        posx, posy = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ingame == True:
                    if posy < BirdY + 50:
                        BirdY -= 50
                    else:
                        BirdY += 50
                    if (BirdY < 0):
                        BirdY = 0
                    if (BirdY > 700):
                        BirdY = 700
                else:
                    if (posx >= 400) & (posx <= 600) & (posy >= 250) & (posy <= 450):
                        if menu == True:
                            menu = False
                            ingame = True
                            BirdY = 350
                            LefI = 0
                            RigI = 1000
                        if losed == True:
                            losed = False
                            menu = True
                    
    pygame.display.flip()