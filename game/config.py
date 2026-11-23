from dataclasses import dataclass


SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
BLOCK_SIZE: int = 20
FPS: int = 60

INITIAL_SNAKE_SPEED: int = 10

COLOR_BLACK: tuple[int, int, int] = (15, 15, 20)
COLOR_WHITE: tuple[int, int, int] = (255, 255, 255)
COLOR_RED: tuple[int, int, int] = (255, 60, 60)
COLOR_GREEN: tuple[int, int, int] = (50, 205, 50)
COLOR_GOLD: tuple[int, int, int] = (255, 215, 0)
COLOR_GRAY: tuple[int, int, int] = (120, 125, 140)
COLOR_DARK_GRAY: tuple[int, int, int] = (35, 40, 50)
COLOR_PANEL_BG: tuple[int, int, int] = (25, 30, 42)
COLOR_PANEL_SELECTED: tuple[int, int, int] = (45, 55, 75)

BACKGROUND_COLOR: tuple[int, int, int] = COLOR_BLACK
SNAKE_COLOR: tuple[int, int, int] = COLOR_GREEN
FOOD_COLOR: tuple[int, int, int] = COLOR_RED


@dataclass
class AnimalConfig:
    """Configuration for an animal character and its favorite food."""
    id: str
    name: str
    food_name: str
    food_type: str
    body_color: tuple[int, int, int]
    head_color: tuple[int, int, int]
    accent_color: tuple[int, int, int]
    food_color: tuple[int, int, int]
    food_secondary_color: tuple[int, int, int]
    emoji: str
    food_emoji: str
    description: str


ANIMALS: list[AnimalConfig] = [
    AnimalConfig(
        id="rabbit",
        name="Rabbit",
        food_name="Carrot",
        food_type="carrot",
        body_color=(235, 235, 240),
        head_color=(250, 250, 255),
        accent_color=(255, 170, 190),  # Pink ears/nose
        food_color=(255, 125, 20),     # Carrot orange
        food_secondary_color=(45, 185, 45), # Leafy green
        emoji="🐰",
        food_emoji="🥕",
        description="Fast & fluffy! Loves crunchy orange carrots.",
    ),
    AnimalConfig(
        id="tiger",
        name="Tiger",
        food_name="Meat",
        food_type="meat",
        body_color=(245, 130, 25),     # Tiger orange
        head_color=(255, 145, 35),
        accent_color=(35, 30, 30),     # Dark stripes
        food_color=(195, 45, 45),      # Meat red
        food_secondary_color=(245, 240, 230), # Bone white
        emoji="🐯",
        food_emoji="🥩",
        description="Fierce hunter! Craves juicy meat chunks.",
    ),
    AnimalConfig(
        id="panda",
        name="Panda",
        food_name="Sugar Cane",
        food_type="sugarcane",
        body_color=(245, 245, 245),    # White
        head_color=(255, 255, 255),
        accent_color=(30, 30, 35),     # Black patches & ears
        food_color=(60, 185, 65),      # Sugar cane green
        food_secondary_color=(165, 230, 125), # Stalk nodes
        emoji="🐼",
        food_emoji="🎋",
        description="Chubby & sweet! Munches fresh sugar cane.",
    ),
    AnimalConfig(
        id="monkey",
        name="Monkey",
        food_name="Banana",
        food_type="banana",
        body_color=(140, 85, 45),      # Brown
        head_color=(165, 105, 55),
        accent_color=(235, 195, 155),  # Peach face
        food_color=(255, 220, 25),     # Banana yellow
        food_secondary_color=(110, 75, 25), # Stem brown
        emoji="🐵",
        food_emoji="🍌",
        description="Playful acrobat! Crazy about sweet bananas.",
    ),
    AnimalConfig(
        id="penguin",
        name="Penguin",
        food_name="Fish",
        food_type="fish",
        body_color=(30, 40, 55),       # Deep navy black
        head_color=(25, 35, 50),
        accent_color=(255, 160, 20),   # Orange beak
        food_color=(75, 160, 235),     # Fish blue
        food_secondary_color=(195, 225, 255), # Light fins
        emoji="🐧",
        food_emoji="🐟",
        description="Waddles on ice! Catches tasty fish.",
    ),
    AnimalConfig(
        id="snake",
        name="Snake",
        food_name="Apple",
        food_type="apple",
        body_color=(35, 185, 70),      # Emerald green
        head_color=(45, 215, 85),
        accent_color=(230, 40, 40),    # Red tongue
        food_color=(225, 35, 35),      # Red apple
        food_secondary_color=(50, 180, 40), # Green leaf
        emoji="🐍",
        food_emoji="🍎",
        description="Classic crawler! Slithers for crisp red apples.",
    ),
]
