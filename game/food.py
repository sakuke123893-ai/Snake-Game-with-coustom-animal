import random
import pygame

from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, AnimalConfig, ANIMALS


class Food:
    """A class representing the food item in the game."""

    def __init__(self, animal: AnimalConfig | None = None) -> None:
        """Initialize location and type of the food."""
        self.animal: AnimalConfig = animal if animal is not None else ANIMALS[0]
        self.position: tuple[int, int] = (0, 0)
        self.respawn([])

    def set_animal(self, animal: AnimalConfig) -> None:
        """Update the food to match the selected animal's favorite food."""
        self.animal = animal

    def respawn(self, snake_body: list[tuple[int, int]]) -> None:
        """
        Move the food to a new random location on the grid.

        Keeps the food within the play area and off the top HUD bar and current snake.
        """
        while True:
            random_x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            # Start at grid row 2 to avoid overlapping the top score/status bar
            random_y = random.randint(2, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            new_position = (random_x, random_y)

            if new_position not in snake_body:
                self.position = new_position
                break

    @staticmethod
    def draw_food_icon(surface: pygame.Surface, x: int, y: int, animal: AnimalConfig) -> None:
        """Draw a custom icon for the animal's favorite food at the given coordinates."""
        food_type = animal.food_type

        if food_type == "carrot":
            # Orange tapered carrot root
            root_pts = [
                (x + 4, y + 6),
                (x + BLOCK_SIZE - 4, y + 6),
                (x + BLOCK_SIZE // 2, y + BLOCK_SIZE - 2),
            ]
            pygame.draw.polygon(surface, animal.food_color, root_pts)
            # Leafy green tops
            pygame.draw.line(surface, animal.food_secondary_color, (x + BLOCK_SIZE // 2, y + 6), (x + BLOCK_SIZE // 2, y + 1), 2)
            pygame.draw.line(surface, animal.food_secondary_color, (x + BLOCK_SIZE // 2, y + 6), (x + 3, y + 2), 2)
            pygame.draw.line(surface, animal.food_secondary_color, (x + BLOCK_SIZE // 2, y + 6), (x + BLOCK_SIZE - 3, y + 2), 2)

        elif food_type == "meat":
            # Steak meat slab
            meat_rect = pygame.Rect(x + 2, y + 3, BLOCK_SIZE - 7, BLOCK_SIZE - 6)
            pygame.draw.ellipse(surface, animal.food_color, meat_rect)
            inner_rect = pygame.Rect(x + 5, y + 6, BLOCK_SIZE - 13, BLOCK_SIZE - 12)
            pygame.draw.ellipse(surface, (230, 90, 90), inner_rect)
            # Bone extending outward
            bone_col = animal.food_secondary_color
            pygame.draw.rect(surface, bone_col, (x + BLOCK_SIZE - 8, y + BLOCK_SIZE // 2 - 2, 6, 4))
            pygame.draw.circle(surface, bone_col, (x + BLOCK_SIZE - 2, y + BLOCK_SIZE // 2 - 2), 2)
            pygame.draw.circle(surface, bone_col, (x + BLOCK_SIZE - 2, y + BLOCK_SIZE // 2 + 2), 2)

        elif food_type == "sugarcane":
            # Sugar cane / bamboo stalk
            stalk_rect = pygame.Rect(x + 6, y + 1, BLOCK_SIZE - 12, BLOCK_SIZE - 2)
            pygame.draw.rect(surface, animal.food_color, stalk_rect, border_radius=2)
            # Bamboo stalk rings
            ring_col = animal.food_secondary_color
            pygame.draw.line(surface, ring_col, (x + 5, y + 7), (x + BLOCK_SIZE - 5, y + 7), 2)
            pygame.draw.line(surface, ring_col, (x + 5, y + 13), (x + BLOCK_SIZE - 5, y + 13), 2)
            # Leaf sprout
            pygame.draw.line(surface, (90, 220, 90), (x + BLOCK_SIZE - 6, y + 7), (x + BLOCK_SIZE - 1, y + 3), 2)

        elif food_type == "banana":
            # Yellow curved banana arc
            pygame.draw.arc(surface, animal.food_color, (x + 1, y + 2, BLOCK_SIZE - 2, BLOCK_SIZE - 2), 3.8, 6.1, 5)
            # Stem and tip
            stem_col = animal.food_secondary_color
            pygame.draw.rect(surface, stem_col, (x + BLOCK_SIZE - 6, y + 2, 3, 3))
            pygame.draw.rect(surface, stem_col, (x + 3, y + BLOCK_SIZE - 6, 3, 2))

        elif food_type == "fish":
            # Fish body
            body_rect = pygame.Rect(x + 2, y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8)
            pygame.draw.ellipse(surface, animal.food_color, body_rect)
            # Tail fin
            tail_pts = [
                (x + BLOCK_SIZE - 7, y + BLOCK_SIZE // 2),
                (x + BLOCK_SIZE - 2, y + 3),
                (x + BLOCK_SIZE - 2, y + BLOCK_SIZE - 3),
            ]
            pygame.draw.polygon(surface, animal.food_secondary_color, tail_pts)
            # Eye
            pygame.draw.circle(surface, (255, 255, 255), (x + 5, y + BLOCK_SIZE // 2 - 1), 2)
            pygame.draw.circle(surface, (0, 0, 0), (x + 5, y + BLOCK_SIZE // 2 - 1), 1)

        else:  # Default apple
            # Apple round body
            pygame.draw.circle(surface, animal.food_color, (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2 + 1), BLOCK_SIZE // 2 - 2)
            # Stem
            pygame.draw.line(surface, (110, 70, 30), (x + BLOCK_SIZE // 2, y + 5), (x + BLOCK_SIZE // 2, y + 1), 2)
            # Green leaf
            pygame.draw.circle(surface, animal.food_secondary_color, (x + BLOCK_SIZE // 2 + 3, y + 3), 2)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the current food on the specified surface."""
        self.draw_food_icon(surface, self.position[0], self.position[1], self.animal)
