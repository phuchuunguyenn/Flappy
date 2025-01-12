import pygame
import random
import math
import sys
import collections

pygame.init()
pygame.font.init()

# color assign
Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
SC = (102, 153, 153)

# font & screen
mfont = pygame.font.SysFont('Consolas', 30)
bfont = pygame.font.SysFont('Consolas', 50)
screen = pygame.display.set_mode((1000, 700))

# texts
PlayButton = mfont.render("PLAY", True, White)
LoseMenu = mfont.render("LOSE", True, White)
WinMenu = mfont.render("WIN", True, White)

# variable
running = True
menu = True
losed = False
ingame = False
wined = False

BirdY = 350
LefI = 0
RigI = 1000
numBullet = 0
Tunnel = []
bullet = []
hammos = []
Target = 0
Shots = 0
premove = 0

def LoseAd ():
    pygame.draw.rect(screen, Black, (400, 250, 200, 200))
    pygame.draw.rect(screen, White, (400, 250, 200, 200))
    pygame.draw.rect(screen, Black, (405, 255, 190, 190))
    screen.blit(LoseMenu, (465, 335))

def WinAd ():
    pygame.draw.rect(screen, Black, (400, 250, 200, 200))
    pygame.draw.rect(screen, White, (400, 250, 200, 200))
    pygame.draw.rect(screen, Black, (405, 255, 190, 190))
    screen.blit(WinMenu, (475, 335))

def DrawTunnel (height, l, r):
    # l, r, 0, height
    Score = bfont.render(str(Shots), True, SC)
    screen.blit(Score, (450, 300))
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

def OutBullet (l, r):
    global Shots
    if (len(bullet) == 10):
        return
    while (len(bullet) > 0) and (bullet[0] > r):
        del(bullet[0])
        del(hammos[0])
    for i in range(len(bullet)):
        left = max(bullet[i], l)
        right = min(bullet[i] + 40, r)
        pygame.draw.rect(screen, White, (left - l, hammos[i], right - left, 20))
        pygame.draw.rect(screen, Black, (left - l + 5, hammos[i] + 5, right - left - 20, 10))
    i = 0
    while (len(bullet) > 0):
        if (right == r) and ((hammos[i] >= Target and hammos[i] <= Target + 50) or (hammos[i] + 20 >= Target and hammos[i] <= Target + 50)):
            Shots += 1
            del(bullet[0])
            del(hammos[0])
        else:
            break

def OutTarget ():
    global wined, ingame
    if (Shots >= int(10)):
        wined = True
        ingame = False
    pygame.draw.rect(screen, Red, (980, Target, 20, 100))

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
                RD = random.randint(1, 15)
                if (RD == 1):
                    premove = -premove
                    Target += premove
                else:
                    Target += premove
                if (Target > 600):
                    Target = 600
                if (Target < 0):
                    Target = 0
                for i in range(len(bullet)):
                    bullet[i] += 0.7
                BirdY += 0.1
                if BirdY > 700:
                    BirdY = 700
                OutTunnel(LefI, RigI)
                OutBullet(LefI, RigI)
                OutTarget()
                OutBird()
            if wined == True:
                WinAd()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        posx, posy = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if ingame:
                if (event.key == pygame.K_c) and (numBullet > 0):
                    bullet.append(LefI + 100)
                    hammos.append(BirdY)
                    numBullet -= 1
                else:
                    if (event.key == pygame.K_v):
                        numBullet += 1
                        numBullet = min(numBullet, 5)
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
                            numBullet = 0
                            bullet.clear()
                            hammos.clear()
                            Target = random.randint(0, 600)
                            Shots = 0
                            premove = -1
                        if wined == True:
                            wined = False
                            menu = True
                        if losed == True:
                            losed = False
                            menu = True
                    
    pygame.display.flip()