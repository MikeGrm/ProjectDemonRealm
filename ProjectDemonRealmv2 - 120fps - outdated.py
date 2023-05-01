"""
Name: Michael Grimm
File: ProjectDemonRealmv2

Comments:

Although this is not a static skeleton of my project, it is the basis of my game that is codenamed Project Demon Realm which is based off of the popular show YuYu Hakusho.
I have created classes for the different characters and objects included in my game with the main ones being myHero and Enemy.
The functions included are used to clear my code of clutter and simplify adding new objects onto the screen.
At this point the functions are for the most part functional and serve a purpose.


Codename: Project Demon Realm is a 2D action game where you control the main character who can run and jump around to avoid enemies and projectiles
while also being able to fight back with your sword. The objective of the game is to survive as long as possible, dodging the bullets and killing enemies to rack up score.
The skeleton currently defines the most important features of the game and that is: the ability to move and jump in a smooth manner, attack enemies, have enemies attack you, 
and have enemies on a timer that allows them to respawn. This will be expanded to include a health system to define when the game is over, projectiles that will hit you and take your health,
a score counter, a start menu, a game over screen, and progressively increasing difficulty.

The skeleton currently draws the playable game area, the characters that inhabit it, and allows for movement and attacks to be done. Elements of the game
are currently in motion and are not static. Game variables that are used to maintain and alter the game state are defined and put to use.

The project team is only I, CDT Grimm. No other additional modules other than pygame are required to complete this project.
"""

"""
Attribution:
Hiei Sprites:

"Yu Yu Hakusho 2: Kakutou no Shou (JPN)" by SmithyGCN: https://www.spriters-resource.com/snes/yuyu2/sheet/12631/

Skeleton Sprites:

"GeGeGe no Kitarou (JPN)" by TheouAegis: https://www.spriters-resource.com/game_boy_advance/gegegenokitarou/sheet/29632/

Background:

"The Layers of Hell" by Stoffan2000 on DeviantArt: https://www.deviantart.com/stoffan2000/art/The-Layers-Of-Hell-796090673

Platforms:

"Platform Pixel Pack" by Persi: https://www.gamedevmarket.net/asset/platform-pixel-pack/
"""

import pygame, sys, os

os.environ['SDL_VIDEO_CENTERED'] = '1'

#Variable which changes the resolution of the playable game screen, recommended to stay at 1280x650 for maximum enjoyability
resolutionx = 1280
resolutiony = 650
#Initialize pygame and the game screen as well as the internal clock
pygame.init()
screen = pygame.display.set_mode((resolutionx,resolutiony)) 
clock = pygame.time.Clock()

#Inidividual clocks which track things such as sprite animation and enemy respawns, etc.
ANIMCLOCK = pygame.USEREVENT
pygame.time.set_timer(ANIMCLOCK,100)
DELAY_WALK_1 = 30
DELAY_WALK_2 = 30
DELAY_WALK_3 = 30
HURT_DELAY = 10
DELAY_ENANIM = 200
DELAY_RESPAWN = 30000
#Global constant that should not change
GRAVITY = 0.9
#Variables that keep track of arbitrary things such as which direction the player character or enemy was last facing
lastKnownDirection = 0

#Sprites
#Enemy Sprites
enIdle = pygame.transform.scale2x(pygame.image.load('assets/skeletonIdle.png').convert_alpha())
enWalk1 = pygame.transform.scale2x(pygame.image.load('assets/skeletonWalk1.png').convert_alpha())
enWalk2 = pygame.transform.scale2x(pygame.image.load('assets/skeletonWalk2.png').convert_alpha())
#Hiei sprites
running1 = pygame.image.load('assets/running1.png').convert_alpha()
running2 = pygame.image.load('assets/running2.png').convert_alpha()
idleSprite = pygame.image.load('assets/idle1.png').convert_alpha()
jumpingSprite = pygame.image.load('assets/jump.png').convert_alpha()
fallingSprite = pygame.image.load('assets/falling.png').convert_alpha()
landingSprite1 = pygame.image.load('assets/landing1.png').convert_alpha()
landingSprite2 = pygame.image.load('assets/landing2.png').convert_alpha()
attackSprite1 = pygame.image.load('assets/attack1.png').convert_alpha()
attackSprite2 = pygame.image.load('assets/attack2.png').convert_alpha()
hurtSprite = pygame.transform.flip(pygame.image.load('assets/hit.png').convert_alpha(),True,False)
#hiei is 47px wide and 81px tall
#his sword attacks 54px infront of him

