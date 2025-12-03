
import pygame
from typing import TYPE_CHECKING, List, Dict, Optional

if TYPE_CHECKING:
    from modules.Game import Game


class Enemy:
    def __init__(self, game: 'Game', x: float, y: float, platform_id: int):
        self.game = game
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.health = 2
        self.speed = 0.8 + (game.level * 0.2)
        self.direction = 1
        self.platform_id = platform_id
        self.current_platform: Optional[Dict] = None


        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 200

        self.find_platform()

    def find_platform(self) -> None:

        for platform in self.game.platforms:
            if platform['id'] == self.platform_id:
                self.current_platform = platform
                self.y = platform['y'] - self.height
                break

    def update(self) -> None:

        if not self.current_platform:
            self.find_platform()
            return


        self.x += self.speed * self.direction


        if self.x <= self.current_platform['x']:
            self.x = self.current_platform['x']
            self.direction = 1
        elif self.x + self.width >= self.current_platform['x'] + self.current_platform['width']:
            self.x = self.current_platform['x'] + self.current_platform['width'] - self.width
            self.direction = -1

        self.y += 0.5


        for platform in self.game.platforms:
            if self.check_collision_with_platform(platform):
                self.y = platform['y'] - self.height


        self.animation_timer += 16
        if self.animation_timer >= self.animation_speed:
            animation_frames = self.game.sprite_manager.get_animation('enemyWalk')
            if animation_frames:
                self.animation_frame = (self.animation_frame + 1) % len(animation_frames)
            else:
                self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_timer = 0

    def check_collision_with_platform(self, platform: Dict) -> bool:

        return (self.x < platform['x'] + platform['width'] and
                self.x + self.width > platform['x'] and
                self.y + self.height > platform['y'] and
                self.y < platform['y'])

    def take_damage(self, damage: int) -> None:

        self.health -= damage

    def is_dead(self) -> bool:

        return self.health <= 0

    def get_rect(self) -> pygame.Rect:

        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self) -> None:

        pass

    def draw(self, screen: pygame.Surface, camera_x: float) -> None:

        animation_frames = self.game.sprite_manager.get_animation('enemyWalk')
        sprite = None

        if animation_frames and self.animation_frame < len(animation_frames):
            sprite = animation_frames[self.animation_frame]

        if sprite:

            if self.direction == -1:
                sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(sprite, (int(self.x - camera_x), int(self.y)))
            else:
                screen.blit(sprite, (int(self.x - camera_x), int(self.y)))
        else:

            color = (0, 170, 0)
            pygame.draw.rect(
                screen,
                color,
                (int(self.x - camera_x), int(self.y), self.width, self.height)
            )


            self.draw_health_bar(screen, camera_x)

    def draw_health_bar(self, screen: pygame.Surface, camera_x: float) -> None:

        if self.health < 2:
            bar_width = self.width
            bar_height = 5
            bar_x = int(self.x - camera_x)
            bar_y = int(self.y) - 10


            pygame.draw.rect(screen, (255, 0, 0),
                             (bar_x, bar_y, bar_width, bar_height))


            health_width = int(bar_width * (self.health / 2))
            pygame.draw.rect(screen, (0, 255, 0),
                             (bar_x, bar_y, health_width, bar_height))