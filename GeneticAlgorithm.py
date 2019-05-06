from flappy import *
def nextGeneration():
    birds = [None]*POPULATION
    for i in range(POPULATION):
        birds[i] = bird()
        birds[i].initialize()
    return birds