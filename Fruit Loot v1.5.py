# PyGame Game - Fruit Loot
# The objective is to get a highscore in this never ending game.

# Import essential libraries
import pygame
import random
import time

# Create a surface
pygame.init()

# Set up initial display
displayLength = 1000
displayWidth = 700
display = pygame.display.set_mode((displayLength,displayWidth))
pygame.display.set_caption("ƒ®µ!τ  L¤¤τ . exe") # ←(Fruit Loot)
clock = pygame.time.Clock()

# Define sprite lists for each player direction found at:
# https://lionheart963.itch.io/goblin-sprite
movingRight = [pygame.image.load("Character Sprites\goblin run r1.png"), pygame.image.load("Character Sprites\goblin run r2.png"), pygame.image.load("Character Sprites\goblin run r3.png"), pygame.image.load("Character Sprites\goblin run r4.png"), pygame.image.load("Character Sprites\goblin run r5.png"), pygame.image.load("Character Sprites\goblin run r6.png")]
movingLeft = [pygame.image.load("Character Sprites\goblin run l1.png"), pygame.image.load("Character Sprites\goblin run l2.png"), pygame.image.load("Character Sprites\goblin run l3.png"), pygame.image.load("Character Sprites\goblin run l4.png"), pygame.image.load("Character Sprites\goblin run l5.png"), pygame.image.load("Character Sprites\goblin run l6.png")]
idleRight = [pygame.image.load("Character Sprites\goblin idle r1.png"), pygame.image.load("Character Sprites\goblin idle r2.png"), pygame.image.load("Character Sprites\goblin idle r3.png")]
idleLeft = [pygame.image.load("Character Sprites\goblin idle l1.png"), pygame.image.load("Character Sprites\goblin idle l2.png"), pygame.image.load("Character Sprites\goblin idle l3.png")]

# Define game background found at:
# https://edermunizz.itch.io/pixel-art-forest
background = pygame.image.load("Display Pages\\forest.jpg")

# Define list of fruit objects found from multiple sources
fruits = [pygame.image.load("Fruit Sprites\\f.apple.png"), pygame.image.load("Fruit Sprites\\f.bananas.png"), pygame.image.load("Fruit Sprites\\f.cherries.png"), pygame.image.load("Fruit Sprites\\f.grapes.png"), pygame.image.load("Fruit Sprites\\f.pear.png"), pygame.image.load("Fruit Sprites\\f.pineapple.png")]

# Custom pages for story and control scheme
instructions = [pygame.image.load("Display Pages\Lore P1.png"), pygame.image.load("Display Pages\Lore P2.png"), pygame.image.load("Display Pages\Controls.png"), pygame.image.load("Display Pages\Objective.png")] 


# Define metrics for position and movement
length = 125
width = 128
xPlayer = (displayLength / 2) - (length / 2)
yPlayer = displayWidth - width
speed = 4
boost = False
move = 0
moveRight = False
moveLeft = False
idle = True
inAir = False
jumpHeight = 8
running = True

# Define variables for menu navigation
showingMenu = True
playGame = 1

# Define required colours
WHITE = [255,255,255]
CORAL = [240,128,128]
greenishWHITE = [225,247,240]

# Define global score counter
global score
score = 0


# Add background music
pygame.mixer.music.load("Fruit Loot Theme.mp3")
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()


# Generate random fruit coordinates
fruitDrops = []
for f in range(6):
    xFruit = random.randrange(0,displayLength)
    yFruit = random.randrange(0,displayWidth)
    fruitDrops.append([xFruit,yFruit])

# This list of four fruits will be the ones that are falling
chosenFruits = [] # Empty since random images will be appended later
whichFruit = random.randint(0,5)
chosenFruits.append(fruits[whichFruit])
for i in range(1,5):
    whichFruit = random.randint(0,5)
    # Making sure that each of fruits chosen for list (theFruits) are different
    while (fruits[whichFruit] in chosenFruits):
        whichFruit = random.randint(0,5)
    chosenFruits.append(fruits[whichFruit])


