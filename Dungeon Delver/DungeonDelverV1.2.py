#THIS IS ALL THE STUFF BEING LOADED BEFORE THE MENU SCREEN
#Load modules
import pygame
import sys
from pygame.locals import *
from Knight import Knight
from enemy import Enemy
from Key import Key
from enemy2 import Enemy2
from enemy3 import Enemy3
from Wizard import Wizard
pygame.init()

#Set screen dimensions
screen = pygame.display.set_mode((1000, 652))

#Load backgrounds
town = pygame.image.load("images/town.png").convert_alpha();
forest = pygame.image.load("images/forest.jpg").convert_alpha();
castle = pygame.image.load("images/castle.jpeg").convert_alpha();
dungeon = pygame.image.load("images/dungeon.jpeg").convert_alpha();
backgroundWin = pygame.image.load("images/win.png").convert_alpha();
backgroundLose = pygame.image.load("images/lose.png").convert_alpha();

#Set window title and font
pygame.display.set_caption('Dungeon Delver (version 1.2)')
font = pygame.font.SysFont(None, 36)

#Load characters
knight = Knight()
wizard = Wizard()
character = knight
choice = ("no class chosen")

#Load enemies and key off-screen
enemy = Enemy(2000, 2000)
enemy2 = Enemy2(2000, 2000)
enemy3 = Enemy3(2000, 2000)
key = Key(2000, 2000)

#Create groups
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)
enemy_group.add(enemy2)
enemy_group.add(enemy3)

all_group = pygame.sprite.Group()
all_group.add(knight)
all_group.add(wizard)
all_group.add(enemy)
all_group.add(key)
all_group.add(enemy2)
all_group.add(enemy3)

#Set font
font = pygame.font.SysFont(None, 30)

#Set score timer
main_clock = pygame.time.Clock()

#Start the main menu
state = 0

