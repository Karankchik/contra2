import pygame
import sys
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple

from .SpriteManager import SpriteManager
from .Player import Player
from .Enemy import Enemy
from .Bullet import Bullet
from .Pickup import Pickup
from .Particle import Particle

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 500
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
DARK_BLUE = (44, 62, 80)
PLATFORM_COLOR = (139, 69, 19)


class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "gameOver"
    WIN = "win"
    LEVEL_COMPLETE = "levelComplete"
    LOADING = "loading"


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("КОНТРА - Аркадный Автомат")
        self.clock = pygame.time.Clock()

        self.sprite_manager = SpriteManager()

        self.game_state = GameState.LOADING

        self.player: Optional[Player] = None
        self.enemies: List[Enemy] = []
        self.bullets: List[Bullet] = []
        self.platforms: List[Dict] = []
        self.pickups: List[Pickup] = []
        self.particles: List[Particle] = []

        self.score = 0
        self.lives = 3
        self.level = 1
        self.max_level = 3

        self.camera_x = 0
        self.camera_width = SCREEN_WIDTH
        self.camera_height = SCREEN_HEIGHT

        self.level_width = 2400
        self.level_height = 500

        self.load_fonts()

        self.load_sprites()


        self.mouse_pressed = False
        self.last_mouse_press_time = 0

    def load_fonts(self) -> None:

        try:

            self.font_small = pygame.font.Font("fonts/PressStart2P.ttf", 10)
            self.font_medium = pygame.font.Font("fonts/PressStart2P.ttf", 16)
            self.font_large = pygame.font.Font("fonts/PressStart2P.ttf", 24)
        except:

            self.font_small = pygame.font.Font(None, 20)
            self.font_medium = pygame.font.Font(None, 30)
            self.font_large = pygame.font.Font(None, 48)

    def load_sprites(self) -> None:

        print("Начинаем загрузку спрайтов...")
        self.sprite_manager.load_all_sprites(self.on_sprites_loaded)

    def on_sprites_loaded(self) -> None:

        print("Все спрайты загружены!")
        self.game_state = GameState.MENU

    def on_level_sprites_loaded(self) -> None:

        print(f"Спрайты для уровня {self.level} загружены!")
        self.generate_level()
        if self.player:
            self.player.x = 50
            self.player.y = 400
        self.camera_x = 0
        self.game_state = GameState.PLAYING

    def start(self) -> None:

        if not self.sprite_manager.is_loading_complete():
            print("Еще не все спрайты загружены!")
            return

        self.game_state = GameState.PLAYING
        self.score = 0
        self.lives = 3
        self.level = 1
        self.player = Player(self)
        self.generate_level()

    def generate_level(self) -> None:

        self.enemies.clear()
        self.bullets.clear()
        self.platforms.clear()
        self.pickups.clear()
        self.particles.clear()

        self.level_width = 2000 + (self.level * 400)

        if self.level == 1:
            self.generate_level_1()
        elif self.level == 2:
            self.generate_level_2()
        elif self.level == 3:
            self.generate_level_3()

        self.update_camera()
        self.update_ui()

    def generate_level_1(self) -> None:

        self.platforms = [
            {'x': 0, 'y': 450, 'width': 400, 'height': 20, 'id': 1},
            {'x': 450, 'y': 400, 'width': 300, 'height': 20, 'id': 2},
            {'x': 800, 'y': 350, 'width': 250, 'height': 20, 'id': 3},
            {'x': 1100, 'y': 300, 'width': 300, 'height': 20, 'id': 4},
            {'x': 1500, 'y': 400, 'width': 300, 'height': 20, 'id': 5},
            {'x': 1900, 'y': 350, 'width': 200, 'height': 20, 'id': 6},
            {'x': 0, 'y': 480, 'width': self.level_width, 'height': 20, 'id': 0}
        ]

        self.enemies.append(Enemy(self, 500, 380, 2))
        self.enemies.append(Enemy(self, 850, 330, 3))
        self.enemies.append(Enemy(self, 1200, 280, 4))
        self.enemies.append(Enemy(self, 1600, 380, 5))

        self.pickups = [
            Pickup(self, 420, 370, 'health'),
            Pickup(self, 700, 320, 'ammo'),
            Pickup(self, 1250, 270, 'health'),
            Pickup(self, 1700, 370, 'ammo')
        ]

    def generate_level_2(self) -> None:

        self.platforms = [
            {'x': 0, 'y': 450, 'width': 350, 'height': 20, 'id': 1},
            {'x': 400, 'y': 400, 'width': 300, 'height': 20, 'id': 2},
            {'x': 750, 'y': 350, 'width': 280, 'height': 20, 'id': 3},
            {'x': 1080, 'y': 300, 'width': 320, 'height': 20, 'id': 4},
            {'x': 1450, 'y': 250, 'width': 250, 'height': 20, 'id': 5},
            {'x': 1750, 'y': 400, 'width': 200, 'height': 20, 'id': 6},
            {'x': 2000, 'y': 350, 'width': 180, 'height': 20, 'id': 7},
            {'x': 2230, 'y': 300, 'width': 170, 'height': 20, 'id': 8},
            {'x': 0, 'y': 480, 'width': self.level_width, 'height': 20, 'id': 0}
        ]

        self.enemies.append(Enemy(self, 450, 380, 2))
        self.enemies.append(Enemy(self, 800, 330, 3))
        self.enemies.append(Enemy(self, 1150, 280, 4))
        self.enemies.append(Enemy(self, 1550, 230, 5))
        self.enemies.append(Enemy(self, 1850, 380, 6))
        self.enemies.append(Enemy(self, 2100, 330, 7))

        self.pickups = [
            Pickup(self, 380, 370, 'ammo'),
            Pickup(self, 900, 270, 'health'),
            Pickup(self, 1300, 220, 'ammo'),
            Pickup(self, 1650, 170, 'health'),
            Pickup(self, 1950, 320, 'ammo'),
            Pickup(self, 2300, 270, 'health')
        ]

    def generate_level_3(self) -> None:

        self.platforms = [
            {'x': 0, 'y': 450, 'width': 300, 'height': 20, 'id': 1},
            {'x': 350, 'y': 420, 'width': 280, 'height': 20, 'id': 2},
            {'x': 680, 'y': 390, 'width': 260, 'height': 20, 'id': 3},
            {'x': 990, 'y': 360, 'width': 240, 'height': 20, 'id': 4},
            {'x': 1280, 'y': 330, 'width': 220, 'height': 20, 'id': 5},
            {'x': 1550, 'y': 400, 'width': 200, 'height': 20, 'id': 6},
            {'x': 1800, 'y': 280, 'width': 180, 'height': 20, 'id': 7},
            {'x': 2030, 'y': 250, 'width': 160, 'height': 20, 'id': 8},
            {'x': 2240, 'y': 350, 'width': 140, 'height': 20, 'id': 9},
            {'x': 2430, 'y': 300, 'width': 120, 'height': 20, 'id': 10},
            {'x': 2600, 'y': 400, 'width': 100, 'height': 20, 'id': 11},
            {'x': 0, 'y': 480, 'width': self.level_width, 'height': 20, 'id': 0}
        ]

        self.enemies.append(Enemy(self, 400, 400, 2))
        self.enemies.append(Enemy(self, 730, 370, 3))
        self.enemies.append(Enemy(self, 1040, 340, 4))
        self.enemies.append(Enemy(self, 1350, 310, 5))
        self.enemies.append(Enemy(self, 1650, 380, 6))
        self.enemies.append(Enemy(self, 1900, 260, 7))
        self.enemies.append(Enemy(self, 2130, 230, 8))
        self.enemies.append(Enemy(self, 2340, 330, 9))

        self.pickups = [
            Pickup(self, 320, 370, 'health'),
            Pickup(self, 600, 310, 'ammo'),
            Pickup(self, 950, 280, 'health'),
            Pickup(self, 1250, 250, 'ammo'),
            Pickup(self, 1600, 320, 'health'),
            Pickup(self, 1850, 200, 'ammo'),
            Pickup(self, 2100, 150, 'health'),
            Pickup(self, 2400, 250, 'ammo')
        ]

    def update_camera(self) -> None:

        if self.player:
            self.camera_x = self.player.x - self.camera_width / 2
            self.camera_x = max(0, min(self.camera_x, self.level_width - self.camera_width))

    def update(self) -> None:

        if self.game_state != GameState.PLAYING:
            return

        keys = pygame.key.get_pressed()

        if self.player:
            self.player.update(keys)
            self.update_camera()


            mouse_buttons = pygame.mouse.get_pressed()
            current_time = pygame.time.get_ticks()

            if mouse_buttons[0] and not self.mouse_pressed:

                mouse_pos = pygame.mouse.get_pos()

                self.player.shoot_mouse(mouse_pos)
                self.mouse_pressed = True
                self.last_mouse_press_time = current_time
            elif not mouse_buttons[0]:
                self.mouse_pressed = False

            elif mouse_buttons[0] and self.mouse_pressed:
                if current_time - self.last_mouse_press_time > self.player.weapons[self.player.current_weapon][
                    'fire_rate']:
                    mouse_pos = pygame.mouse.get_pos()
                    self.player.shoot_mouse(mouse_pos)
                    self.last_mouse_press_time = current_time

        for enemy in self.enemies[:]:
            enemy.update()

            if self.player and self.check_collision(self.player, enemy):
                self.player.take_damage(20)
                enemy.x += enemy.direction * 10

            if enemy.is_dead():
                self.create_explosion(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2)
                self.enemies.remove(enemy)
                self.score += 100

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_out_of_bounds(self.level_width):
                self.bullets.remove(bullet)

        for pickup in self.pickups[:]:
            if self.player and self.check_collision(self.player, pickup):
                pickup.collect(self.player)
                self.pickups.remove(pickup)

        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

        self.check_collisions()
        self.update_ui()

        if len(self.enemies) == 0:
            self.level_complete()

    def check_collisions(self) -> None:

        for bullet in self.bullets[:]:
            if not bullet.is_enemy:
                for enemy in self.enemies[:]:
                    if self.check_collision(bullet, enemy):
                        enemy.take_damage(bullet.damage)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break

    def check_collision(self, obj1, obj2) -> bool:

        rect1 = obj1.get_rect() if hasattr(obj1, 'get_rect') else pygame.Rect(obj1.x, obj1.y, obj1.width, obj1.height)
        rect2 = obj2.get_rect() if hasattr(obj2, 'get_rect') else pygame.Rect(obj2.x, obj2.y, obj2.width, obj2.height)
        return rect1.colliderect(rect2)

    def create_explosion(self, x: float, y: float) -> None:

        for _ in range(8):
            self.particles.append(Particle(x, y))

    def update_ui(self) -> None:

        pass

    def render(self) -> None:

        self.screen.fill(DARK_BLUE)

        if self.game_state == GameState.LOADING:
            self.render_loading_screen()
        elif self.game_state == GameState.PLAYING:
            self.render_game()
        elif self.game_state == GameState.MENU:
            self.render_menu()
        elif self.game_state == GameState.PAUSED:
            self.render_game()
            self.render_pause_screen()
        elif self.game_state == GameState.GAME_OVER:
            self.render_game()
            self.render_game_over_screen()
        elif self.game_state == GameState.WIN:
            self.render_game()
            self.render_win_screen()
        elif self.game_state == GameState.LEVEL_COMPLETE:
            self.render_game()
            self.render_level_complete_screen()

        pygame.display.flip()

    def render_game(self) -> None:

        clip_rect = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        self.render_background()

        self.render_platforms()

        for pickup in self.pickups:
            pickup.draw(self.screen, self.camera_x)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x)

        for bullet in self.bullets:
            bullet.draw(self.screen, self.camera_x)

        for particle in self.particles:
            particle.draw(self.screen, self.camera_x)

        if self.player:
            self.player.draw(self.screen, self.camera_x)

        self.screen.set_clip(clip_rect)

        self.render_ui()


        if self.game_state == GameState.PLAYING:
            mouse_pos = pygame.mouse.get_pos()
            crosshair_size = 12
            crosshair_color = (255, 255, 255, 180)


            pygame.draw.line(
                self.screen, crosshair_color,
                (mouse_pos[0], mouse_pos[1] - crosshair_size),
                (mouse_pos[0], mouse_pos[1] + crosshair_size),
                2
            )

            pygame.draw.line(
                self.screen, crosshair_color,
                (mouse_pos[0] - crosshair_size, mouse_pos[1]),
                (mouse_pos[0] + crosshair_size, mouse_pos[1]),
                2
            )


            pygame.draw.circle(
                self.screen, (255, 0, 0, 200),
                mouse_pos, 3
            )

    def render_background(self) -> None:

        background_sprite = self.sprite_manager.get_sprite('background')
        if background_sprite:
            for x in range(0, self.level_width, background_sprite.get_width()):
                if x + background_sprite.get_width() > self.camera_x and x < self.camera_x + SCREEN_WIDTH:
                    self.screen.blit(background_sprite, (x - self.camera_x, 0))
        else:

            self.screen.fill((15, 52, 96), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def render_platforms(self) -> None:

        platform_sprite = self.sprite_manager.get_sprite('platform')
        for platform in self.platforms:
            if (platform['x'] + platform['width'] > self.camera_x and
                    platform['x'] < self.camera_x + SCREEN_WIDTH):

                if platform_sprite:

                    for x_offset in range(0, platform['width'], platform_sprite.get_width()):
                        draw_x = platform['x'] + x_offset - self.camera_x
                        sprite_width = min(platform_sprite.get_width(), platform['width'] - x_offset)
                        scaled_sprite = pygame.transform.scale(
                            platform_sprite,
                            (sprite_width, platform_sprite.get_height())
                        )
                        self.screen.blit(scaled_sprite, (draw_x, platform['y']))
                else:

                    pygame.draw.rect(
                        self.screen,
                        PLATFORM_COLOR,
                        (
                            int(platform['x'] - self.camera_x),
                            int(platform['y']),
                            platform['width'],
                            platform['height']
                        )
                    )

    def render_ui(self) -> None:

        ui_rect = pygame.Rect(15, 15, 180, 140)

        ui_surface = pygame.Surface((ui_rect.width, ui_rect.height), pygame.SRCALPHA)
        ui_surface.fill((44, 62, 80, 200))
        self.screen.blit(ui_surface, ui_rect)

        pygame.draw.rect(self.screen, YELLOW, ui_rect, 3, border_radius=8)

        texts = [
            f"LEVEL: {self.level}",
            f"LIVES: {self.lives}",
            f"HEALTH: {self.player.health if self.player else 0}",
            f"SCORE: {self.score:06d}",
            f"AMMO: {self.player.weapons['pistol']['ammo'] if self.player else 0}",
            f"ENEMIES: {len(self.enemies)}"
        ]

        colors = [YELLOW, RED, GREEN, BLUE, YELLOW, RED]

        for i, (text, color) in enumerate(zip(texts, colors)):
            text_surface = self.font_small.render(text, True, color)
            self.screen.blit(text_surface, (30, 25 + i * 22))

    def render_loading_screen(self) -> None:

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        progress = self.sprite_manager.loaded_sprites / max(self.sprite_manager.total_sprites, 1)

        loading_text = self.font_large.render(
            f"LOADING: {self.sprite_manager.loaded_sprites}/{self.sprite_manager.total_sprites}",
            True, WHITE
        )
        text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(loading_text, text_rect)

        bar_width = 400
        bar_height = 20
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = SCREEN_HEIGHT // 2 + 20

        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        fill_width = int(bar_width * progress)
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, fill_width, bar_height))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

    def render_menu(self) -> None:

        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)

        menu_surface = pygame.Surface((menu_rect.width, menu_rect.height), pygame.SRCALPHA)
        menu_surface.fill((26, 26, 46, 200))
        self.screen.blit(menu_surface, menu_rect)

        pygame.draw.rect(self.screen, YELLOW, menu_rect, 5, border_radius=15)

        title = self.font_large.render("🎮 CONTRA 🎮", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title, title_rect)

        self.render_menu_buttons()

    def render_menu_buttons(self) -> None:

        start_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(self.screen, RED, start_btn, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, start_btn, 3, border_radius=10)

        start_text = self.font_medium.render("INSERT COIN", True, WHITE)
        start_text_rect = start_text.get_rect(center=start_btn.center)
        self.screen.blit(start_text, start_text_rect)

        instr_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
        pygame.draw.rect(self.screen, BLUE, instr_btn, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, instr_btn, 3, border_radius=10)

        instr_text = self.font_medium.render("HOW TO PLAY", True, WHITE)
        instr_text_rect = instr_text.get_rect(center=instr_btn.center)
        self.screen.blit(instr_text, instr_text_rect)

    def render_pause_screen(self) -> None:

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font_large.render("PAUSED", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(pause_text, pause_rect)

        continue_text = self.font_small.render("PRESS P TO CONTINUE", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(continue_text, continue_rect)

    def render_game_over_screen(self) -> None:

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font_medium.render(f"FINAL SCORE: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        level_text = self.font_medium.render(f"LEVEL: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
        self.screen.blit(level_text, level_rect)

        menu_text = self.font_small.render("PRESS ESC FOR MENU", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(menu_text, menu_rect)

    def render_win_screen(self) -> None:

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        win_text = self.font_large.render("VICTORY!", True, GREEN)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(win_text, win_rect)

        score_text = self.font_medium.render(f"FINAL SCORE: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)

        lives_text = self.font_medium.render(f"LIVES: {self.lives}", True, WHITE)
        lives_rect = lives_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 5))
        self.screen.blit(lives_text, lives_rect)

        levels_text = self.font_medium.render(f"LEVELS: {self.max_level}", True, WHITE)
        levels_rect = levels_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(levels_text, levels_rect)

        menu_text = self.font_small.render("PRESS ESC FOR MENU", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(menu_text, menu_rect)

    def render_level_complete_screen(self) -> None:

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        level_text = self.font_large.render("LEVEL COMPLETE!", True, GREEN)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(level_text, level_rect)

        score_text = self.font_medium.render(f"SCORE: {self.score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        lives_text = self.font_medium.render(f"LIVES: {self.lives}", True, YELLOW)
        lives_rect = lives_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
        self.screen.blit(lives_text, lives_rect)

        continue_text = self.font_small.render("PRESS ANY KEY TO CONTINUE", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(continue_text, continue_rect)

    def level_complete(self) -> None:
        """Завершение уровня и переход к следующему"""
        self.level += 1
        if self.level <= self.max_level:
            self.game_state = GameState.LEVEL_COMPLETE
        else:
            self.win_game()

    def win_game(self) -> None:

        self.game_state = GameState.WIN

    def show_instructions(self) -> None:

        temp_screen = self.screen.copy()

        instructions_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        instructions_surface.fill((0, 0, 0, 220))

        title = self.font_large.render("🎯 HOW TO PLAY", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        instructions_surface.blit(title, title_rect)

        instructions = [
            "←→ ARROWS: MOVE",
            "SPACE/W/↑: JUMP",
            "MOUSE: AIM",
            "LEFT CLICK: SHOOT",
            "P KEY: PAUSE",
            "ESC: MENU",
            "DESTROY ALL ENEMIES!"
        ]

        for i, instruction in enumerate(instructions):
            text = self.font_medium.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40 + i * 30))
            instructions_surface.blit(text, text_rect)

        back_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
        pygame.draw.rect(instructions_surface, RED, back_btn, border_radius=10)
        pygame.draw.rect(instructions_surface, WHITE, back_btn, 3, border_radius=10)

        back_text = self.font_medium.render("BACK", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_btn.center)
        instructions_surface.blit(back_text, back_text_rect)

        self.screen.blit(temp_screen, (0, 0))
        self.screen.blit(instructions_surface, (0, 0))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.collidepoint(event.pos):
                        waiting = False

        self.screen.blit(temp_screen, (0, 0))
        pygame.display.flip()

    def run(self) -> None:

        running = True
        showing_instructions = False

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    showing_instructions = self.handle_mouse_click(event, showing_instructions)

            if showing_instructions:
                self.show_instructions()
                showing_instructions = False

            self.update()
            self.render()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def handle_keydown(self, event: pygame.event.Event) -> None:

        if event.key == pygame.K_ESCAPE:
            self.handle_escape_key()
        elif event.key == pygame.K_p:
            self.handle_pause_key()
        elif self.game_state == GameState.LEVEL_COMPLETE:
            self.handle_level_complete_key(event)

    def handle_escape_key(self) -> None:

        if self.game_state == GameState.PLAYING:
            self.game_state = GameState.MENU
        elif self.game_state == GameState.PAUSED:
            self.game_state = GameState.PLAYING
        elif self.game_state in [GameState.GAME_OVER, GameState.WIN]:
            self.game_state = GameState.MENU

    def handle_pause_key(self) -> None:

        if self.game_state == GameState.PLAYING:
            self.game_state = GameState.PAUSED
        elif self.game_state == GameState.PAUSED:
            self.game_state = GameState.PLAYING

    def handle_level_complete_key(self, event: pygame.event.Event) -> None:
        if event.key not in [pygame.K_ESCAPE, pygame.K_p]:

            self.game_state = GameState.LOADING
            print(f"Загрузка спрайтов для уровня {self.level}...")


            self.sprite_manager.reload_for_level(self.level, self.on_level_sprites_loaded)

    def handle_mouse_click(self, event: pygame.event.Event, showing_instructions: bool) -> bool:

        if self.game_state == GameState.MENU:
            mouse_pos = pygame.mouse.get_pos()
            start_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
            instr_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)

            if start_btn.collidepoint(mouse_pos):
                self.start()
            elif instr_btn.collidepoint(mouse_pos):
                return True

        return showing_instructions