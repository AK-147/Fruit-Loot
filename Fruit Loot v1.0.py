# Pygame Game - Fruit Loot
# The objective is to get a highscore in this never ending game.
# By Ahmad Khan - ICS3U0


# Importing Essential Libraries
import pygame
import random
import time


# Creating a Surface
pygame.init()

global score

displayLength = 1000
displayWidth = 700

display = pygame.display.set_mode((displayLength,displayWidth))
pygame.display.set_caption("ƒ®µ!τ  L¤¤τ . exe") # ←(Fruit Loot)
clock = pygame.time.Clock()


# Implementing Sprites and Images into Lists
# Character Sprites Found at: https://lionheart963.itch.io/goblin-sprite
movingRight = [pygame.image.load("goblin run r1.png"), pygame.image.load("goblin run r2.png"), pygame.image.load("goblin run r3.png"), pygame.image.load("goblin run r4.png"), pygame.image.load("goblin run r5.png"), pygame.image.load("goblin run r6.png")]
movingLeft = [pygame.image.load("goblin run l1.png"), pygame.image.load("goblin run l2.png"), pygame.image.load("goblin run l3.png"), pygame.image.load("goblin run l4.png"), pygame.image.load("goblin run l5.png"), pygame.image.load("goblin run l6.png")]
idleRight = [pygame.image.load("goblin idle r1.png"), pygame.image.load("goblin idle r2.png"), pygame.image.load("goblin idle r3.png")]
idleLeft = [pygame.image.load("goblin idle l1.png"), pygame.image.load("goblin idle l2.png"), pygame.image.load("goblin idle l3.png")]
# Background Found at: https://edermunizz.itch.io/pixel-art-forest
background = pygame.image.load("forest.jpg")
fruits = [pygame.image.load("f.apple.png"), pygame.image.load("f.bananas.png"), pygame.image.load("f.cherries.png"), pygame.image.load("f.grapes.png"), pygame.image.load("f.pear.png"), pygame.image.load("f.pineapple.png")]
# I created these Pages myself
instructions = [pygame.image.load("Lore P1.png"), pygame.image.load("Lore P2.png"), pygame.image.load("Controls.png"), pygame.image.load("Objective.png")] 


# Defining Variables
length = 125
width = 125
xPlayer = (displayLength / 2) - (length / 2)
yPlayer = displayWidth - width - 3 # So that he is lined up with the ground
speed = 4
boost = False
move = 0
moveRight = False
moveLeft = False
idle = True
inAir = False
jumpHeight = 8
running = True
showingMenu = True
playGame = 1
WHITE = [255,255,255]
CORAL = [240,128,128]
greenishWHITE = [225,247,240]
score = 0


# Adding Background Music
# pygame.mixer.music.load("Fruit Loot Theme.mp3")
# pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
# pygame.mixer.music.play()


# Making Fruit Fall Randomly
fruitDrops = [] # Empty since random coordinates will be appended later
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

    display.blit(background, (0,-20))
    
    # This is the hitbox. Uncomment it if you want to see if the collision works.
    #pygame.draw.rect(display, CORAL, [xPlayer + 40, yPlayer + 40, length - 80, width - 60], 2)

    if move + 1 >= 60:
        move = 0

    # Using Integer Division to have Whole Frames
    if not idle:    
        if moveLeft:  
            display.blit(movingLeft[move//12], (xPlayer,yPlayer))
            move += 1
        elif moveRight:
            display.blit(movingRight[move//12], (xPlayer,yPlayer))
            move += 1
    else:
        if moveLeft:
            display.blit(idleLeft[move//6], (xPlayer,yPlayer))
            move = 0
        else:
            display.blit(idleRight[move//6], (xPlayer,yPlayer))
            move = 0


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
        font = pygame.font.SysFont("VT323", 200, True, False)
        title = font.render("ƒ®µ!τ L¤¤τ", True, CORAL)
        display.blit(title, [75, 200])

        font = pygame.font.SysFont("VT323", 50, True, False)
        play = font.render("Press SPACE to Play", True, WHITE)
        display.blit(play, [300, 450])
        
        pygame.display.flip()
        animateCharacter()
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
        move = 0

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
    font = pygame.font.SysFont("VT323", 35, True, False)
    scoreCounter = font.render("Fruit Collected: " + str(score), True, greenishWHITE)
    display.blit(scoreCounter, [15, 15])

    pygame.display.flip()

    
pygame.quit()
