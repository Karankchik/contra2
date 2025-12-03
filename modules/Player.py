import pygame
import math
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from modules.Game import Game
    from modules.Bullet import Bullet


class Player:
    def __init__(self, game: 'Game'):
        self.game = game
        self.x = 50.0
        self.y = 400.0
        self.width = 40
        self.height = 60
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = 3.0
        self.jump_power = 15.0
        self.is_jumping = False
        self.facing = 'right'
        self.health = 100
        self.invulnerable = False
        self.invulnerable_timer = 0

        self.current_animation = 'idle'
        self.animation_frame = 0
        self.animation_timer = 0
        self.walk_animation_speed = 150
        self.jump_animation_speed = 200

        self.weapons: Dict[str, Dict] = {
            'pistol': {
                'name': 'ПИСТОЛЕТ',
                'damage': 1,
                'fire_rate': 300,
                'ammo': 30,
                'max_ammo': 30
            }
        }
        self.current_weapon = 'pistol'
        self.last_shot = 0

    def take_damage(self, damage: int) -> None:

        if self.invulnerable:
            return

        self.health -= damage
        self.invulnerable = True
        self.invulnerable_timer = 60

        if self.health <= 0:
            self.game.lives -= 1
            if self.game.lives <= 0:
                self.game.game_state = 'gameOver'
            else:
                self.respawn()

    def respawn(self) -> None:

        self.x = 50
        self.y = 400
        self.velocity_y = 0
        self.is_jumping = False
        self.health = 100
        self.invulnerable = False
        self.current_animation = 'idle'
        self.animation_frame = 0
        self.animation_timer = 0

    def update(self, keys: Dict[int, bool]) -> None:

        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        self.velocity_x = 0
        is_moving = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing = 'left'
            is_moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing = 'right'
            is_moving = True

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and not self.is_jumping:
            self.velocity_y = -self.jump_power
            self.is_jumping = True
            self.animation_frame = 0
            self.animation_timer = 0

        self.animation_timer += 16

        new_animation = 'idle'
        if self.is_jumping:
            new_animation = 'jump'
        elif is_moving:
            new_animation = 'walk'

        if self.current_animation != new_animation:
            self.current_animation = new_animation
            self.animation_frame = 0
            self.animation_timer = 0

        self.update_animation()

        self.velocity_y += 0.8
        self.x += self.velocity_x
        self.y += self.velocity_y

        self.x = max(0, min(self.x, self.game.level_width - self.width))

        self.check_platform_collisions()

        if self.y > self.game.level_height:
            self.take_damage(50)

    def update_animation(self) -> None:

        if self.current_animation == 'walk':
            if self.animation_timer >= self.walk_animation_speed:
                animation_frames = self.game.sprite_manager.get_animation('playerWalk')
                if animation_frames:
                    self.animation_frame = (self.animation_frame + 1) % len(animation_frames)
                else:
                    self.animation_frame = (self.animation_frame + 1) % 2
                self.animation_timer = 0
        elif self.current_animation == 'jump':
            if self.animation_timer >= self.jump_animation_speed:
                animation_frames = self.game.sprite_manager.get_animation('playerJump')
                if animation_frames:
                    self.animation_frame = (self.animation_frame + 1) % len(animation_frames)
                else:
                    self.animation_frame = (self.animation_frame + 1) % 2
                self.animation_timer = 0

    def check_platform_collisions(self) -> None:

        for platform in self.game.platforms:
            if (self.x < platform['x'] + platform['width'] and
                    self.x + self.width > platform['x'] and
                    self.y + self.height > platform['y'] and
                    self.y < platform['y']):

                if self.velocity_y > 0:
                    self.y = platform['y'] - self.height
                    self.velocity_y = 0
                    self.is_jumping = False
                    if self.current_animation == 'jump':
                        self.current_animation = 'idle'
                        self.animation_frame = 0
                        self.animation_timer = 0

    def shoot_mouse(self, mouse_pos: tuple) -> None:

        weapon = self.weapons[self.current_weapon]
        if weapon['ammo'] <= 0:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot < weapon['fire_rate']:
            return

        weapon['ammo'] -= 1
        self.last_shot = current_time


        mouse_x, mouse_y = mouse_pos
        world_mouse_x = mouse_x + self.game.camera_x


        if world_mouse_x > self.x + self.width / 2:
            direction = 'right'
        else:
            direction = 'left'


        self.facing = direction


        dx = world_mouse_x - (self.x + self.width / 2)
        dy = mouse_y - (self.y + self.height / 2)


        if abs(dx) < 1:
            dx = 1 if direction == 'right' else -1


        angle = math.atan2(dy, dx)


        if direction == 'right':
            bullet_x = self.x + self.width
        else:
            bullet_x = self.x

        bullet_y = self.y + self.height / 2

        from modules.Bullet import Bullet
        bullet = Bullet(
            self.game,
            bullet_x,
            bullet_y,
            direction,
            False,
            weapon['damage'],
            angle
        )
        self.game.bullets.append(bullet)

    def get_rect(self) -> pygame.Rect:

        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self) -> None:

        pass

    def draw(self, screen: pygame.Surface, camera_x: float) -> None:

        if self.invulnerable and (self.invulnerable_timer // 5) % 2 == 0:
            return

        sprite = self.get_current_sprite()

        if sprite:
            self.draw_sprite(screen, sprite, camera_x)
        else:
            self.draw_fallback(screen, camera_x)

    def get_current_sprite(self) -> Optional[pygame.Surface]:

        if self.current_animation == 'walk':
            animation_frames = self.game.sprite_manager.get_animation('playerWalk')
        elif self.current_animation == 'jump':
            animation_frames = self.game.sprite_manager.get_animation('playerJump')
        else:
            return self.game.sprite_manager.get_sprite('playerIdle')

        if animation_frames and self.animation_frame < len(animation_frames):
            return animation_frames[self.animation_frame]

        return None

    def draw_sprite(self, screen: pygame.Surface, sprite: pygame.Surface, camera_x: float) -> None:

        if self.facing == 'left':
            if self.current_animation == 'jump':

                screen.blit(sprite, (int(self.x - camera_x), int(self.y)))
            else:
                flipped_sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(flipped_sprite, (int(self.x - camera_x), int(self.y)))
        else:
            if self.current_animation == 'jump':

                flipped_sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(flipped_sprite, (int(self.x - camera_x), int(self.y)))
            else:
                screen.blit(sprite, (int(self.x - camera_x), int(self.y)))

    def draw_fallback(self, screen: pygame.Surface, camera_x: float) -> None:

        color = (233, 69, 96)
        pygame.draw.rect(
            screen,
            color,
            (int(self.x - camera_x), int(self.y), self.width, self.height)
        )

        font = pygame.font.Font(None, 8)
        text = self.current_animation.upper()
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (int(self.x - camera_x) + 5, int(self.y) + 30))