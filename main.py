import sys
import traceback
import pygame
from game.engine import GameEngine

def run_game() -> None:
    """Initializes pygame, creates the game engine, and runs the main loop."""
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Animal Feast - Snake Game")
    
    try:
        engine = GameEngine()
        
        while engine.is_running:
            engine.handle_input()
            engine.update()
            engine.draw()
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    run_game()