#Hiei's sprites compacted into list which are cycled through to create illusion of animation
attackIndex = 0
runIndex = 0
runningList = [running1,running2]
landingList = [landingSprite1,landingSprite2]
attackList = [attackSprite1,attackSprite2]

#Enemy Sprite variables
activeSprite = idleSprite
enSprite = enIdle
enSpriteIndex = [enIdle,enWalk1,enWalk2]
enSpriteBackwardsIndex = [pygame.transform.flip(enIdle,True,False),pygame.transform.flip(enWalk1,True,False),pygame.transform.flip(enWalk2,True,False)]
enIndex = 0

#Classes that make game objects much easier to work with
class background:
    picture = pygame.image.load('assets/hell-background.png')
    picture = pygame.transform.scale(picture,(resolutionx,resolutiony))

    def __init__(self,x,y):
        self.xPos = x
        self.yPos = y

    def draw(self):
        screen.blit(self.picture,(self.xPos,self.yPos))

class platform:
    #creates a platform at designated location
    def __init__(self,x,y):
        self.sprite = pygame.image.load('assets/demonFloor.png').convert_alpha()
        self.xPos = x
        self.yPos = y
        self.hitbox = self.sprite.get_rect(topleft = (self.xPos,self.yPos))
        #platforms are 125px wide and 124px high

    def draw(self):
        screen.blit(self.sprite,self.hitbox)

