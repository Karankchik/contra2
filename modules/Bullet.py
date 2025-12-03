import pygame
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.Game import Game


class Bullet:
    def __init__(self, game: 'Game', x: float, y: float,
                 direction: str, is_enemy: bool = False, damage: int = 1, angle: float = 0):
        self.game = game
        self.x = x
        self.y = y
        self.width = 8
        self.height = 4
        self.speed = 10
        self.direction = direction
        self.is_enemy = is_enemy
        self.damage = damage
        self.angle = angle
        self.speed_x = math.cos(angle) * self.speed
        self.speed_y = math.sin(angle) * self.speed
        self.is_angled = angle != 0

    def update(self) -> None:
        if self.is_angled:

            self.x += self.speed_x
            self.y += self.speed_y
        else:

            if self.direction == 'right':
                self.x += self.speed
            else:
                self.x -= self.speed

    def is_out_of_bounds(self, level_width: float) -> bool:

        if self.is_angled:
            return (self.x < -50 or self.x > level_width + 50 or
                    self.y < -50 or self.y > 600)
        return self.x < -50 or self.x > level_width + 50

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self) -> None:
        pass

    def draw(self, screen: pygame.Surface, camera_x: float) -> None:
        sprite = self.game.sprite_manager.get_sprite('bullet')

        if sprite and not self.is_enemy:

            if self.is_angled:

                rotated_sprite = pygame.transform.rotate(sprite, -math.degrees(self.angle))

                rotated_rect = rotated_sprite.get_rect(center=sprite.get_rect(center=(0, 0)).center)
                screen.blit(rotated_sprite,
                            (int(self.x - camera_x - rotated_rect.width // 2 + self.width // 2),
                             int(self.y - rotated_rect.height // 2 + self.height // 2)))
            else:
                screen.blit(sprite, (int(self.x - camera_x), int(self.y)))
        else:
            color = (255, 0, 0) if self.is_enemy else (255, 255, 0)


            if self.is_angled:
                pygame.draw.circle(
                    screen,
                    color,
                    (int(self.x - camera_x + self.width // 2), int(self.y + self.height // 2)),
                    4
                )
            else:
                pygame.draw.rect(
                    screen,
                    color,
                    (int(self.x - camera_x), int(self.y), self.width, self.height)
                )