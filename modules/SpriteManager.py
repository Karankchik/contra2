import pygame
import os
from typing import Dict, List, Optional, Any, Callable


class SpriteManager:

    def __init__(self):
        self.sprites: Dict[str, pygame.Surface] = {}
        self.animations: Dict[str, List[pygame.Surface]] = {}
        self.loaded_sprites = 0
        self.total_sprites = 0
        self.base_path = "sprites"

        # Словари для спрайтов по уровням
        self.level_sprites: Dict[int, Dict[str, str]] = {
            1: {},  # Спрайты для уровня 1
            2: {},  # Спрайты для уровня 2  
            3: {}  # Спрайты для уровня 3
        }

        # Текущий уровень для загрузки нужных спрайтов
        self.current_level = 1

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
            print(f"Создана папка {self.base_path}. Поместите туда спрайты.")

    def load_all_sprites(self, callback: Callable) -> None:
        """Загружаем все спрайты для всех уровней"""

        # Определяем спрайты для каждого уровня
        self.level_sprites[1] = {
            # Player
            'playerIdle': 'player.png',
            'playerWalking1': 'PlayerWalking1.png',
            'playerWalking2': 'PlayerWalking2.png',
            'playerJumping1': 'PlayerJumping1.png',
            'playerJumping2': 'PlayerJumping2.png',

            # Enemies
            'enemy1': 'enemy1_level1.png',
            'enemy2': 'enemy2_level1.png',
            'enemy3': 'enemy3_level1.png',
            'enemy4': 'enemy4_level1.png',

            # Platforms and objects
            'platform': 'platform_level1.png',
            'health': 'health.png',
            'ammo': 'bullets.png',
            'background': 'background_level1.jpg',

        }

        self.level_sprites[2] = {
            # Player
            'playerIdle': 'player.png',
            'playerWalking1': 'PlayerWalking1.png',
            'playerWalking2': 'PlayerWalking2.png',
            'playerJumping1': 'PlayerJumping1.png',
            'playerJumping2': 'PlayerJumping2.png',

            # Enemies
            'enemy1': 'enemy1_level2.png',
            'enemy2': 'enemy2_level2.png',
            'enemy3': 'enemy3_level2.png',
            'enemy4': 'enemy4_level2.png',

            # Platforms and objects
            'platform': 'platform_level2.jpg',
            'health': 'health.png',
            'ammo': 'bullets.png',
            'background': 'background_level2.jpg',

        }

        self.level_sprites[3] = {
            # Player
            'playerIdle': 'player.png',
            'playerWalking1': 'PlayerWalking1.png',
            'playerWalking2': 'PlayerWalking2.png',
            'playerJumping1': 'PlayerJumping1.png',
            'playerJumping2': 'PlayerJumping2.png',

            # Enemies
            'enemy1': 'enemy1_level3.png',
            'enemy2': 'enemy2_level3.png',
            'enemy3': 'enemy3_level3.png',
            'enemy4': 'enemy4_level3.png',

            # Platforms and objects
            'platform': 'platform_level3.png',
            'health': 'health.png',
            'ammo': 'bullets.png',
            'background': 'background_level3.png',

        }


        self.total_sprites = sum(len(sprites) for sprites in self.level_sprites.values())


        self.load_sprites_for_level(1, callback)

    def load_sprites_for_level(self, level: int, callback: Callable) -> None:

        print(f"Загрузка спрайтов для уровня {level}...")


        self.loaded_sprites = 0
        self.current_level = level

        sprite_list = self.level_sprites.get(level, {})

        for sprite_name, sprite_file in sprite_list.items():
            self.load_sprite(sprite_name, sprite_file, callback, level)

    def load_sprite(self, name: str, filename: str, callback: Callable, level: int = 1) -> None:

        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            path = os.path.join(project_root, self.base_path, filename)

            if not os.path.exists(path):
                path = os.path.join(self.base_path, filename)

            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                img = self.scale_sprite(name, img)
                self.sprites[name] = img
                print(f"✓ Загружен спрайт уровня {level}: {name} из {path}")
            else:
                self.create_fallback_sprite(name, level)
                print(f"⚠ Файл не найден: {filename}, создан фолбэк для: {name}")
        except Exception as e:
            print(f"✗ Ошибка загрузки спрайта {name}: {e}")
            self.create_fallback_sprite(name, level)

        self.loaded_sprites += 1


        if self.loaded_sprites == len(self.level_sprites[self.current_level]):
            self.init_animations()
            print(f"✅ Все спрайты для уровня {self.current_level} загружены!")
            callback()

    def scale_sprite(self, name: str, img: pygame.Surface) -> pygame.Surface:

        if 'player' in name:
            return pygame.transform.scale(img, (40, 60))
        elif 'enemy' in name:
            return pygame.transform.scale(img, (40, 60))
        elif name == 'platform':
            return pygame.transform.scale(img, (100, 20))
        elif name in ['health', 'ammo', 'bullet']:
            return pygame.transform.scale(img, (20, 20))
        elif name == 'background':
            return pygame.transform.scale(img, (2400, 500))
        return img

    def create_fallback_sprite(self, name: str, level: int = 1) -> None:


        colors_by_level = {
            1: {
                'player': (233, 69, 96, 255),  # #e94560
                'enemy': (0, 170, 0, 255),  # #00aa00
                'platform': (139, 69, 19, 255),  # #8b4513
                'health': (255, 0, 0, 255),  # Красный
                'ammo': (255, 255, 0, 255),  # Желтый
                'bullet': (255, 255, 0, 255),  # Желтый
                'background': (15, 52, 96, 255)  # #0f3460
            },
            2: {
                'player': (65, 105, 225, 255),  # #4169e1
                'enemy': (178, 34, 34, 255),  # #b22222
                'platform': (107, 142, 35, 255),  # #6b8e23
                'health': (255, 165, 0, 255),  # Оранжевый
                'ammo': (0, 255, 255, 255),  # Голубой
                'bullet': (0, 255, 255, 255),  # Голубой
                'background': (25, 25, 112, 255)  # #191970
            },
            3: {
                'player': (147, 112, 219, 255),  # #9370db
                'enemy': (255, 140, 0, 255),  # #ff8c00
                'platform': (188, 143, 143, 255),  # #bc8f8f
                'health': (255, 20, 147, 255),  # Розовый
                'ammo': (50, 205, 50, 255),  # #32cd32
                'bullet': (50, 205, 50, 255),  # #32cd32
                'background': (47, 79, 79, 255)  # #2f4f4f
            }
        }

        colors = colors_by_level.get(level, colors_by_level[1])

        if 'player' in name:
            self.sprites[name] = self.create_text_sprite(40, 60, colors['player'], f"P{level}")
        elif 'enemy' in name:
            self.sprites[name] = self.create_text_sprite(40, 60, colors['enemy'], f"E{name[-1]}")
        else:
            if name == 'platform':
                self.sprites[name] = pygame.Surface((100, 20))
                self.sprites[name].fill(colors['platform'])
            elif name == 'health':
                self.sprites[name] = self.create_health_sprite(level)
            elif name == 'ammo':
                self.sprites[name] = self.create_ammo_sprite(level)
            elif name == 'bullet':
                self.sprites[name] = pygame.Surface((8, 4))
                self.sprites[name].fill(colors['bullet'])
            elif name == 'background':
                self.sprites[name] = pygame.Surface((2400, 500))
                self.sprites[name].fill(colors['background'])

    def create_text_sprite(self, width: int, height: int, color: tuple, text: str) -> pygame.Surface:

        img = pygame.Surface((width, height), pygame.SRCALPHA)
        img.fill(color)

        font = pygame.font.Font(None, 12)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        img.blit(text_surface, text_rect)

        return img

    def create_health_sprite(self, level: int = 1) -> pygame.Surface:

        img = pygame.Surface((20, 20), pygame.SRCALPHA)
        if level == 1:
            pygame.draw.polygon(img, (255, 0, 0), [(10, 2), (2, 10), (10, 18), (18, 10)])
        elif level == 2:
            pygame.draw.circle(img, (255, 165, 0), (10, 10), 9)
        else:
            pygame.draw.rect(img, (255, 20, 147), (5, 5, 10, 10))
        return img

    def create_ammo_sprite(self, level: int = 1) -> pygame.Surface:

        img = pygame.Surface((20, 20), pygame.SRCALPHA)
        if level == 1:
            pygame.draw.circle(img, (255, 255, 0), (10, 10), 8)
        elif level == 2:
            pygame.draw.rect(img, (0, 255, 255), (6, 6, 8, 8))
        else:
            pygame.draw.circle(img, (50, 205, 50), (10, 10), 8)
        return img

    def init_animations(self) -> None:

        self.animations['playerWalk'] = [
            self.sprites.get('playerWalking1'),
            self.sprites.get('playerWalking2')
        ]

        self.animations['playerJump'] = [
            self.sprites.get('playerJumping1'),
            self.sprites.get('playerJumping2')
        ]

        self.animations['enemyWalk'] = [
            self.sprites.get('enemy1'),
            self.sprites.get('enemy2'),
            self.sprites.get('enemy3'),
            self.sprites.get('enemy4')
        ]

    def get_sprite(self, name: str) -> Optional[pygame.Surface]:

        return self.sprites.get(name)

    def get_animation(self, name: str) -> List[pygame.Surface]:

        return self.animations.get(name, [])

    def get_animation_frame(self, name: str, frame: int) -> Optional[pygame.Surface]:

        animation = self.animations.get(name, [])
        if animation and 0 <= frame < len(animation):
            return animation[frame]
        return None

    def is_loading_complete(self) -> bool:

        return self.loaded_sprites >= len(self.level_sprites.get(self.current_level, {}))

    def reload_for_level(self, level: int, callback: Callable) -> None:

        if level in self.level_sprites:
            self.sprites.clear()  # Очищаем старые спрайты
            self.animations.clear()  # Очищаем анимации
            self.load_sprites_for_level(level, callback)