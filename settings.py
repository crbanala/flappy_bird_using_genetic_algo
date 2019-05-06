from flappy import pygame

FPS = 50
SCREENWIDTH = 288
SCREENHEIGHT = 512
# amount by which base can maximum shift to left
PIPEGAPSIZE = 100  # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.79
POPULATION = 500
# image, sound and hitmask  dicts

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)



def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask






def init():
    global IMAGES,FPS ,baseShift, pipeH,pipeW,HITMASKS,SCREEN,FPSCLOCK
    IMAGES, SOUNDS, HITMASKS = {}, {}, {}
    pipeW, pipeH = 0, 0
    baseShift = 0
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()
    #pipeindex = random.randint(0, len(PIPES_LIST) - 1)
    IMAGES['pipe'] = [None] * len(PIPES_LIST)
    for pipeindex in range(len(PIPES_LIST)):
        IMAGES['pipe'][pipeindex] = (
        pygame.transform.rotate(
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
        pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
    )
    HITMASKS['pipe'] = (
        getHitmask(IMAGES['pipe'][0][0]),
        getHitmask(IMAGES['pipe'][0][1]),
    )

    pipeW = IMAGES['pipe'][0][0].get_width()
    pipeH = IMAGES['pipe'][0][0].get_height()
    IMAGES['player']=[None]*len(PLAYERS_LIST)
    HITMASKS['player'] =[None]*len(PLAYERS_LIST)
    for randPlayer in range(len(PLAYERS_LIST)):
        IMAGES['player'][randPlayer] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )
        HITMASKS['player'][randPlayer] = (
            getHitmask(IMAGES['player'][randPlayer][0]),
            getHitmask(IMAGES['player'][randPlayer][1]),
            getHitmask(IMAGES['player'][randPlayer][2]),
        )
    IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[0]).convert()
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()