#Allows you to quit the game
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #Load key presses
    keys = pygame.key.get_pressed()

    #Load collisions
    collide_list = pygame.sprite.spritecollide(character, enemy_group, False, collided = None)

    #Lose lives and score if the player hits an enemy
    if len(collide_list) > 0:
        time -= 100
        lives -= 1
        for enemies in collide_list:
            enemies.collision()

    #From now on, most of the code is the same apart from "if state ==", so you dont have to read everything
    #I will write new states in all caps
    #For some reason, the first area code comes before the main menu code, so don't get confused

       #STATE 0 IS MAIN MENU
    if state == 0:

        #Render background image
        screen.blit(town, (0, 0))

        #Create input for character selection and set character lives, then move onto state 1
        if keys[K_k]:
            character = knight
            offCharacter = wizard
            choice =("knight")
            lives = 5

        if keys[K_m]:
            character = wizard
            offCharacter = knight
            choice =("wizard")
            lives = 3

        if keys[K_c]:
            enemy.rect.x = 500
            enemy.rect.y = 100
            enemy2.rect.x = 2000
            enemy3.rect.x = 2000
            key.rect.x = 2000
            character.rect.x = 0
            offCharacter.rect.x = -2000
            time = 0
            state = 1

        #Show instructions
        instructions = font.render('Welcome to Dungeon Delver!  Press M to play as a wizard or K to play as a knight.', 1, (0, 0, 0))
        instructions_rect = instructions.get_rect()
        instructions_rect.topleft = (50, 50)
        screen.blit(instructions, instructions_rect)

        #Show character choice
        charChoice = font.render('Your class is: ' + choice + '- press C to continue.', 1, (0, 0, 0))
        charChoice_rect = charChoice.get_rect()
        charChoice_rect.topleft = (50, 100)
        screen.blit(charChoice, charChoice_rect)

        #Update the screen
        pygame.display.update()

    #STATE 1 IS FIRST BATTLE AREA IN FOREST
    elif state == 1:

        #Set directional controls
        if keys[K_a]:
            direction = 1
        elif keys[K_d]:
            direction = 0
        elif keys[K_w]:
            direction = 2
        elif keys[K_s]:
            direction = 3
        else:
            direction = -1

        #Make level boundaries
        if character.rect.x < 0:
            direction = 0
        elif character.rect.y < 0:
            direction = 3
        elif character.rect.y > 552:
            direction = 2

        #Load background
        screen.blit(forest, (0, 0))

        #Show timer and background
        main_clock.tick(60)
        time -= .015
        time_text = font.render('score: %s' % int(time), 1, (255, 255, 255))
        time_rect = time_text.get_rect()
        time_rect.topleft = (50, 50)
        screen.blit(time_text, time_rect)

        #Show message
        instructions_rect.topleft = (175, 50)
        if character == knight:
            instructions = font.render('You start with five lives, and lose one when you hit a zombie.  Be careful, knight!', 1, (255, 255, 255))
        elif character == wizard:
            instructions = font.render('You start with three lives, and lose one when you hit a zombie.  Be careful, wizard!', 1, (255, 255, 255))
        screen.blit(instructions, instructions_rect)

        #Show lives
        lives_text = font.render('lives: %s' %int(lives), 1, (255, 255, 255))
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (50, 100)
        screen.blit(lives_text, lives_rect)

        #Update player and enemy movements
        enemy.update()
        enemy2.update()
        enemy3.update()
        character.update(direction)
        all_group.clear(screen, forest)
        all_group.draw(screen)

        #Go to death screen if player losses all lives
        if lives <= 0:
            state = 5

        #If the player passes the edge of the screen, move onto the next area and reset enemies and player
        if character.rect.x >= 1000:
            character.rect.x = 0
            enemy2.rect.x = 300
            enemy2.rect.y = 500
            enemy.rect.x = 500
            enemy.rect.y = 100
            state = 2
            time += 100

        #Update the screen
        pygame.display.update()

    #STATE 2 IS OUTSIDE THE DUNGEON WITH THE KEY
    elif state == 2:

        #Set location of the key
        key.rect.x = 700
        key.rect.y = 100

        #Set directional controls
        if keys[K_a]:
            direction = 1
        elif keys[K_d]:
            direction = 0
        elif keys[K_w]:
            direction = 2
        elif keys[K_s]:
            direction = 4
        else:
            direction = -1

        #Set score and background
        main_clock.tick(60)
        time -= .015
        time_text = font.render('score: %s' % int(time), 1, (255, 255, 255))
        screen.blit(castle, (0, 0))
        screen.blit(time_text, time_rect)

        #Show lives
        lives_text = font.render('lives: %s' %int(lives), 1, (255, 255, 255))
        screen.blit(lives_text, lives_rect)

        #Show message
        instructions_rect.topleft = (200, 50)
        instructions = font.render('Get the key!', 1, (255, 255, 255))
        screen.blit(instructions, instructions_rect)

        #Update movements
        enemy.update()
        enemy2.update()
        enemy3.update()
        character.update(direction)
        all_group.clear(screen, castle)
        all_group.draw(screen)

        #If the player hits the key, then the next level begins
        if character.rect.x >= 700 and character.rect.x <= 800 and character.rect.y >= 100 and character.rect.y <= 125:
            character.rect.x = 0
            enemy.rect.x = 500
            enemy.rect.y = 100
            enemy2.rect.x = 300
            enemy2.rect.y = 500
            enemy3.rect.x = 700
            enemy3.rect.y = 100
            state = 3
            time += 200

        #If the player loses lives, the game ends
        if lives <= 0:
            state = 5

        #Update screen
        pygame.display.update()

    #STATE 3 IS THE FINAL LEVEL, THE DUNGEON
    elif state == 3:

        #Remove the key from the last level
        key.rect.x = 2000
        key.rect.y = 2000

        #If the player reaches the end of the level, the game ends
        if character.rect.x >= 1000:
            state = 4
            time += 300

        #Set directional controls
        if keys[K_a]:
                direction = 1
        elif keys[K_d]:
                direction = 0
        elif keys[K_w]:
                direction = 2
        elif keys[K_s]:
                direction = 4
                character.update(direction)
        else:
            direction = -1

        #Set score and background
        main_clock.tick(60)
        time -= .015
        time_text = font.render('score: %s' % int(time), 1, (255, 255, 255))
        screen.blit(dungeon, (0, 0))
        screen.blit(time_text, time_rect)

        #Show lives
        lives_text = font.render('lives: %s' %int(lives), 1, (255, 255, 255))
        screen.blit(lives_text, lives_rect)

        #Show message
        instructions_rect.topleft = (200, 50)
        instructions = font.render('You got the key and opened the doors to the dungeon.', 1, (255, 255, 255))
        screen.blit(instructions, instructions_rect)

        #Update movements
        character.update(direction)
        enemy.update()
        enemy2.update()
        enemy3.update()
        all_group.clear(screen, dungeon)
        all_group.draw(screen)

        #If the player loses too many lives, the game ends
        if lives <= 0:
            state = 5

        #Update screen
        pygame.display.update()

    #STATE 4 IS THE WIN SCREEN
    if state == 4:

        #Render background image and message
        if character == knight:
            if lives < 5:
                instructions = font.render('You beat the game!  Your score was ' + str(time) + ',', 1, (0, 0, 0))
                instructions2 = font.render(' with a bonus of 300 points for making it to the end.  Want to play again?  Press "y".', 1, (0, 0, 0))
            elif lives == 5:
                instructions = font.render('Wow, you not only beat the game, but without dying once!', 1, (0, 0, 0))
                instructions2 = font.render('Your score was ' + str(time) + ', with a bonus of 500 points for not dying.  Want to play again?  Press "y".', 1, (0, 0, 0))
        elif character == wizard:
            if lives < 3:
                instructions = font.render('You beat the game!  Your score was ' + str(time) + ',', 1, (0, 0, 0))
                instructions2 = font.render(' with a bonus of 300 points for making it to the end.  Want to play again?  Press "y".', 1, (0, 0, 0))
            elif lives == 3:
                 instructions = font.render('Wow, you not only beat the game, but without dying once!', 1, (0, 0, 0))
                 instructions2 = font.render('Your score was ' + str(time) + ', with a bonus of 500 points for not dying.  Want to play again?  Press "y".', 1, (0, 0, 0))

        instructions_rect = instructions.get_rect()
        instructions_rect.topleft = (250, 50)
        instructions2_rect = instructions2.get_rect()
        instructions2_rect.topleft = (50, 100)
        screen.blit(backgroundWin, (0, 0))
        screen.blit(instructions, instructions_rect)
        screen.blit(instructions2, instructions2_rect)

        #Return to the main menu after hitting y
        if keys[K_y]:
            state = 0

        #Update screen
        pygame.display.update()

    #STATE 5 IS THE LOSE SCREEN
    if state == 5:

        #Move characters and enemies out
        character.rect.x = -1000
        enemy.rect.x = 1000
        enemy2.rect.x = 1000
        enemy3.rect.x = 1000

        #Render background image and instructions
        instructions = font.render('You lost!  Your score was ' + str(time) + '.  Want to play again?  Press "y".', 1, (0, 0, 0))
        instructions_rect = time_rect
        screen.blit(backgroundLose, (0, 0))
        screen.blit(instructions, instructions_rect)

        #Return to the main menu after hitting y
        if keys[K_y]:
            state = 0

        #Update screen
        pygame.display.update()

#And that's it!  I want to add some attacks and new classes, maybe even potions and multiple adventures.
