# Classic Snake Game 🐍
import random
import time
import os
import sys

# Platform-specific imports for non-blocking keyboard input
if sys.platform == "win32":
    import msvcrt
else:
    import tty
    import termios

# --- Game Constants ---
WIDTH = 20
HEIGHT = 15
SPEED = 0.2  # Lower is faster

def setup_terminal():
    """Hides the cursor."""
    if os.name == 'nt': # For Windows
        os.system('cls')
    else: # For macOS and Linux
        os.system('clear')
    # Hide cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def restore_terminal():
    """Restores the cursor."""
    # Show cursor
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def get_key():
    """Gets a single character from standard input, without blocking."""
    if sys.platform == "win32":
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8').lower()
    else:
        # Set terminal to raw mode to capture single key presses
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            # Check if there is input to be read
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

def draw_board(snake, food, score):
    """Draws the game board, snake, food, and score."""
    # Move cursor to top-left corner
    sys.stdout.write("\033[H")
    
    print("SNAKE GAME 🐍".center(WIDTH * 2))
    print(f"Score: {score}".center(WIDTH * 2))
    print("+" + "-" * (WIDTH * 2) + "+")

    for y in range(HEIGHT):
        line = "|"
        for x in range(WIDTH):
            if (x, y) == snake[0]:
                line += "@@"  # Snake head
            elif (x, y) in snake:
                line += "oo"  # Snake body
            elif (x, y) == food:
                line += "🍎"  # Food
            else:
                line += "  "
        line += "|"
        print(line)

    print("+" + "-" * (WIDTH * 2) + "+")
    print("Controls: W (Up), A (Left), S (Down), D (Right), Q (Quit)".center(WIDTH * 2))

def play_game():
    """Runs one round of the Snake game and returns the final score."""
    # --- Game State ---
    snake = [(WIDTH // 2, HEIGHT // 2)]
    food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
    direction = (1, 0)  # Start by moving right
    score = 0

    while True:
        # --- Handle Input ---
        key = get_key()
        if key == 'q':
            break
        elif key == 'w' and direction != (0, 1): direction = (0, -1)
        elif key == 's' and direction != (0, -1): direction = (0, 1)
        elif key == 'a' and direction != (1, 0): direction = (-1, 0)
        elif key == 'd' and direction != (-1, 0): direction = (1, 0)

        # --- Update Game Logic ---
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check for collisions (wall or self)
        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake):
            break # Game over

        snake.insert(0, head)

        # Check for food
        if head == food:
            score += 10
            food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        else:
            snake.pop()

        # --- Draw Frame ---
        draw_board(snake, food, score)
        time.sleep(SPEED)
    
    return score

def main():
    """Main entry point, handles playing multiple games."""
    while True:
        setup_terminal()
        try:
            score = play_game()
        finally:
            restore_terminal() # Ensure terminal is always restored

        print(f"\nGAME OVER! Final Score: {score}\n")
        if input("Play again? (y/n): ").lower() != 'y':
            break

if __name__ == '__main__':
    main()
