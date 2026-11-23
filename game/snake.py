import pygame

from game.config import (
    BLOCK_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    AnimalConfig,
    ANIMALS,
)


class Snake:
    """A class to represent the animal/snake in the game."""

    def __init__(self, animal: AnimalConfig | None = None) -> None:
        """Initialize the animal with starting position, direction, and appearance."""
        self.animal: AnimalConfig = animal if animal is not None else ANIMALS[0]
        self.x: int = SCREEN_WIDTH // 2
        self.y: int = ((SCREEN_HEIGHT + 40) // 2 // BLOCK_SIZE) * BLOCK_SIZE
        self.x_change: int = BLOCK_SIZE
        self.y_change: int = 0
        self.body: list[list[int]] = [[self.x - BLOCK_SIZE, self.y], [self.x, self.y]]
        self.length: int = 2
        self.direction_changed_this_step: bool = False

    def set_animal(self, animal: AnimalConfig) -> None:
        """Update the active animal configuration."""
        self.animal = animal

    def update(self) -> None:
        """Update position based on current direction."""
        self.x += self.x_change
        self.y += self.y_change
        self.direction_changed_this_step = False

        self.body.append([self.x, self.y])

        if len(self.body) > self.length:
            del self.body[0]

    def set_direction(self, x_change: int, y_change: int) -> None:
        """Set movement direction, preventing reversals and rapid double-turns."""
        if self.direction_changed_this_step:
            return

        if x_change != 0 and self.x_change == 0:
            self.x_change = x_change
            self.y_change = 0
            self.direction_changed_this_step = True
        elif y_change != 0 and self.y_change == 0:
            self.y_change = y_change
            self.x_change = 0
            self.direction_changed_this_step = True

    def check_collision_boundary(self) -> bool:
        """Return True if the animal head collided with boundaries or the HUD area."""
        if self.x >= SCREEN_WIDTH or self.x < 0:
            return True
        # Top 40 pixels reserved for HUD bar
        if self.y >= SCREEN_HEIGHT or self.y < 40:
            return True
        return False

    def check_collision_self(self) -> bool:
        """Return True if head collided with its own body."""
        head = [self.x, self.y]
        for segment in self.body[:-1]:
            if segment == head:
                return True
        return False

    def grow(self) -> None:
        """Increase the length of the animal body."""
        self.length += 1

    def reset(self) -> None:
        """Reset to initial position and length."""
        self.x = SCREEN_WIDTH // 2
        self.y = ((SCREEN_HEIGHT + 40) // 2 // BLOCK_SIZE) * BLOCK_SIZE
        self.x_change = BLOCK_SIZE
        self.y_change = 0
        self.body = [[self.x - BLOCK_SIZE, self.y], [self.x, self.y]]
        self.length = 2
        self.direction_changed_this_step = False

    @staticmethod
    def _draw_body_segment(
        surface: pygame.Surface,
        sx: int,
        sy: int,
        animal: AnimalConfig,
        index: int,
    ) -> None:
        """Draw an individual body segment customized for the animal."""
        rect = pygame.Rect(sx, sy, BLOCK_SIZE, BLOCK_SIZE)

        if animal.id == "panda":
            # Alternating black and white panda pattern
            seg_color = animal.body_color if index % 2 == 0 else animal.accent_color
            pygame.draw.rect(surface, seg_color, rect, border_radius=4)
            pygame.draw.rect(surface, (20, 20, 25), rect, 1, border_radius=4)

        elif animal.id == "tiger":
            # Orange segment with tiger stripes
            pygame.draw.rect(surface, animal.body_color, rect, border_radius=4)
            stripe_color = animal.accent_color
            pygame.draw.line(surface, stripe_color, (sx + 5, sy + 3), (sx + 5, sy + BLOCK_SIZE - 3), 2)
            pygame.draw.line(surface, stripe_color, (sx + 13, sy + 3), (sx + 13, sy + BLOCK_SIZE - 3), 2)
            pygame.draw.rect(surface, (180, 80, 10), rect, 1, border_radius=4)

        elif animal.id == "rabbit":
            # Fluffy white/cream segment with soft border
            pygame.draw.rect(surface, animal.body_color, rect, border_radius=5)
            pygame.draw.rect(surface, (210, 210, 220), rect, 1, border_radius=5)

        elif animal.id == "penguin":
            # Dark navy body with white belly center
            pygame.draw.rect(surface, animal.body_color, rect, border_radius=4)
            pygame.draw.rect(surface, (245, 245, 250), (sx + 4, sy + 3, BLOCK_SIZE - 8, BLOCK_SIZE - 6), border_radius=3)

        elif animal.id == "monkey":
            # Warm brown with peach accent patch
            pygame.draw.rect(surface, animal.body_color, rect, border_radius=4)
            pygame.draw.rect(surface, animal.accent_color, (sx + 5, sy + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10), border_radius=2)

        else:  # Snake
            # Emerald green with subtle scales
            pygame.draw.rect(surface, animal.body_color, rect, border_radius=3)
            pygame.draw.rect(surface, (20, 130, 45), rect, 1, border_radius=3)

    @staticmethod
    def _draw_head(
        surface: pygame.Surface,
        sx: int,
        sy: int,
        animal: AnimalConfig,
        direction: tuple[int, int],
    ) -> None:
        """Draw the head segment with animal-specific features and facial direction."""
        head_rect = pygame.Rect(sx, sy, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, animal.head_color, head_rect, border_radius=5)

        dx, dy = direction
        # Determine eye offsets
        if dx > 0:  # Right
            eye1 = (sx + 13, sy + 5)
            eye2 = (sx + 13, sy + 13)
        elif dx < 0:  # Left
            eye1 = (sx + 5, sy + 5)
            eye2 = (sx + 5, sy + 13)
        elif dy < 0:  # Up
            eye1 = (sx + 5, sy + 5)
            eye2 = (sx + 13, sy + 5)
        else:  # Down or stationary
            eye1 = (sx + 5, sy + 13)
            eye2 = (sx + 13, sy + 13)

        # Animal-specific details
        if animal.id == "rabbit":
            # Pink rabbit ears
            ear_color = animal.accent_color
            if dx > 0 or (dx == 0 and dy == 0):
                pygame.draw.ellipse(surface, ear_color, (sx - 3, sy + 2, 5, 5))
                pygame.draw.ellipse(surface, ear_color, (sx - 3, sy + 11, 5, 5))
            elif dx < 0:
                pygame.draw.ellipse(surface, ear_color, (sx + BLOCK_SIZE - 2, sy + 2, 5, 5))
                pygame.draw.ellipse(surface, ear_color, (sx + BLOCK_SIZE - 2, sy + 11, 5, 5))
            elif dy < 0:
                pygame.draw.ellipse(surface, ear_color, (sx + 2, sy + BLOCK_SIZE - 2, 5, 5))
                pygame.draw.ellipse(surface, ear_color, (sx + 11, sy + BLOCK_SIZE - 2, 5, 5))
            else:
                pygame.draw.ellipse(surface, ear_color, (sx + 2, sy - 3, 5, 5))
                pygame.draw.ellipse(surface, ear_color, (sx + 11, sy - 3, 5, 5))
            # Pink nose
            pygame.draw.circle(surface, animal.accent_color, (sx + BLOCK_SIZE // 2, sy + BLOCK_SIZE // 2), 2)

        elif animal.id == "tiger":
            # Tiger rounded ears on corners
            pygame.draw.circle(surface, animal.accent_color, (sx + 3, sy + 3), 3)
            pygame.draw.circle(surface, animal.accent_color, (sx + BLOCK_SIZE - 3, sy + 3), 3)
            # Forehead mark
            pygame.draw.line(surface, animal.accent_color, (sx + BLOCK_SIZE // 2, sy + 2), (sx + BLOCK_SIZE // 2, sy + 6), 2)

        elif animal.id == "panda":
            # Black panda ears on head corners
            pygame.draw.circle(surface, animal.accent_color, (sx + 3, sy + 3), 4)
            pygame.draw.circle(surface, animal.accent_color, (sx + BLOCK_SIZE - 4, sy + 3), 4)
            # Black eye patches
            pygame.draw.circle(surface, animal.accent_color, eye1, 3)
            pygame.draw.circle(surface, animal.accent_color, eye2, 3)

        elif animal.id == "monkey":
            # Protruding side ears
            pygame.draw.circle(surface, animal.accent_color, (sx - 1, sy + BLOCK_SIZE // 2), 3)
            pygame.draw.circle(surface, animal.accent_color, (sx + BLOCK_SIZE + 1, sy + BLOCK_SIZE // 2), 3)

        elif animal.id == "penguin":
            # Orange triangle beak in facing direction
            beak_color = animal.accent_color
            if dx > 0 or (dx == 0 and dy == 0):
                beak = [(sx + BLOCK_SIZE - 2, sy + 7), (sx + BLOCK_SIZE + 4, sy + 10), (sx + BLOCK_SIZE - 2, sy + 13)]
            elif dx < 0:
                beak = [(sx + 2, sy + 7), (sx - 4, sy + 10), (sx + 2, sy + 13)]
            elif dy < 0:
                beak = [(sx + 7, sy + 2), (sx + 10, sy - 4), (sx + 13, sy + 2)]
            else:
                beak = [(sx + 7, sy + BLOCK_SIZE - 2), (sx + 10, sy + BLOCK_SIZE + 4), (sx + 13, sy + BLOCK_SIZE - 2)]
            pygame.draw.polygon(surface, beak_color, beak)

        else:  # Snake
            # Forked red tongue in facing direction
            tongue_color = animal.accent_color
            if dx > 0 or (dx == 0 and dy == 0):
                pygame.draw.line(surface, tongue_color, (sx + BLOCK_SIZE, sy + 10), (sx + BLOCK_SIZE + 4, sy + 10), 2)
            elif dx < 0:
                pygame.draw.line(surface, tongue_color, (sx, sy + 10), (sx - 4, sy + 10), 2)
            elif dy < 0:
                pygame.draw.line(surface, tongue_color, (sx + 10, sy), (sx + 10, sy - 4), 2)
            else:
                pygame.draw.line(surface, tongue_color, (sx + 10, sy + BLOCK_SIZE), (sx + 10, sy + BLOCK_SIZE + 4), 2)

        # Draw eyes (white + pupil)
        pupil_color = (15, 15, 20)
        pygame.draw.circle(surface, (255, 255, 255), eye1, 2)
        pygame.draw.circle(surface, pupil_color, eye1, 1)
        pygame.draw.circle(surface, (255, 255, 255), eye2, 2)
        pygame.draw.circle(surface, pupil_color, eye2, 1)

    @classmethod
    def draw_animal_preview(
        cls,
        surface: pygame.Surface,
        x: int,
        y: int,
        animal: AnimalConfig,
    ) -> None:
        """Draw a compact preview (1 body segment + head) for menus and UI."""
        cls._draw_body_segment(surface, x, y, animal, 0)
        cls._draw_head(surface, x + BLOCK_SIZE, y, animal, (BLOCK_SIZE, 0))

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all body segments and head on the given surface."""
        for i, segment in enumerate(self.body):
            if i == len(self.body) - 1:
                # Head
                self._draw_head(
                    surface,
                    segment[0],
                    segment[1],
                    self.animal,
                    (self.x_change, self.y_change),
                )
            else:
                # Body segment
                self._draw_body_segment(
                    surface,
                    segment[0],
                    segment[1],
                    self.animal,
                    i,
                )