# Function for Animating Character
def animateCharacter():
    global move

    display.blit(background, (-110,-20))
    
    # This is the hitbox. Uncomment it if you want to see if the collision works.
    #pygame.draw.rect(display, CORAL, [xPlayer + 40, yPlayer + 40, length - 80, width - 60], 2)

    if move + 1 >= 30:
            move = 0

    # Using Integer Division to have Whole Frames
    if not idle:
        
        if moveLeft:  
            display.blit(movingLeft[move//5], (xPlayer,yPlayer))
            move += 1
        elif moveRight:
            display.blit(movingRight[move//5], (xPlayer,yPlayer))
            move += 1
    else:
        
        if moveLeft:
            display.blit(idleLeft[move//10], (xPlayer,yPlayer))
            move += 1
        else:
            display.blit(idleRight[move//10], (xPlayer,yPlayer))
            move += 1


# Function for Fruit Fall Physics
def fruitFall(fruitInUse):
     for f in range(len(fruitInUse)):
        
        display.blit(fruitInUse[f], fruitDrops[f])
        # Falling Speed of Fruit
        fruitDrops[f][1] += 2

        # Making Fruits disappear after hitting ground
        if fruitDrops[f][1] > displayWidth - 60:
            xFruit = random.randrange(0,displayLength - speed - length)
            fruitDrops[f][0] = xFruit
            yFruit = random.randrange(-25,-5)
            fruitDrops[f][1] = yFruit

        # Making Player Catch Fruits
        if (fruitDrops[f][0] >= xPlayer + 15) and (fruitDrops[f][0] <= xPlayer + 80):
            if (fruitDrops[f][1] >= yPlayer + 15) and (fruitDrops[f][1] <= yPlayer + 70):
                xFruit = random.randrange(0,displayLength - speed - length)
                fruitDrops[f][0] = xFruit
                yFruit = random.randrange(-25,-5)
                fruitDrops[f][1] = yFruit
                return True
                # fruitDrops[f][0] is the random x-coordinate
                # fruitDrops[f][1] is the random y-coordinate


# Define fonts for main menu and user interface
titleFont = pygame.font.SysFont("VT323", 200, True, False)
playFont = pygame.font.SysFont("VT323", 50, True, False)
scoreFont = pygame.font.SysFont("VT323", 35, True, False)

# Render centered text to display on screen
title = titleFont.render("ƒ®µ!τ L¤¤τ", True, CORAL)
titlePosition = title.get_rect(center = (displayLength/2, 300))
play = playFont.render("Press SPACE to Play", True, WHITE)
playPosition = play.get_rect(center = (displayLength/2, 550))


# Main Menu Display Loop
while running and showingMenu:
    clock.tick(60)

    # Allowing User to Exit Program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Making Sure Music keeps Replaying
        if event.type == pygame.constants.USEREVENT:
            pygame.mixer.music.load("Fruit Loot Theme.mp3")
            pygame.mixer.music.play()
            
        # Letting User Proceed after Main Menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playGame += 1
                if playGame == 6:
                    showingMenu = False


    # This is the Home Screen
    if playGame == 1:
        animateCharacter()
        display.blit(title, titlePosition)
        display.blit(play, playPosition)
        fruitFall(chosenFruits)

    # This is Page One of the Storyline
    if playGame == 2:
        display.blit(instructions[0], [0,0])

    # This is Page Two of the Storyline
    if playGame == 3:
        display.blit(instructions[1], [0,0])

    # This is the Controls Display
    if playGame == 4:
        display.blit(instructions[2], [0,0])

    # This is the Objective Display
    if playGame == 5:
        display.blit(instructions[3], [0,0])

    pygame.display.flip()
    

# Gameplay Loop
while running and not showingMenu:
    clock.tick(60)

    # Allowing User to Exit Program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Making Sure Music keeps Replaying
        elif event.type == pygame.constants.USEREVENT:
            pygame.mixer.music.load("Fruit Loot Theme.mp3")
            pygame.mixer.music.play()

    
    # Assigning Character Controls
    keys = pygame.key.get_pressed()

    if (keys[pygame.K_a] == True) and xPlayer > speed - 40:
        xPlayer -= speed
        moveRight = False
        moveLeft = True
        idle = False

    elif (keys[pygame.K_d] == True) and xPlayer < displayLength - speed - length + 40:
        xPlayer += speed
        moveRight = True
        moveLeft = False
        idle = False

    else:
        idle = True

    # Jump Animation and Physics
    if not inAir:
        if keys[pygame.K_w]:
            inAir = True
            moveRight = False
            moveLeft = False
            move = 0
    else:
        if jumpHeight >= -8:
            comeDown = 1
            if jumpHeight < 0:
                comeDown = -1
            yPlayer -= (jumpHeight ** 2) * 0.5 * comeDown
            jumpHeight -= 1
            time.sleep(0.01)
        else:
            inAir = False
            jumpHeight = 8
            time.sleep(0.1)
            # This delay makes it look likes the game lags after every jump


    # Calling Functions and Redrawing Display
    animateCharacter()
    fruitCaught = fruitFall(chosenFruits)
    
    if fruitCaught:
        score += 1

    # Adding a Scoring System
    scoreCounter = scoreFont.render("Fruit Collected: " + str(score), True, greenishWHITE)
    display.blit(scoreCounter, [15, 15])

    pygame.display.flip()

    
pygame.quit()
