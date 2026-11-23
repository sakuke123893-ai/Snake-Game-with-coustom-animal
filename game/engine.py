import pygame

from game.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLOCK_SIZE,
    INITIAL_SNAKE_SPEED,
    COLOR_BLACK,
    COLOR_WHITE,
    COLOR_RED,
    COLOR_GOLD,
    COLOR_GRAY,
    COLOR_DARK_GRAY,
    COLOR_PANEL_BG,
    COLOR_PANEL_SELECTED,
    AnimalConfig,
    ANIMALS,
)
from game.snake import Snake
from game.food import Food

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"


class GameEngine:
    """Manages game state, user input, animal selection, and rendering."""

    def __init__(self) -> None:
        """Initialize the game engine, display window, and fonts."""
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running: bool = True
        self.state: str = STATE_MENU
        self.selected_animal_index: int = 0
        self.score: int = 0

        # Fonts
        font_names = ["Segoe UI", "Arial", "sans-serif"]
        self.title_font = pygame.font.SysFont(font_names, 30, bold=True)
        self.heading_font = pygame.font.SysFont(font_names, 22, bold=True)
        self.body_font = pygame.font.SysFont(font_names, 16)
        self.small_font = pygame.font.SysFont(font_names, 13)

        # Initialize animal and food with default selection (Rabbit)
        initial_animal = ANIMALS[self.selected_animal_index]
        self.snake = Snake(initial_animal)
        self.food = Food(initial_animal)

    @property
    def current_animal(self) -> AnimalConfig:
        """Return the currently selected animal configuration."""
        return ANIMALS[self.selected_animal_index]

    def start_game(self) -> None:
        """Start or restart the game with the chosen animal."""
        animal = self.current_animal
        self.snake.set_animal(animal)
        self.snake.reset()
        self.food.set_animal(animal)
        self.food.respawn([tuple(segment) for segment in self.snake.body])
        self.score = 0
        self.state = STATE_PLAYING

    def handle_input(self) -> None:
        """Process keyboard and mouse events depending on the current state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return

            if self.state == STATE_MENU:
                self._handle_menu_input(event)
            elif self.state == STATE_PLAYING:
                self._handle_playing_input(event)
            elif self.state == STATE_GAME_OVER:
                self._handle_game_over_input(event)

    def _handle_menu_input(self, event: pygame.event.Event) -> None:
        """Handle input during the animal selection menu."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_animal_index = (self.selected_animal_index - 1) % len(ANIMALS)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_animal_index = (self.selected_animal_index + 1) % len(ANIMALS)
            elif pygame.K_1 <= event.key <= pygame.K_1 + len(ANIMALS) - 1:
                self.selected_animal_index = event.key - pygame.K_1
                self.start_game()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start_game()
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                self.is_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            card_x, card_w, card_h = 40, 560, 48
            start_y, spacing = 82, 54

            for i in range(len(ANIMALS)):
                rect = pygame.Rect(card_x, start_y + i * spacing, card_w, card_h)
                if rect.collidepoint(mouse_x, mouse_y):
                    self.selected_animal_index = i
                    self.start_game()
                    break

    def _handle_playing_input(self, event: pygame.event.Event) -> None:
        """Handle movement and shortcuts during active gameplay."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.snake.set_direction(0, -BLOCK_SIZE)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.snake.set_direction(0, BLOCK_SIZE)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.snake.set_direction(-BLOCK_SIZE, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.snake.set_direction(BLOCK_SIZE, 0)
            elif event.key in (pygame.K_c, pygame.K_m):
                # Return to animal selection
                self.state = STATE_MENU
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                self.is_running = False

    def _handle_game_over_input(self, event: pygame.event.Event) -> None:
        """Handle choices after game over."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.start_game()
            elif event.key in (pygame.K_c, pygame.K_m):
                self.state = STATE_MENU
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                self.is_running = False

    def update(self) -> None:
        """Update positions, food eating, and collision detection."""
        if self.state != STATE_PLAYING:
            return

        self.snake.update()

        # Check wall collision
        if self.snake.check_collision_boundary():
            self.state = STATE_GAME_OVER
            return

        # Check self collision
        if self.snake.check_collision_self():
            self.state = STATE_GAME_OVER
            return

        # Check food collision
        snake_head_rect = pygame.Rect(self.snake.x, self.snake.y, BLOCK_SIZE, BLOCK_SIZE)
        food_rect = pygame.Rect(self.food.position[0], self.food.position[1], BLOCK_SIZE, BLOCK_SIZE)

        if snake_head_rect.colliderect(food_rect):
            self.snake.grow()
            self.score += 1
            self.food.respawn([tuple(segment) for segment in self.snake.body])

    def draw(self) -> None:
        """Render the appropriate view based on game state."""
        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_PLAYING:
            self._draw_playing()
        elif self.state == STATE_GAME_OVER:
            self._draw_playing()
            self._draw_game_over_overlay()

        pygame.display.flip()
        self.tick()

    def _draw_menu(self) -> None:
        """Render the animal selection menu."""
        self.screen.fill(COLOR_BLACK)

        # Title and header
        title_surf = self.title_font.render("CHOOSE YOUR ANIMAL", True, COLOR_GOLD)
        self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 35)))

        sub_surf = self.body_font.render(
            "Each animal hunts for its own favorite food!", True, COLOR_GRAY
        )
        self.screen.blit(sub_surf, sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 63)))

        # Animal cards
        card_x, card_w, card_h = 40, 560, 48
        start_y, spacing = 82, 54

        for i, animal in enumerate(ANIMALS):
            card_y = start_y + i * spacing
            card_rect = pygame.Rect(card_x, card_y, card_w, card_h)
            is_selected = (i == self.selected_animal_index)

            # Background fill
            bg_color = COLOR_PANEL_SELECTED if is_selected else COLOR_PANEL_BG
            pygame.draw.rect(self.screen, bg_color, card_rect, border_radius=8)

            # Border
            border_color = COLOR_GOLD if is_selected else COLOR_DARK_GRAY
            border_width = 2 if is_selected else 1
            pygame.draw.rect(self.screen, border_color, card_rect, border_width, border_radius=8)

            # Key number badge [1]
            badge_text = f"[{i + 1}]"
            badge_color = COLOR_GOLD if is_selected else COLOR_GRAY
            badge_surf = self.body_font.render(badge_text, True, badge_color)
            self.screen.blit(badge_surf, (card_x + 14, card_y + 14))

            # Animal preview (1 body + 1 head)
            Snake.draw_animal_preview(self.screen, card_x + 46, card_y + 14, animal)

            # Animal name
            name_color = COLOR_WHITE if is_selected else (220, 220, 225)
            name_surf = self.heading_font.render(animal.name, True, name_color)
            self.screen.blit(name_surf, (card_x + 100, card_y + 12))

            # Favorite food text & icon
            fav_label = self.body_font.render("eats", True, COLOR_GRAY)
            self.screen.blit(fav_label, (card_x + 195, card_y + 15))

            Food.draw_food_icon(self.screen, card_x + 235, card_y + 14, animal)

            food_name_surf = self.heading_font.render(animal.food_name, True, animal.food_color)
            self.screen.blit(food_name_surf, (card_x + 265, card_y + 12))

            # Description
            desc_surf = self.small_font.render(animal.description, True, COLOR_GRAY)
            self.screen.blit(desc_surf, (card_x + 360, card_y + 17))

            # Selection arrow marker
            if is_selected:
                arrow_surf = self.heading_font.render("►", True, COLOR_GOLD)
                self.screen.blit(arrow_surf, (card_x + card_w - 24, card_y + 12))

        # Footer hints
        footer_text = "▲ / ▼ or [1-6] to Select   |   [ENTER] / Click to Play   |   [Q] Quit"
        footer_surf = self.small_font.render(footer_text, True, (160, 165, 180))
        self.screen.blit(footer_surf, footer_surf.get_rect(center=(SCREEN_WIDTH // 2, 458)))

    def _draw_playing(self) -> None:
        """Render active gameplay with HUD and play area."""
        self.screen.fill(COLOR_BLACK)

        # Draw top HUD bar background
        hud_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 40)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, hud_rect)
        pygame.draw.line(self.screen, COLOR_DARK_GRAY, (0, 40), (SCREEN_WIDTH, 40), 1)

        animal = self.current_animal

        # Left: Score
        score_surf = self.heading_font.render(f"Score: {self.score}", True, COLOR_GOLD)
        self.screen.blit(score_surf, (15, 8))

        # Center: Current Animal and Favorite Food preview
        center_x = SCREEN_WIDTH // 2 - 120
        Snake.draw_animal_preview(self.screen, center_x, 10, animal)

        animal_name_surf = self.body_font.render(animal.name, True, COLOR_WHITE)
        self.screen.blit(animal_name_surf, (center_x + 48, 11))

        eats_surf = self.body_font.render("loves", True, COLOR_GRAY)
        self.screen.blit(eats_surf, (center_x + 115, 11))

        Food.draw_food_icon(self.screen, center_x + 160, 10, animal)

        food_name_surf = self.body_font.render(animal.food_name, True, animal.food_color)
        self.screen.blit(food_name_surf, (center_x + 188, 11))

        # Right: Shortcuts
        nav_surf = self.small_font.render("[C] Change Animal  |  [Q] Quit", True, COLOR_GRAY)
        self.screen.blit(nav_surf, (SCREEN_WIDTH - nav_surf.get_width() - 15, 13))

        # Draw game elements
        self.food.draw(self.screen)
        self.snake.draw(self.screen)

    def _draw_game_over_overlay(self) -> None:
        """Draw a modal overlay when game is over."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 15, 205))
        self.screen.blit(overlay, (0, 0))

        box_w, box_h = 420, 260
        box_rect = pygame.Rect(
            (SCREEN_WIDTH - box_w) // 2,
            (SCREEN_HEIGHT - box_h) // 2,
            box_w,
            box_h,
        )
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, box_rect, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_RED, box_rect, 2, border_radius=12)

        # Game Over Title
        go_surf = self.title_font.render("GAME OVER", True, COLOR_RED)
        self.screen.blit(go_surf, go_surf.get_rect(center=(SCREEN_WIDTH // 2, box_rect.top + 38)))

        # Final score
        score_surf = self.heading_font.render(
            f"Final Score: {self.score}", True, COLOR_GOLD
        )
        self.screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, box_rect.top + 80)))

        # Animal and Food eaten recap
        animal = self.current_animal
        recap_y = box_rect.top + 120
        recap_center = SCREEN_WIDTH // 2 - 80
        Snake.draw_animal_preview(self.screen, recap_center, recap_y, animal)

        ate_text = f"{animal.name} ate {self.score} {animal.food_name}s!"
        ate_surf = self.body_font.render(ate_text, True, COLOR_WHITE)
        self.screen.blit(ate_surf, (recap_center + 50, recap_y + 1))

        # Action buttons / keys
        play_again_surf = self.body_font.render(
            f"Press [R] to Play Again as {animal.name}", True, COLOR_WHITE
        )
        self.screen.blit(play_again_surf, play_again_surf.get_rect(center=(SCREEN_WIDTH // 2, box_rect.top + 170)))

        change_surf = self.body_font.render(
            "Press [C] to Choose a Different Animal", True, COLOR_GOLD
        )
        self.screen.blit(change_surf, change_surf.get_rect(center=(SCREEN_WIDTH // 2, box_rect.top + 200)))

        quit_surf = self.small_font.render(
            "Press [Q] or [ESC] to Quit", True, COLOR_GRAY
        )
        self.screen.blit(quit_surf, quit_surf.get_rect(center=(SCREEN_WIDTH // 2, box_rect.top + 230)))

    def tick(self) -> None:
        """Control frame rate."""
        # In menu mode, refresh at 30 FPS for smooth UI responsiveness
        fps = 30 if self.state == STATE_MENU else INITIAL_SNAKE_SPEED
        self.clock.tick(fps)