class platformUseable:
    #creates a platform which the player character can walk on at designated location
    def __init__(self,x,y):
        self.sprite = pygame.image.load('assets/demonFloor.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite,((resolutionx//2) - 20,45))
        self.xPos = x
        self.yPos = y
        self.hitbox = self.sprite.get_rect(topleft = (self.xPos,self.yPos))

    def draw(self):
        screen.blit(self.sprite,(self.xPos,self.yPos))

class myHero:
    def __init__(self, sprite, xPos, yPos):
        """
        Recieves an initial sprite, the x and y coordinate of the player character.
        Initializes characteristics of the player character that are used to create 
        the basic functions of the game.
        """
        self.sprite = activeSprite
        self.xPos = xPos
        self.yPos = yPos
        self.xSpeed = 0
        self.ySpeed = 0
        self.on_platform = False
        self.attackingNow = False
        self.invincFrames = False
        self.Life = 100

    def update(self):
        """
        Updates different aspects of the player character and his attributes.
        Allows for gravity to affect him and also allows for him to interact with the playable environment.
        """
        #Call this each frame to update position
        self.xPos += self.xSpeed
        self.yPos += self.ySpeed
        self.ySpeed += GRAVITY
        self.direction = bool
        #update hitbox on each frame
        self.hitbox = self.sprite.get_rect(topleft = (self.xPos,self.yPos + 5))

        #collide with platform in the middle
        if self.hitbox.colliderect(middlePlat.hitbox) and self.ySpeed > 0:
            self.on_platform = True
            self.on_ground = True
        else:
            self.on_platform = False
        if self.on_platform == True:
            self.ySpeed = 0
            self.yPos = middlePlat.yPos - 60

        #makes character not fall through ground and checks to see if they are on solid ground
        if self.yPos >= (resolutiony-160):
            self.yPos = resolutiony-160
            self.ySpeed = 0
            self.on_ground = True

    #makes character jump and disallows double jumps
    def jump(self):
        if self.on_ground or self.on_platform:
            self.on_platform = False
            self.on_ground = False
            self.ySpeed = -25

    def draw(self):
        screen.blit(self.sprite, (self.xPos,self.yPos))

class enemy:
    """
    Enemies are defined by a class to allow for ease of use.
    This class makes it much simpler to create additions to the ensemble of enemies on the screen
    """
    def __init__(self,sprite,xPos,yPos):
        self.sprite = enSprite
        self.xPos = xPos
        self.yPos = yPos
        self.xSpeed = 0
        self.alive = False
        self.initialX = xPos
        self.xSpeed = 2

    def update(self):
        self.xPos += self.xSpeed
        self.direction = True
        self.hitbox = self.sprite.get_rect(topleft = (self.xPos,self.yPos))

    def draw(self):
        screen.blit(self.sprite,(self.xPos,self.yPos))

#Actors being defined, this is where all objects that interact are created
hiei = myHero(activeSprite,resolutionx/2,resolutiony/1.5)
hellScape = background(0,0)
middlePlat = platformUseable(resolutionx/4,resolutiony/2.25)
enemy1 = enemy(enSprite,50,resolutiony-165)
enemy2 = enemy(enSprite,800,resolutiony-165)
enemy3 = enemy(enSprite,resolutionx//4 + 50,resolutiony//2.25 - 65)
#a list of the enemies present, mutable in order to allow for the game to increase in difficulty
enemyList = [enemy1,enemy2,enemy3]
#This index chooses which enemy in the list will respawn next
respawnIndex = 0

def drawGround():
    """
    This procedure will draw the ground at the appropriate length no matter how large the game screen is
    """
    groundPieces = []
    count = 0
    neededGround = (resolutionx/120) + 1
    while neededGround > 0:
        groundPieces.append(count)
        count += 120
        neededGround -= 1
    for z in groundPieces:
        hellGround = platform(z,resolutiony-105)
        hellGround.draw()


def movementAnimations():
    """
    This procedure will tell the game which sprite to use depending on the state of the player character.
    Takes the attributes defined in the classes and translates them to animations that are played.
    """
    if lastKnownDirection == 1:
        hiei.direction = True
    else:
        hiei.direction = False
    if hiei.invincFrames == True:
        hiei.sprite = hurtSprite
    if hiei.ySpeed < 0 and hiei.invincFrames == False:
        hiei.sprite = fallingSprite
    elif hiei.ySpeed > 0 and hiei.invincFrames == False:
        hiei.sprite = jumpingSprite
    elif hiei.xSpeed == 0 and hiei.ySpeed == 0 and hiei.invincFrames == False:
        hiei.sprite = idleSprite
    elif (hiei.xSpeed > 0 or hiei.xSpeed < 0) and hiei.invincFrames == False:
        hiei.sprite = runningList[runIndex]
    if hiei.xSpeed < 0:
        hiei.direction = False
    elif hiei.xSpeed > 0:
        hiei.direction = True
    if hiei.attackingNow == True:
        hiei.sprite = attackList[attackIndex]
    if hiei.direction == False:
        hiei.sprite = pygame.transform.flip(hiei.sprite,True,False)
    
def enemy_direction(enemy):
    """
    This function will make the enemies switch directions in order to complete their patrolling cycle.
    The one parameter that is required is essential in order to make it compatible with a later function called enemy_actions.
    """
    if enemy.xSpeed < 0:
        enemy.sprite = enSpriteIndex[enIndex]
    else:
        enemy.sprite = enSpriteBackwardsIndex[enIndex]

def revive_enemy(enemy):
    """
    This function accepts one parameter which is enemy that works with the main game loop to revive a specific enemy 
    """
    enemy.alive = True

def check_collision(enemy):
    """
    This function accepts one parameter and that is the enemy which is being collided with.
    It checks to see if the collision is with the player character while he is attack or while he is not,
    and applies appropriate measures as to hit the player character or make the enemy die.
    """
    if enemy.hitbox.colliderect(hiei.hitbox) and hiei.attackingNow == True:
        enemy.alive = False
    elif enemy.hitbox.colliderect(hiei.hitbox) and hiei.attackingNow == False:
        hiei.invincFrames = True
        hiei.Life -= 1
        print(hiei.Life)
        if hiei.on_platform == True:
            hiei.yPos -= 10

def enemy_actions(enemy):
    """
    This function accepts the parameter of enemy which correlates to our class enemy and applies the functions listed below to the enemies on the screen.
    The use of this series of functions is to easily apply attributes to unique enemies and makes the player character's
    interactions with each enemy sprite unique and not apply them to all enemies.
    Seperates enemy interactions to individual sprites.
    """
    enemy.draw()
    enemy.update()
    check_collision(enemy)

while True:
    """
    This is the main game loop that is used to run the actual game.
    It keeps track of user inputs that call upon different functions to perform the associated actions.
    I was able to find a way to keep track of many different game clocks that interact with different things
    such as enemy walk animation, enemy patrolling patterns, player animations, and the player state.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and hiei.invincFrames == False:
            if event.key == pygame.K_LEFT:
                hiei.xSpeed = -5
                lastKnownDirection = 0
            elif event.key == pygame.K_RIGHT:
                hiei.xSpeed = 5
                lastKnownDirection = 1
            elif event.key == pygame.K_UP:
                hiei.jump()
            elif event.key == pygame.K_SPACE and hiei.attackingNow == False:
                hiei.attackingNow = True
                hiei.xSpeed = 0
                attack_time_1 = pygame.time.get_ticks()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and hiei.xSpeed < 0:
                hiei.xSpeed = 0
            elif event.key == pygame.K_RIGHT and hiei.xSpeed > 0:
                hiei.xSpeed = 0
 
        #crucial for animations, allows me to countdown time from last calling and gate how fast things go
        now = pygame.time.get_ticks()

        if event.type == ANIMCLOCK:
            #Hiei attack animation timer
            if hiei.attackingNow == True:
                ATTACK_DELAY_1 = 150
                if ( now > attack_time_1 + ATTACK_DELAY_1):
                    if attackIndex == 0:
                        if lastKnownDirection == 1:
                            hiei.xPos += 54
                        else:
                            hiei.xPos -= 54
                        attackIndex += 1
                    else:
                        attackIndex = 0
                        hiei.attackingNow = False
                    attack_time_1 = now  
            #Hiei run animation timer  
            else:
                if runIndex >= 1:
                    runIndex = 0
                else:
                    runIndex += 1
            #hiei hit timer
            if hiei.invincFrames == True:
                HURT_DELAY -= 1
                if (now < now + HURT_DELAY):
                    if lastKnownDirection == 1:
                        hiei.xSpeed = -5
                    elif lastKnownDirection == 0:
                        hiei.xSpeed = 5
                    hiei.ySpeed -= 4.5
                else:
                    hiei.invincFrames = False
                    hiei.xSpeed = 0
                    HURT_DELAY = 10
            #enemy movement timer
            if enemy1.alive == True:
                DELAY_WALK_1 -= 1
                if ( now >= now + DELAY_WALK_1):
                    enemy1.xSpeed = enemy1.xSpeed * -1
                    DELAY_WALK_1 = 30
            if enemy2.alive == True:
                DELAY_WALK_2 -= 1
                if ( now >= now + DELAY_WALK_2):
                    enemy2.xSpeed = enemy2.xSpeed * -1
                    DELAY_WALK_2 = 30
            if enemy3.alive == True:
                DELAY_WALK_3 -= 1
                if ( now >= now + DELAY_WALK_3):
                    enemy3.xSpeed = enemy3.xSpeed * -1
                    DELAY_WALK_3 = 30
            #enemy walk animation
            DELAY_ENANIM -= 175
            if ( now >= now + DELAY_ENANIM):
                enemy_direction(enemy1)
                enemy_direction(enemy2)
                enemy_direction(enemy3)
                if enIndex < 2:
                    enIndex += 1
                else:
                    enIndex = 0
                
                DELAY_ENANIM = 200
            
            #enemy respawn timer
            DELAY_RESPAWN -= 575 #in order for their paths to not sync up you need to make the timer a weird interval
            if ( now >= now + DELAY_RESPAWN):
                nextinLine = enemyList[respawnIndex]
                revive_enemy(nextinLine)
                if respawnIndex < 2:
                    respawnIndex += 1
                else:
                    respawnIndex = 0
                DELAY_RESPAWN = 30000

    if hiei.xPos > resolutionx - 50:
        hiei.xSpeed = 0
        hiei.xPos -= 1
    elif hiei.xPos < 0:
        hiei.xSpeed = 0
        hiei.xPos += 1 
    if hiei.yPos <= 0:
        hiei.ySpeed = 0
        hiei.yPos += 5

    #landscape functions
    hellScape.draw()
    drawGround()
    #middle platforms
    middlePlat.draw()
    #Character functions
    hiei.update()
    hiei.draw()
    movementAnimations()
    #Enemy behavior
    if enemy1.alive == True:
        enemy_actions(enemy1)
    if enemy2.alive == True:
        enemy_actions(enemy2)
    if enemy3.alive == True:
        enemy_actions(enemy3)

    pygame.display.update()
    clock.tick(120)