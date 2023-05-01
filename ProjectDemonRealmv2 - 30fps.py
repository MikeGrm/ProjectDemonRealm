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

Projectiles:

"Fireball" by Haagnus: https://www.spriters-resource.com/genesis_32x_scd/kidchameleon/sheet/31742/
"""

import pygame, sys, os, random

os.environ['SDL_VIDEO_CENTERED'] = '1'

#Variable which changes the resolution of the playable game screen, recommended to stay at 1280x650 for maximum enjoyability
resolutionx = 1280
resolutiony = 650
#Initialize pygame and the game screen as well as the internal clock
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((resolutionx,resolutiony)) 
clock = pygame.time.Clock()

#Inidividual clocks which track things such as sprite animation and enemy respawns, etc.
ANIMCLOCK = pygame.USEREVENT
pygame.time.set_timer(ANIMCLOCK,100)
DELAY_WALK_1 = 60
DELAY_WALK_2 = 60
DELAY_WALK_3 = 60
HURT_DELAY = 10
DELAY_ENANIM = 100
DELAY_RESPAWN = 30000
scoreTimer = 10
DELAY_BALL= 1
#Global constant that should not change
GRAVITY = 3.5
#Gamestate variables
lastKnownDirection = 0
gameActive = False
gameOver = False
playerScore = 0
playerHiScore = 0

#Sounds
ENhitSound = pygame.mixer.Sound('assets/ENHit.wav')
hitSound = pygame.mixer.Sound('assets/hit5.wav')
jumpSound = pygame.mixer.Sound('assets/jumppp11.wav')
attackSound = pygame.mixer.Sound('assets/swordsound.wav')
backgroundNoise = pygame.mixer.Sound('assets/gamemusic.wav')
firebackground = pygame.mixer.Sound('assets/burning1.wav')
backgroundNoise.set_volume(0.25)
backgroundNoise.play(-1)
firebackground.set_volume(0.05)
firebackground.play(-1)
#Sprites

#Heart sprites
fullHeart = pygame.transform.scale(pygame.image.load('assets/FULLheart.png').convert_alpha(),(50,50))
halfHeart = pygame.transform.scale(pygame.image.load('assets/HALFheart.png').convert_alpha(),(50,50))
emptyHeart = pygame.transform.scale(pygame.image.load('assets/EMPTYheart.png').convert_alpha(),(50,50))
#Projectile Sprites
fireball1 = pygame.transform.scale(pygame.image.load('assets/fireball1.png').convert_alpha(),(50,15))
fireball2 = pygame.transform.scale(pygame.image.load('assets/fireball2.png').convert_alpha(),(50,15))
projectileSprite = fireball1
fireballList = [fireball1,fireball2]
fireIndex = 0
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

class projectile:
    def __init__(self,x,y,direction):
        self.sprite = projectileSprite
        self.xPos = x
        self.yPos = y
        self.xSpeed = 10
        if direction < 0:
            self.sprite = pygame.transform.flip(self.sprite,True,False)
            self.rightBall = True
        elif direction > 0:
            self.rightBall = False
    def flight(self,direction):
        self.hitbox = self.sprite.get_rect(center = (self.xPos,self.yPos))
        self.xPos += self.xSpeed * direction
        if self.rightBall == True and self.xPos <= -500:
            self.xPos = 1300
            self.yPos = random.randrange(150,550)
        elif self.rightBall == False and self.xPos >= 1800:
            self.xPos = -50
            self.yPos = random.randrange(125,550)
            
    def draw(self):
        screen.blit(self.sprite,self.hitbox)

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
        self.jumpSoft = False

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
    def jump(self,jumpSpeed):
        if self.on_ground or self.on_platform:
            jumpSound.play()
            self.on_platform = False
            self.on_ground = False
            self.ySpeed = jumpSpeed

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
        self.alive = False
        self.initialX = xPos
        self.xSpeed = 3

    def update(self):
        self.xPos += self.xSpeed
        self.direction = True
        self.hitbox = self.sprite.get_rect(topleft = (self.xPos,self.yPos))

    def draw(self):
        screen.blit(self.sprite,(self.xPos,self.yPos))

class hearts:
    def __init__(self,x,y):
        self.sprite = fullHeart
        self.xPos = x
        self.yPos = y
        self.rect = self.sprite.get_rect(topleft = (x,y))
    def draw(self):
        screen.blit(self.sprite,self.rect)

#Actors being defined, this is where all objects that interact are created
hiei = myHero(activeSprite,resolutionx/2,resolutiony/1.5)
hellScape = background(0,0)
middlePlat = platformUseable(resolutionx/4,resolutiony/2.25)
enemy1 = enemy(enSprite,50,resolutiony-165)
enemy2 = enemy(enSprite,675,resolutiony-165)
enemy3 = enemy(enSprite,resolutionx//4 + 30,resolutiony//2.25 - 65)
#a list of the enemies present, mutable in order to allow for the game to increase in difficulty
enemyList = [enemy1,enemy2,enemy3]
#This index chooses which enemy in the list will respawn next
respawnIndex = 0
#projectiles
ball1,ball2,ball3,ball4,ball5,ball6,ball7,ball8,ball9,ball10 = projectile(1300,500,-1),projectile(-50,420,1),\
projectile(1300,150,-1),projectile(-50,150,1),projectile(1300,200,-1),projectile(-50,550,1),projectile(1300,200,-1),projectile(-50,550,1),projectile(1300,200,-1),projectile(-50,550,1)

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
    if enemy.hitbox.colliderect(hiei.hitbox) and hiei.attackingNow == True and isinstance(enemy,projectile) == False:
        enemy.alive = False
        ENhitSound.play()
        global playerScore
        playerScore += 5
    elif enemy.hitbox.colliderect(hiei.hitbox) and hiei.attackingNow == False and hiei.invincFrames == False:
        hiei.invincFrames = True
        hiei.Life -= 5
        hitSound.play()
        if hiei.on_platform == True:
            hiei.yPos -= 10
        if isinstance(enemy,projectile) == True:
            hiei.Life -= 10
            if enemy.rightBall == True:
                enemy.xPos = -10
            else:
                enemy.xPos = 1300
    if isinstance(enemy,projectile) == True and enemy.hitbox.colliderect(middlePlat.hitbox):
        if enemy.rightBall == True:
            enemy.xPos = -10
        else:
            enemy.xPos = 1300

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

def text_display():
    #game font
    font_size = 50
    game_font = pygame.font.Font('assets/AmazDooMLeft.ttf',font_size)
    if gameActive == True:
        health_surface = game_font.render(f'HEALTH:',True,(255,255,255))
        health_rect = health_surface.get_rect(topleft = (0,0))
        outlineHp_surface = game_font.render(f'HEALTH:',True,(0,0,0))
        outlineHp_rect = outlineHp_surface.get_rect(topleft = (0,0))
        outlineHp_rect = outlineHp_rect.inflate(6,6)
        screen.blit(outlineHp_surface,outlineHp_rect)
        screen.blit(health_surface,health_rect)
        draw_health()
        score_surface = game_font.render(f'Score: {playerScore}',True,(255,255,255))
        outline_surface = game_font.render(f'Score: {playerScore}',True,(0,0,0))
        outline_rect = outline_surface.get_rect(topleft = (0,50))
        outline_rect = outline_rect.inflate(8,8)
        score_rect = score_surface.get_rect(topleft = (0,50))
        screen.blit(outline_surface,outline_rect)
        screen.blit(score_surface,score_rect)
    if gameActive == False and gameOver == False:
        start_screen = pygame.transform.scale(pygame.image.load('assets/projectDemonRealmTitleScreen.png').convert_alpha(),(resolutionx,resolutiony))
        screen.blit(start_screen,(0,0))
        highScore_surface = game_font.render(f'HIGHSCORE: {playerHiScore}',True,(255,255,255))
        hiX = resolutionx//2.4
        hiY = 575
        highScore_rect = highScore_surface.get_rect(topleft = (hiX,hiY))
        screen.blit(highScore_surface,highScore_rect)
    elif gameOver == True:
        end_screen = pygame.transform.scale(pygame.image.load('assets/gameoverScreen.png').convert_alpha(),(resolutionx,resolutiony))
        screen.blit(end_screen,(0,0))
        highScore_surface = game_font.render(f'HIGHSCORE: {playerHiScore}',True,(255,255,255))
        hiX = resolutionx//2.4
        hiY = 400
        highScore_rect = highScore_surface.get_rect(topleft = (hiX,hiY))
        screen.blit(highScore_surface,highScore_rect)


def draw_health():
    heart1 = hearts(110,0)
    heart2 = hearts(165,0)
    heart3 = hearts(220,0)
    heart4 = hearts(275,0)
    heart5 = hearts(330,0)
    if hiei.Life <= 90:
        heart5.sprite = halfHeart
    if hiei.Life <= 80:
        heart5.sprite = emptyHeart
    if hiei.Life <= 70:
        heart4.sprite = halfHeart
    if hiei.Life <= 60:
        heart4.sprite = emptyHeart
    if hiei.Life <= 50:
        heart3.sprite = halfHeart
    if hiei.Life <= 40:
        heart3.sprite = emptyHeart
    if hiei.Life <= 30:
        heart2.sprite = halfHeart
    if hiei.Life <= 20:
        heart2.sprite = emptyHeart
    if hiei.Life <= 10:
        heart1.sprite = halfHeart
    heart1.draw()
    heart2.draw()
    heart3.draw()
    heart4.draw()
    heart5.draw()

def fireballFlight(ball,direction):
    ball.flight(direction)
    check_collision(ball)
    ball.draw()

def fireballAnimation(ball):
    if ball.rightBall == False:
        ball.sprite = fireballList[fireIndex]
    else: ball.sprite = pygame.transform.flip(fireballList[fireIndex],True,False)

while True:
    """
    This is the main game loop that is used to run the actual game.
    It keeps track of user inputs that call upon different functions to perform the associated actions.
    I was able to find a way to keep track of many different game clocks that interact with different things
    such as enemy walk animation, enemy patrolling patterns, player animations, and the player state.
    """
    if gameActive == False and gameOver == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameActive = True
                    playerScore = 0
                    startTime = pygame.time.get_ticks()
    if gameActive == True and gameOver == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and hiei.invincFrames == False:
                if event.key == pygame.K_LEFT:
                    hiei.xSpeed = -10
                    lastKnownDirection = 0
                if event.key == pygame.K_LSHIFT:
                    hiei.jumpSoft = True
                elif event.key == pygame.K_RIGHT:
                    hiei.xSpeed = 10
                    lastKnownDirection = 1
                elif event.key == pygame.K_UP and hiei.jumpSoft == True:
                    hiei.jump(-30)
                elif event.key == pygame.K_UP:
                    hiei.jump(-45)
                elif event.key == pygame.K_SPACE and hiei.attackingNow == False:
                    hiei.attackingNow = True
                    
                    hiei.xSpeed = 0
                    attack_time_1 = pygame.time.get_ticks()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and hiei.xSpeed < 0:
                    hiei.xSpeed = 0
                elif event.key == pygame.K_RIGHT and hiei.xSpeed > 0:
                    hiei.xSpeed = 0
                if event.key == pygame.K_LSHIFT:
                    hiei.jumpSoft = False
    
            #crucial for animations, allows me to countdown time from last calling and gate how fast things go
            now = pygame.time.get_ticks()
            if event.type == ANIMCLOCK:
                if( now < scoreTimer + now):
                    scoreTimer -= 1
                else:
                    playerScore += 1
                    scoreTimer = 10
                #Hiei attack animation timer
                if hiei.attackingNow == True:
                    ATTACK_DELAY_1 = 150
                    if ( now > attack_time_1 + ATTACK_DELAY_1):
                        if attackIndex == 0:
                            attackSound.play()
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
                            hiei.xSpeed = -10
                        elif lastKnownDirection == 0:
                            hiei.xSpeed = 10 
                        if hiei.ySpeed < -8:
                            hiei.ySpeed +- 1000
                        elif hiei.ySpeed == 0:   
                            hiei.ySpeed -= 8
                        if hiei.on_platform == True:
                            hiei.yPos -= 10 
                    else: 
                        hiei.invincFrames = False
                        hiei.xSpeed = 0
                        HURT_DELAY = 10
                #enemy movement timer
                if enemy1.alive == True:
                    DELAY_WALK_1 -= 1
                    if ( now >= now + DELAY_WALK_1):
                        enemy1.xSpeed = enemy1.xSpeed * -1
                        DELAY_WALK_1 = 60
                if enemy2.alive == True:
                    DELAY_WALK_2 -= 1
                    if ( now >= now + DELAY_WALK_2):
                        enemy2.xSpeed = enemy2.xSpeed * -1
                        DELAY_WALK_2 = 60
                if enemy3.alive == True:
                    DELAY_WALK_3 -= 1
                    if ( now >= now + DELAY_WALK_3):
                        enemy3.xSpeed = enemy3.xSpeed * -1
                        DELAY_WALK_3 = 60
                #enemy walk animation
                DELAY_ENANIM -= 95
                if ( now >= now + DELAY_ENANIM):
                    enemy_direction(enemy1)
                    enemy_direction(enemy2)
                    enemy_direction(enemy3)
                    if enIndex < 2:
                        enIndex += 1
                    else:
                        enIndex = 0
                    
                    DELAY_ENANIM = 100
                
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
                #fireball animation timer
                DELAY_BALL -= 1
                if ( now >= now + DELAY_BALL):
                    fireballAnimation(ball1)
                    fireballAnimation(ball2)
                    fireballAnimation(ball3)
                    fireballAnimation(ball4)
                    fireballAnimation(ball5)
                    fireballAnimation(ball6)
                    fireballAnimation(ball7)
                    fireballAnimation(ball8)
                    fireballAnimation(ball9)
                    fireballAnimation(ball10)
                    if fireIndex < 1:
                        fireIndex += 1
                    else:
                        fireIndex = 0
                    
                    DELAY_BALL = 1
        #prevents character from moving off the screen
        if hiei.xPos > resolutionx - 50:
            hiei.xPos = 5
        elif hiei.xPos < 0:
            hiei.xPos = resolutionx - 45
        if hiei.yPos <= 0:
            hiei.ySpeed = 0
            hiei.yPos += 5

        if hiei.Life <= 0:
            gameOver = True
            gameActive = False
            if playerScore > playerHiScore:
                playerHiScore = playerScore


        #landscape functions
        hellScape.draw()
        drawGround()
        #middle platforms
        middlePlat.draw()
        #Character functions
        hiei.update()
        hiei.draw()
        movementAnimations()
        #fireball functions
        fireballFlight(ball1,-1)
        fireballFlight(ball2,1)
        fireballFlight(ball3,-1)
        if playerScore >= 50:
            fireballFlight(ball4,1)
        if playerScore >= 75:
            fireballFlight(ball5,-1)
        if playerScore >= 100:
            fireballFlight(ball6,1)
        if playerScore >= 125:
            fireballFlight(ball7,1)
        if playerScore >= 150:
            fireballFlight(ball8,1)
        if playerScore >= 175:
            fireballFlight(ball9,1)
        if playerScore >= 200:
            fireballFlight(ball10,1)
        
        #Enemy behavior
        if enemy1.alive == True:
            enemy_actions(enemy1)
        if enemy2.alive == True:
            enemy_actions(enemy2)
        if enemy3.alive == True:
            enemy_actions(enemy3)
    if gameOver == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameOver = False
                    gameAcive = False
                    hiei.Life = 100
                    hiei.xSpeed = 0
                    enemy1.alive = False
                    enemy2.alive = False
                    enemy3.alive = False
                    hiei.xPos = resolutionx/2
                    hiei.yPos = resolutiony/1.5
                    hiei.invincFrames = False
                    playerScore = 0
                    ball1.xPos = 1300
                    ball2.xPos = -50
                    ball3.xPos = 1300
                    ball4.xPos = -50
                    ball5.xPos = 1300
                    ball6.xPos = -50
 
        hellScape.draw()
        drawGround()

    text_display()
    pygame.display.update()
    clock.tick(30)