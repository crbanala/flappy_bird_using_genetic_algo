import random,numpy as np,math
from itertools import cycle

from numpy import random
from NeuralNet import NeuralNetwork
import settings
from flappy import pygame

class bird():

    def __init__(self,args=None):
        if args is None:
            #random.seed(1)
            self.nn = NeuralNetwork(5,4,1)
        else:
            self.nn = args['nn']



    def initialize(self,args=None):

        if args is None:
            #random.seed(1)
            self.nn = NeuralNetwork(5,5,1)
        else:
            self.nn = args['nn']


        self.crashed = False
        # movementInfo = showWelcomeAnimation()
        # select random player sprites
        randPlayer = random.randint(0, len(settings.PLAYERS_LIST) - 1)


        #print(type(settings.IMAGES['player'][0][0]))


        self.movementInfo = {
            'playery': int((settings.SCREENHEIGHT - settings.IMAGES['player'][0][0].get_height()) / 2),
            'basex': -10,
            'playerIndexGen': cycle([0, 1, 2, 1]),
        }
        self.basex = self.movementInfo['basex']

        self.score = self.playerIndex = self.loopIter = 0
        self.playerIndexGen = self.movementInfo['playerIndexGen']
        self.playerx, self.playery = int(settings.SCREENWIDTH * 0.2), self.movementInfo['playery']

        # player velocity, max velocity, downward accleration, accleration on flap
        self.playerVelY = -9  # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10  # max vel along Y, max descend speed
        self.playerMinVelY = -8  # min vel along Y, max ascend speed
        self.playerAccY = 1  # players downward accleration
        self.playerRot = 45  # player's rotation
        self.playerVelRot = 3  # angular speed
        self.playerRotThr = 20  # rotation threshold
        self.playerFlapAcc = -9  # players speed on flapping
        self.playerFlapped = False  # True when player flaps
        # hitmask for player'



    def getHitmask(self,image):
        """returns a hitmask using an image's alpha."""
        mask = []
        for x in range(image.get_width()):
            mask.append([])
            for y in range(image.get_height()):
                mask[x].append(bool(image.get_at((x, y))[3]))
        return mask

    def checkcrash(self,upperpipes=None,lowerpipes=None):
        return self.checkCrashhelper({'x': self.playerx, 'y': self.playery, 'index': self.playerIndex}, upperpipes, lowerpipes)

    def checkCrashhelper(self,player, upperPipes, lowerPipes):
        """returns True if player collders with base or pipes."""
        pi = player['index']


        player['w'] = settings.IMAGES['player'][0][0].get_width()
        player['h'] = settings.IMAGES['player'][0][0].get_height()

        # if player crashes into ground
        if player['y'] + player['h'] >= settings.BASEY - 1:
            return [True, True]
        # if player['y'] + player['h'] <= SCREENHEIGHT - 1:
        #     return [True, True]
        else:

            playerRect = pygame.Rect(player['x'], player['y'],
                                     player['w'], player['h'])

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                # upper and lower pipe rects
                uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], settings.pipeW, settings.pipeH)
                lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], settings.pipeW, settings.pipeH)

                # player and upper/lower pipe hitmasks
                pHitMask = settings.HITMASKS['player'][pi][0]
                uHitmask = settings.HITMASKS['pipe'][0]
                lHitmask = settings.HITMASKS['pipe'][1]

                # if bird collided with upipe or lpipe
                uCollide = self.pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
                lCollide = self.pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

                if uCollide or lCollide:
                    return [True, False]

        return [False, False]

    def pixelCollision(self,rect1, rect2, hitmask1, hitmask2):
        """Checks if two objects collide and not just their rects"""
        rect = rect1.clip(rect2)

        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - rect1.x, rect.y - rect1.y
        x2, y2 = rect.x - rect2.x, rect.y - rect2.y

        for x in range(rect.width):
            for y in range(rect.height):
                if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                    return True
        return False

    def decide_to_flap(self,args=None):
        input = [args['y'],args['pipex'],args['upipey'],args['lpipey'],args['vely']]
        hidden_state, output = self.nn.think(np.array(input))
        #print(output)
        if output[0]>0.5:
            #print("*True")
            return True
        else:
            #print("*False")
            return False



    def think(self,upperPipes, lowerPipes):
        closestpipe = None
        closestpipeindex = 0
        closestDistance = math.inf
        for index, pipe in enumerate(upperPipes):
            pipeMidPos = pipe['x'] + settings.IMAGES['pipe'][0][0].get_width() / 2
            dist = pipeMidPos - self.playerMidPos
            if dist > 0 and closestDistance > dist:
                closestpipe = pipe
                closestDistance = dist
                closestpipeindex = index

        if len(upperPipes) > 0:
            pipex = closestpipe['x'] + settings.IMAGES['pipe'][0][0].get_width() / 2 - self.playerMidPos
            upipey = closestpipe['y'] + settings.IMAGES['pipe'][0][0].get_height()
            lpipey = lowerPipes[closestpipeindex]['y']
            # print("x : {} y : {} pipex : {} upipey: {} lpipey: {}".format(playerMidPos, playerMidPosy , pipex,upipey,lpipey))

        if self.playery > -2 * settings.IMAGES['player'][0][0].get_height():
            args = {}
            args['y'], args['pipex'], args['lpipey'], args[
                'upipey'] = self.playerMidPosy / settings.SCREENHEIGHT, pipex / settings.SCREENWIDTH, lpipey / settings.SCREENHEIGHT, upipey / settings.SCREENHEIGHT
            args['y'], args['pipex'], args['lpipey'], args['upipey'] = self.playerMidPosy, pipex, lpipey, upipey
            args['vely'] = self.playerVelY
            # print(args)
            self.playerFlapped = self.decide_to_flap(args=args)
            if self.playerFlapped:
                self.playerVelY = self.playerFlapAcc

        # playerIndex basex change
        if (self.loopIter + 1) % 3 == 0:
            playerIndex = next(self.playerIndexGen)
        self.loopIter = (self.loopIter + 1) % 30
        self.basex = -((-self.basex + 100) % settings.baseShift)

        # rotate the player
        if self.playerRot > -90:
            self.playerRot -= self.playerVelRot

        # player's movement
        if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
            self.playerVelY += self.playerAccY
        if self.playerFlapped:
            self.playerFlapped = False
            # more rotation to cover the threshold (calculated in visible rotation)
            self.playerRot = 45

        self.playerHeight = settings.IMAGES['player'][self.playerIndex][0].get_height()
        self.playery += min(self.playerVelY, settings.BASEY - self.playery - self.playerHeight)




    def update_score(self,upperPipes):
        # check for score
        self.playerMidPos = self.playerx + settings.IMAGES['player'][0][0].get_width() / 2
        self.playerMidPosy = self.playery
        indexiter = -1
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + settings.IMAGES['pipe'][0][0].get_width() / 2
            indexiter += 1
            if pipeMidPos <= self.playerMidPos < pipeMidPos + 4:
                # print("Check 1")
                self.score += 1

    def update_surface(self):
        # Player rotation has a threshold
        self.visibleRot = self.playerRotThr
        if self.playerRot <= self.playerRotThr:
            self.visibleRot = self.playerRot
        self.playerSurface = pygame.transform.rotate(settings.IMAGES['player'][self.playerIndex][0], self.visibleRot)

if __name__ == '__main__':
    print("heyy")