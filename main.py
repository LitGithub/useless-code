import pygame
from Player import *

pygame.init()  
pygame.display.set_caption("easy platformer")  # sets the window title
screen = pygame.display.set_mode((800, 800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop

Player1 = player(400, 200)

#CONSTANTS
LEFT=0
RIGHT=1
UP = 2
DOWN = 3

#animation variables variables
frameWidth = 16 * 2
frameHeight = 16 * 2
RowNum = 0 #for left animation, this will need to change for other animations
frameNum = 0
ticker = 0

Link = pygame.image.load('dude.png') #load your spritesheet
Link.set_colorkey((255, 0, 255)) #this makes bright pink (255, 0, 255) transparent (sort of)

#player variables
xpos = 500 #xpos of player
ypos = 200 #ypos of player
vx = 0 #x velocity of player
vy = 0 #y velocity of player
keys = [False, False, False, False] #this list holds whether each key has been pressed
isOnGround = False #this variable stops gravity from pulling you down more when on a platform

image = pygame.image.load("tree2.png")
image.set_colorkey((255, 255, 255))
jump = pygame.mixer.Sound('jump.wav')
music = pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)
while not gameover: #GAME LOOP############################################################
    clock.tick(60) #FPS
    
    #Input Section------------------------------------------------------------
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
      
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT]=True
            if event.key == pygame.K_RIGHT:
                keys[RIGHT]=True
            elif event.key == pygame.K_UP:
                keys[UP]=True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys[LEFT]=False
            if event.key == pygame.K_RIGHT:
                keys[RIGHT]=False
            elif event.key == pygame.K_UP:
                keys[UP]=False
          
    #physics section--------------------------------------------------------------------
    Player1.keys(keys)
    #LEFT MOVEMENT
    if keys[0]==True:
            vx=-3
            direction = 0
    if keys[1]==True:
        vx=3
        direction = 1
        #turn off velocity\
    if not keys[0] and not keys[1]:
        vx = 0
    if keys[UP] == True and isOnGround == True: #only jump when on the ground
        vy = -8
        isOnGround = False
        direction = UP
        pygame.mixer.Sound.play(jump) 

    Player1.collide()
    #COLLISION
    if xpos>100 and xpos<200 and ypos+40 >750 and ypos+40 <770:
        ypos = 750-40
        isOnGround = True
        vy = 0
    elif xpos>200 and xpos<300 and ypos+40 >650 and ypos+40 <670:
        ypos = 650-40
        isOnGround = True
        vy = 0
    else:
        isOnGround = False


    
    #stop falling if on bottom of game screen
    if ypos > 760:
        isOnGround = True
        vy = 0
        ypos = 760
    
    #gravity
    if isOnGround == False:
        vy+=.2 #notice this grows over time, aka ACCELERATION
    

    #update player position
    xpos+=vx 
    ypos+=vy
    Player1.update()
    
    if vx>0:
        RowNum = 0
    if vx < 0: #left animation
        RowNum = 1
        # Ticker is a spedometer. We don't want Link animating as fast as the
        # processor can process! Update Animation Frame each time ticker goes over
        ticker+=1
        if ticker%10==0: #only change frames every 10 ticks
          frameNum+=1
           #If we are over the number of frames in our sprite, reset to 0.
           #In this particular case, there are 10 frames (0 through 9)
        if frameNum>3: 
           frameNum = 0
  
    # RENDER Section--------------------------------------------------------------------------------
            
    screen.fill((0,0,0)) #wipe screen so it doesn't smear
    Player1.render(screen)
    pygame.draw.rect(screen, (100, 200, 100), (xpos, ypos, 20, 40))
    screen.blit(Link, (xpos, ypos), (frameWidth*frameNum, RowNum*frameHeight, frameWidth, frameHeight))
    #first platform
    pygame.draw.rect(screen, (200, 0, 100), (100, 750, 100, 20))
    
    #second platform
    pygame.draw.rect(screen, (100, 0, 200), (200, 650, 100, 20))
    
    screen.blit(image, (500, 500))
    
    pygame.display.flip()#this actually puts the pixel on the screen
    
#end game loop------------------------------------------------------------------------------
pygame.quit()
