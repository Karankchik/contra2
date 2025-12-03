
import pygame
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.Game import Game


def main():

    pygame.init()
    pygame.mixer.init()


    game = Game()
    game.run()


if __name__ == "__main__":
    main()