import random
from itertools import cycle

import numpy as np
import pygame
import sys


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("default")
import settings

birds = []
bestbird = None

def main():
    settings.init()
    while True:
        # select random background sprites
        randBg = random.randint(0, len(settings.BACKGROUNDS_LIST) - 1)
        settings.IMAGES['background'] = pygame.image.load(settings.BACKGROUNDS_LIST[randBg]).convert()
        crashInfo = mainGame()


def mainGame():
    from bird import bird
    global birds
    #Initial Population
    birds = [0] * settings.POPULATION
    for i in range(settings.POPULATION):
        birds[i] = bird()
        birds[i].initialize()

    while True:

        # get 2 new pipes to add to upperPipes lowerPipes list
        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()

        # list of upper pipes
        upperPipes = [
            {'x': settings.SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
            {'x': settings.SCREENWIDTH + 200 + (settings.SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]

        # list of lowerpipe
        lowerPipes = [
            {'x': settings.SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': settings.SCREENWIDTH + 200 + (settings.SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        pipeVelX = -4

        num_crashed_birds = 0
        refresh = False
        while True and not refresh:
            # move pipes to left
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                uPipe['x'] += pipeVelX
                lPipe['x'] += pipeVelX

            # add new pipe when first pipe is about to touch left of screen
            if 0 < upperPipes[0]['x'] < 5:
                newPipe = getRandomPipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

            # remove first pipe if its out of the screen
            if upperPipes[0]['x'] < -settings.pipeW:
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # draw sprites
            settings.SCREEN.blit(settings.IMAGES['background'], (0, 0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                rand_pipe_int = random.randint(0,len(settings.PIPES_LIST)-1)
                settings.SCREEN.blit(settings.IMAGES['pipe'][rand_pipe_int][0], (uPipe['x'], uPipe['y']))
                settings.SCREEN.blit(settings.IMAGES['pipe'][rand_pipe_int][1], (lPipe['x'], lPipe['y']))
            for bird_instance in birds:

                if not bird_instance.crashed and num_crashed_birds<len(birds):

                    # check for crash here
                    crashTest = bird_instance.checkcrash(upperpipes=upperPipes,lowerpipes=lowerPipes)
                    if crashTest[0]:
                        bird_instance.crashed = True
                        num_crashed_birds += 1
                    bird_instance.update_score(upperPipes)
                    bird_instance.think(upperPipes,lowerPipes)


                    settings.SCREEN.blit(settings.IMAGES['base'], (bird_instance.basex, settings.BASEY))
                    # print score so player overlaps the score
                    showScore(bird_instance.score)
                    bird_instance.update_surface()
                    settings.SCREEN.blit(bird_instance.playerSurface, (bird_instance.playerx, bird_instance.playery))
                if num_crashed_birds == len(birds):
                    num_crashed_birds = 0
                    birds = nextGeneration()
                    refresh = True
                    break

            pygame.display.update()
            settings.FPSCLOCK.tick(settings.FPS)





def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
        playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(settings.BASEY * 0.6 - settings.PIPEGAPSIZE))
    gapY += int(settings.BASEY * 0.2)
    pipeHeight = settings.IMAGES['pipe'][0][0].get_height()
    pipeX = settings.SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + settings.PIPEGAPSIZE},  # lower pipe
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0  # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += settings.IMAGES['numbers'][digit].get_width()

    Xoffset = (settings.SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        settings.SCREEN.blit(settings.IMAGES['numbers'][digit], (Xoffset, settings.SCREENHEIGHT * 0.1))
        Xoffset += settings.IMAGES['numbers'][digit].get_width()








#### Genetic ALgorithm helper functions implementation

def calculatefitness():
    global birds
    sum = 0
    for bird_inst in birds:
        # print("Check 2")
        sum += bird_inst.score
    for bird_inst in birds:
        if sum != 0:
            bird_inst.fitness = bird_inst.score
        else:
            bird_inst.fitness = 0
    # print(sum)
    return sum!=0
def pickOne():
    global birds
    index = 0
    fitness_vals = np.array([birds[index].fitness for index in range(len(birds))])
    index2 = np.argmax(fitness_vals)
    print(fitness_vals[index2])
    r = random.random()
    while(r>0 and index<len(birds)):
        r = r-birds[index].fitness
        index+=1
    index-=1
    return index2

def nextGeneration():

    global birds

    from bird import bird

    if(calculatefitness()):
        birds_next = [None]*settings.POPULATION
        birds_next[0] = bird()
        args = {}
        index = pickOne()
        args['nn'] = birds[index].nn.copy()
        birds_next[0].initialize(args)
        for i in range(1,settings.POPULATION):
            birds_next[i] = bird()
            args = {}
            args['nn'] = birds[index].nn.mutate(0.01)
            birds_next[i].initialize(args)
    else:
        birds_next = [None]*settings.POPULATION

        for i in range(settings.POPULATION):
            birds_next[i] = bird()
            birds_next[i].initialize()

    return birds_next

if __name__ == '__main__':
    main()