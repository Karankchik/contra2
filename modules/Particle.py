
import pygame
import random
import math
from typing import Tuple


class Particle:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.size = random.uniform(1, 4)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = 30
        self.color = self.random_explosion_color()

    def random_explosion_color(self) -> Tuple[int, int, int]:

        hue = random.randint(0, 60)
        return self.hsv_to_rgb(hue, 1.0, 1.0)

    def hsv_to_rgb(self, h: int, s: float, v: float) -> Tuple[int, int, int]:

        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:  # 300 <= h < 360
            r, g, b = c, 0, x

        return (
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )

    def update(self) -> None:

        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1

    def is_alive(self) -> bool:

        return self.life > 0

    def draw(self, screen: pygame.Surface, camera_x: float) -> None:

        alpha = self.life / 30
        color_with_alpha = (
            int(self.color[0] * alpha),
            int(self.color[1] * alpha),
            int(self.color[2] * alpha)
        )
        pygame.draw.circle(
            screen,
            color_with_alpha,
            (int(self.x - camera_x), int(self.y)),
            int(self.size)
        )

    def render(self, ctx, camera_x: float) -> None:

        self.draw(ctx, camera_x)