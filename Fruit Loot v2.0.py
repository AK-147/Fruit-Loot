# PyGame Arcade Video Game - Fruit Loot
# The objective is to get a highscore in this never ending game.

# Import essential libraries
import pygame
import random
import time

# Create surface
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

# Define custom pages for story and control scheme
instructions = [pygame.image.load("Display Pages\Lore P1.png"), pygame.image.load("Display Pages\Lore P2.png"), pygame.image.load("Display Pages\Controls.png"), pygame.image.load("Display Pages\Objective.png")] 


# Play background music
pygame.mixer.music.load("Fruit Loot Theme.mp3")
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()


# Define player as object
class goblin:

    # Initialize attributes for position and movement
    def __init__(self, x, y, length, width, speed):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.speed = speed
        self.boost = False
        self.move = 0
        self.faceRight = False
        self.faceLeft = False
        self.idle = True
        self.inAir = False
        self.jumpHeight = 8

    # Animate sprites with respect to direction
    def animate(self, display):

        # Show up to a total of thirty sprite images
        if self.move + 1 >= 30:
            self.move = 0

        # User is moving
        if not self.idle:

            # User moves left
            if self.faceLeft:  
                display.blit(movingLeft[self.move//5], (self.x, self.y))
                self.move += 1

            # User moves right
            elif self.faceRight:
                display.blit(movingRight[self.move//5], (self.x, self.y))
                self.move += 1

        # User is idle
        else:

            # User is facing left
            if self.faceLeft:
                display.blit(idleLeft[self.move//10], (self.x, self.y))
                self.move += 1

            # User is facing right
            else:
                display.blit(idleRight[self.move//10], (self.x, self.y))
                self.move += 1


# Define fruit as object
class fruit:

    # Initialize required attributes of fruits 
    def __init__(self, numFruits, fallSpeed):
        self.numFruits = numFruits
        self.fallSpeed = fallSpeed
        self.fruitDrops = []
        self.chosenFruits = []

    # Produce fruits of random variety and position
    def spawn(self):
        
        # Generate random fruit coordinates
        for f in range(self.numFruits):
            xFruit = random.randrange(0, displayLength)
            yFruit = random.randrange(0, displayWidth)
            self.fruitDrops.append([xFruit, yFruit])

        # Randomly pick which fruit to fall
        whichFruit = random.randint(0, self.numFruits - 1)
        self.chosenFruits.append(fruits[whichFruit])

        # Randomize selection
        for i in range(1, self.numFruits - 1):
            whichFruit = random.randint(0, self.numFruits - 1)

            # Ensure chosen fruit are distinct
            while (fruits[whichFruit] in self.chosenFruits):
                whichFruit = random.randint(0, self.numFruits - 1)
            self.chosenFruits.append(fruits[whichFruit])

    # Add free fall and collision physics to fruitss
    def fruitFall(self, fruitInUse):
         for f in range(len(fruitInUse)):

            # Show randomly chosen fruit at random position
            display.blit(fruitInUse[f], self.fruitDrops[f])

            # Free fall speed
            self.fruitDrops[f][1] += self.fallSpeed

            # Make fruit disappear after hitting ground
            if self.fruitDrops[f][1] > displayWidth - 60:
                xFruit = random.randrange(0, displayLength - player.speed - player.length)
                self.fruitDrops[f][0] = xFruit
                yFruit = random.randrange(-25, -5)
                self.fruitDrops[f][1] = yFruit

            # Cause fruit and player objects to collide
            if (self.fruitDrops[f][0] >= player.x + 15) and (self.fruitDrops[f][0] <= player.x + 80):
                if (self.fruitDrops[f][1] >= player.y + 15) and (self.fruitDrops[f][1] <= player.y + 70):
                    xFruit = random.randrange(0, displayLength - player.speed - player.length)
                    self.fruitDrops[f][0] = xFruit
                    yFruit = random.randrange(-25, -5)
                    self.fruitDrops[f][1] = yFruit
                    return True


# Refresh sprites and game background
def updateAnim():

    # Show background image
    display.blit(background, (-110,-20))

    # Animate sprites
    player.animate(display)


# Define metrics for position and movement
length = 125
width = 128
xPlayer = (displayLength / 2) - (length / 2)
yPlayer = displayWidth - width
speed = 4
fallSpeed = 2

# Define variables for menu navigation
running = True
gaming = False
playGame = 1

# Define required colours
WHITE = [255,255,255]
CORAL = [240,128,128]
greenishWHITE = [225,247,240]

# Define global score counter
global score
score = 0

# Instantiate player and fruit objects
player = goblin(xPlayer, yPlayer, length, width, speed)
fruit = fruit(len(fruits), fallSpeed)
fruit.spawn()


# Define fonts for main menu and user interface
titleFont = pygame.font.SysFont("VT323", 200, True, False)
playFont = pygame.font.SysFont("VT323", 50, True, False)
gameFont = pygame.font.SysFont("VT323", 35, True, False)

# Render centered text to display on screen
title = titleFont.render("ƒ®µ!τ L¤¤τ", True, CORAL)
titlePosition = title.get_rect(center = (displayLength/2, 300))
play = playFont.render("Press SPACE to Play", True, WHITE)
playPosition = play.get_rect(center = (displayLength/2, 550))
quitGame = gameFont.render("Press Esc to quit", True, greenishWHITE)


# Main menu misplay loop
while running and not gaming:

    # Update frames
    clock.tick(60)

    # Check for program termination
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Ensure background music replays
        if event.type == pygame.constants.USEREVENT:
            pygame.mixer.music.load("Fruit Loot Theme.mp3")
            pygame.mixer.music.play()

        # Allow user to navigate menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playGame += 1

    # User is on the home screen
    if playGame == 1:
        updateAnim()
        display.blit(title, titlePosition)
        display.blit(play, playPosition)
        fruit.fruitFall(fruit.chosenFruits)

    # User in on the first page of the storyline
    if playGame == 2:
        display.blit(instructions[0], [0,0])

    # User in on the second page of the storyline
    if playGame == 3:
        display.blit(instructions[1], [0,0])

    # User in on the control scheme display
    if playGame == 4:
        display.blit(instructions[2], [0,0])

    # User in on the objective display
    if playGame == 5:
        display.blit(instructions[3], [0,0])

    pygame.display.flip()
    
    # Check for final menu page
    if playGame == 6:

        gaming = True
        
        # Gameplay loop
        while running and gaming:

            # Update frames
            clock.tick(60)

            # Check for program termination
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gaming = False
                    running = False

                # Allow user to quit to main menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:

                        # Reset player position and game values
                        player.x = (displayLength / 2) - (length / 2)
                        player.y = displayWidth - width
                        score = 0
                        playGame = 1
                        gaming = False
                        
                # Ensure background music replays
                elif event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.load("Fruit Loot Theme.mp3")
                    pygame.mixer.music.play()

            # Define event of a key press
            keys = pygame.key.get_pressed()

            # Player presses A key and moves left
            if (keys[pygame.K_a] == True) and player.x > player.speed - 40:
                player.x -= speed
                player.faceRight = False
                player.faceLeft = True
                player.idle = False

            # Player presses D key and moves right
            elif (keys[pygame.K_d] == True) and player.x < displayLength - player.speed - player.length + 40:
                player.x += speed
                player.faceRight = True
                player.faceLeft = False
                player.idle = False

            # Player is idle
            else:
                player.idle = True


            # Add jump physics to player object
            if not player.inAir:
                
                # Enable jumping from ground level with W key
                if keys[pygame.K_w]:
                    player.inAir = True
                    player.faceRight = False
                    player.faceLeft = False
                    player.move = 0

            # Player is midair
            else:

                # Player has jumped
                if player.jumpHeight >= -8:
                    comeDown = 1
                    if player.jumpHeight < 0:
                        comeDown = -1
                    player.y -= (player.jumpHeight ** 2) * 0.5 * comeDown
                    player.jumpHeight -= 1
                    time.sleep(0.01)

                # Player has landed
                else:
                    player.inAir = False
                    player.jumpHeight = 8
                    time.sleep(0.1)
                    # This delay makes it look likes the game lags after every jump

            # Update animation according to player movement
            updateAnim()

            # Increase score when fruit is caught
            if fruit.fruitFall(fruit.chosenFruits):
                score += 1

            # Add score tracking system and quitting option on display
            scoreCounter = gameFont.render("Fruit Collected: " + str(score), True, greenishWHITE)
            display.blit(scoreCounter, [15, 15])
            display.blit(quitGame, [displayLength - quitGame.get_width() - 25, 15])
            pygame.display.flip()


# Terminate game window
pygame.quit()
