import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.Game import Game
    from modules.Player import Player


class Pickup:
    def __init__(self, game: 'Game', x: float, y: float, type_: str):
        self.game = game
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.type = type_

    def collect(self, player: 'Player') -> None:

        if self.type == 'health':
            player.health = min(player.health + 30, 100)
        elif self.type == 'ammo':
            weapon = player.weapons.get(player.current_weapon)
            if weapon:
                weapon['ammo'] = weapon['max_ammo']

    def get_rect(self) -> pygame.Rect:

        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self) -> None:

        pass

    def draw(self, screen: pygame.Surface, camera_x: float) -> None:

        sprite = None

        if self.type == 'health':
            sprite = self.game.sprite_manager.get_sprite('health')
        elif self.type == 'ammo':
            sprite = self.game.sprite_manager.get_sprite('ammo')

        if sprite:
            screen.blit(sprite, (int(self.x - camera_x), int(self.y)))
        else:

            color = (255, 0, 0) if self.type == 'health' else (255, 255, 0)
            pygame.draw.rect(
                screen,
                color,
                (int(self.x - camera_x), int(self.y), self.width, self.height)
            )