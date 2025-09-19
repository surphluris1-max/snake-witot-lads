from nicegui import ui, app
import random
from collections import deque

# --- Game Constants ---
WIDTH = 20
HEIGHT = 15
SPEED_MS = 200  # Milliseconds between updates

# --- Game State ---
# We use a deque for efficient appends and pops from both ends
snake = deque([(WIDTH // 2, HEIGHT // 2)])
food = (-1, -1)  # Initial dummy position
direction = (1, 0)  # (dx, dy) - Start moving right
score = 0
game_over = True  # Start in a "game over" state

def generate_food():
    """Generates a new food item at a position not occupied by the snake."""
    global food
    while True:
        new_food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        if new_food not in snake:
            food = new_food
            break

def restart_game():
    """Resets the game to its initial state."""
    global snake, direction, score, game_over
    snake = deque([(WIDTH // 2, HEIGHT // 2)])
    direction = (1, 0)
    score = 0
    game_over = False
    score_label.set_text(f'Score: {score}')
    generate_food()
    game_board.refresh()
    ui.notify('Game Started!', position='center', color='positive')

def update_game_state():
    """The main game loop logic, called by a timer."""
    if game_over:
        return

    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # Collision detection (wall or self)
    if (head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT or
        head in snake):
        global game_over
        game_over = True
        ui.notify(f'Game Over! Final Score: {score}', position='center', type='negative', multi_line=True)
        game_board.refresh()
        return

    snake.appendleft(head)

    # Food consumption
    if head == food:
        global score
        score += 10
        score_label.set_text(f'Score: {score}')
        generate_food()
    else:
        snake.pop()

    game_board.refresh()

def handle_key(e: ui.keyboard_key):
    """Handles keyboard input for desktop players."""
    global direction
    if game_over or not e.action.keydown:
        return

    if e.key.name == 'ArrowUp' and direction != (0, 1): direction = (0, -1)
    elif e.key.name == 'ArrowDown' and direction != (0, -1): direction = (0, 1)
    elif e.key.name == 'ArrowLeft' and direction != (1, 0): direction = (-1, 0)
    elif e.key.name == 'ArrowRight' and direction != (-1, 0): direction = (1, 0)

def set_direction(new_direction):
    """Handles button clicks for mobile players."""
    global direction
    # Prevent moving directly backward
    if (direction[0] == -new_direction[0] and direction[1] == -new_direction[1]):
        return
    direction = new_direction

# --- UI Definition ---
app.native.start_args['debug'] = False
ui.query('body').style('background-color: #222')
ui.keyboard(on_key=handle_key)

with ui.column().classes('w-full items-center'):
    ui.label('SNAKE GAME 🐍').classes('text-3xl text-white mt-4')
    score_label = ui.label(f'Score: {score}').classes('text-2xl text-white')

    @ui.refreshable
    def game_board():
        """Renders the game board. @ui.refreshable allows targeted updates."""
        with ui.grid(columns=WIDTH).classes('gap-0.5 mt-4 border-2 border-gray-600 p-1'):
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    pos = (x, y)
                    color = 'bg-gray-800'  # Empty cell
                    if pos == food: color = 'bg-red-500'
                    if pos in snake: color = 'bg-green-600'
                    if snake and pos == snake[0]: color = 'bg-green-400'
                    ui.label().classes(f'w-4 h-4 {color} rounded-sm')
        if game_over:
            with ui.column().classes('absolute-center items-center'):
                ui.button('Play Game', on_click=restart_game, color='positive')

    game_board() # Initial rendering

    # On-screen controls for mobile
    with ui.row().classes('mt-4'):
        ui.button(icon='arrow_left', on_click=lambda: set_direction((-1, 0))).props('round')
        with ui.column():
            ui.button(icon='arrow_upward', on_click=lambda: set_direction((0, -1))).props('round')
            ui.button(icon='arrow_downward', on_click=lambda: set_direction((0, 1))).props('round')
        ui.button(icon='arrow_right', on_click=lambda: set_direction((1, 0))).props('round')

# Initialize the game state and start the game loop timer
generate_food()
ui.timer(SPEED_MS, update_game_state)

ui.run(title='Python Snake', dark=True, reload=False)
