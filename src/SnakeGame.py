import pygame
import random

# Initialize pygame
pygame.init()
# Initialize the mixer
pygame.mixer.init()
# Initialize the font module
pygame.font.init()

# Set the dimensions of the screen to be larger than the playing field
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Define the dimensions of the playing field
PLAYING_FIELD_WIDTH = 600
PLAYING_FIELD_HEIGHT = 600

# Create a surface for the playing field
playing_field = pygame.Surface((PLAYING_FIELD_WIDTH, PLAYING_FIELD_HEIGHT))

# Create a surface for the text display
text_display = pygame.Surface((SCREEN_WIDTH - PLAYING_FIELD_WIDTH, SCREEN_HEIGHT))

# Snake dimensions
SNAKE_BLOCK = 20
SNAKE_SPEED = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Define a font
font = pygame.font.Font(None, 36)

# Load the music file
pygame.mixer.music.load("music/music.mp3")

# Play the music
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load the sound file
sound = pygame.mixer.Sound("music/eat.wav")

# Load the snake images
head_up_image = pygame.transform.scale(pygame.image.load("Graphics/head_up.png"), (SNAKE_BLOCK, SNAKE_BLOCK))
head_down_image = pygame.transform.scale(pygame.image.load("Graphics/head_down.png"), (SNAKE_BLOCK, SNAKE_BLOCK))
head_left_image = pygame.transform.scale(pygame.image.load("Graphics/head_left.png"), (SNAKE_BLOCK, SNAKE_BLOCK))
head_right_image = pygame.transform.scale(pygame.image.load("Graphics/head_right.png"), (SNAKE_BLOCK, SNAKE_BLOCK))
body_horizontal_image = pygame.transform.scale(pygame.image.load("Graphics/body_horizontal.png"),
                                               (SNAKE_BLOCK, SNAKE_BLOCK))
body_vertical_image = pygame.transform.scale(pygame.image.load("Graphics/body_vertical.png"),
                                             (SNAKE_BLOCK, SNAKE_BLOCK))
body_topleft_image = pygame.transform.scale(pygame.image.load("Graphics/body_topleft.png"), (SNAKE_BLOCK, SNAKE_BLOCK))
body_topright_image = pygame.transform.scale(pygame.image.load("Graphics/body_topright.png"),
                                             (SNAKE_BLOCK, SNAKE_BLOCK))
body_bottomleft_image = pygame.transform.scale(pygame.image.load("Graphics/body_bottomleft.png"),
                                               (SNAKE_BLOCK, SNAKE_BLOCK))
body_bottomright_image = pygame.transform.scale(pygame.image.load("Graphics/body_bottomright.png"),
                                                (SNAKE_BLOCK, SNAKE_BLOCK))
tail_up_image = pygame.transform.scale(pygame.image.load("Graphics/tail_up.png"), (SNAKE_BLOCK, SNAKE_BLOCK))
tail_down_image = pygame.transform.scale(pygame.image.load("Graphics/tail_down.png"), (SNAKE_BLOCK, SNAKE_BLOCK))
tail_left_image = pygame.transform.scale(pygame.image.load("Graphics/tail_left.png"), (SNAKE_BLOCK, SNAKE_BLOCK))
tail_right_image = pygame.transform.scale(pygame.image.load("Graphics/tail_right.png"), (SNAKE_BLOCK, SNAKE_BLOCK))

# Set up the clock
clock = pygame.time.Clock()

# Initialize the snake
snake = [(200, 200), (200, 210), (200, 220)]


def is_apple_overlapping(apple_position, snake):
    """Returns True if the apple position overlaps with the snake's body, False otherwise."""
    for block in snake:
        if block == apple_position:
            return True
    return False


def generate_new_apple_pos(snake, width, height, block_size):
    """Generates a new random apple position that doesn't overlap with the snake's body."""
    while True:
        pos = (random.randint(0, width - block_size) // block_size * block_size,
               random.randint(0, height - block_size) // block_size * block_size)
        if not is_apple_overlapping(pos, snake):
            return pos


def start_game():
    # Initialize the apple
    apple_pos = generate_new_apple_pos(snake, PLAYING_FIELD_WIDTH, PLAYING_FIELD_HEIGHT, SNAKE_BLOCK)
    apple = pygame.transform.scale(pygame.image.load("Graphics/apple.png"), (SNAKE_BLOCK, SNAKE_BLOCK))
    # Initialize the food eaten counter
    food_eaten = 0

    # Initialize the direction
    direction = "LEFT"
    change_to = direction

    # Initialize the paused flag
    paused = False

    # Map key presses to directions
    DIRECTION_MAP = {
        pygame.K_UP: "UP",
        pygame.K_DOWN: "DOWN",
        pygame.K_LEFT: "LEFT",
        pygame.K_RIGHT: "RIGHT"
    }

    # Game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # Toggle the paused flag when the spacebar is pressed
                if event.key == pygame.K_SPACE:
                    paused = not paused
                # Check if the key press is in the direction map
                elif event.key in DIRECTION_MAP and not paused:
                    # Set the new direction
                    change_to = DIRECTION_MAP[event.key]

        # Pause the game if the paused flag is set
        if paused:
            pygame.mixer.music.pause()
            paused_text = font.render(" Paused", True, WHITE)
            # Draw the text display
            text_display.fill(BLACK)
            text_display.blit(paused_text, (0, 0))
            screen.blit(text_display, (PLAYING_FIELD_WIDTH, 0))
            # Draw the line
            pygame.draw.line(screen, WHITE, (PLAYING_FIELD_WIDTH, 0), (PLAYING_FIELD_WIDTH, SCREEN_HEIGHT), 2)
            # Update the display
            pygame.display.update()
            continue

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()

        # Make sure the snake cannot move in the opposite direction instantaneously
        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        # Move the snake
        if direction == "UP":
            snake[0] = (snake[0][0], snake[0][1] - SNAKE_BLOCK)
        if direction == "DOWN":
            snake[0] = (snake[0][0], snake[0][1] + SNAKE_BLOCK)
        if direction == "LEFT":
            snake[0] = (snake[0][0] - SNAKE_BLOCK, snake[0][1])
        if direction == "RIGHT":
            snake[0] = (snake[0][0] + SNAKE_BLOCK, snake[0][1])

        # Check if the snake has collided with the boundaries
        if snake[0][0] < 0 or snake[0][0] > PLAYING_FIELD_WIDTH - SNAKE_BLOCK \
                or snake[0][1] < 0 or snake[0][1] > PLAYING_FIELD_HEIGHT - SNAKE_BLOCK:
            pygame.quit()
            exit()

        # Update the snake
        if snake[0] == apple_pos:
            snake.append(snake[-1])
            food_eaten += 1
            sound.play()
            # Generate a new apple position
            apple_pos = generate_new_apple_pos(snake, PLAYING_FIELD_WIDTH, PLAYING_FIELD_HEIGHT, SNAKE_BLOCK)

        # Check if the snake has collided with itself
        if snake[0] in snake[1:]:
            pygame.quit()
            exit()

        # Move the snake body
        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i - 1][0], snake[i - 1][1])

        # Draw the playing field
        playing_field.fill(BLACK)
        for i, block in enumerate(snake):
            # Draw the head
            if i == 0:
                if direction == "UP":
                    playing_field.blit(head_up_image, block)
                elif direction == "DOWN":
                    playing_field.blit(head_down_image, block)
                elif direction == "LEFT":
                    playing_field.blit(head_left_image, block)
                elif direction == "RIGHT":
                    playing_field.blit(head_right_image, block)
            # Draw the body
            elif 1 < i < len(snake) - 1:
                # Get the previous and next blocks
                prev_block = snake[i - 1]
                next_block = snake[i + 1]
                if prev_block[1] == block[1] and next_block[1] == block[1]:
                    # The snake is moving horizontally
                    playing_field.blit(body_horizontal_image, block)
                elif prev_block[0] == block[0] and next_block[0] == block[0]:
                    # The snake is moving vertically
                    playing_field.blit(body_vertical_image, block)
                elif prev_block[0] < block[0] and next_block[1] < block[1]:
                    # The snake is turning from the left to up
                    playing_field.blit(body_topleft_image, block)
                elif prev_block[0] < block[0] and next_block[1] > block[1]:
                    # The snake is turning from the left to down
                    playing_field.blit(body_bottomleft_image, block)
                elif prev_block[0] > block[0] and next_block[1] < block[1]:
                    # The snake is turning from the right to up
                    playing_field.blit(body_topright_image, block)
                elif prev_block[0] > block[0] and next_block[1] > block[1]:
                    # The snake is turning from the right to down
                    playing_field.blit(body_bottomright_image, block)
                elif prev_block[1] < block[1] and next_block[0] < block[0]:
                    # The snake is turning from the left to up
                    playing_field.blit(body_topleft_image, block)
                elif prev_block[1] < block[1] and next_block[0] > block[0]:
                    # The snake is turning from the right to up
                    playing_field.blit(body_topright_image, block)
                elif prev_block[1] > block[1] and next_block[0] < block[0]:
                    # The snake is turning from the left to down
                    playing_field.blit(body_bottomleft_image, block)
                elif prev_block[1] > block[1] and next_block[0] > block[0]:
                    # The snake is turning from the right to down
                    playing_field.blit(body_bottomright_image, block)
            # Draw the tail
            elif i == len(snake) - 1:
                # Get the previous block
                prev_block = snake[i - 1]
                # Check if the last element in the snake list is the tail
                if prev_block[1] == block[1] and prev_block[0] > block[0]:
                    # The snake is moving left
                    playing_field.blit(tail_left_image, block)
                elif prev_block[1] == block[1] and prev_block[0] < block[0]:
                    # The snake is moving right
                    playing_field.blit(tail_right_image, block)
                elif prev_block[1] < block[1] and prev_block[0] == block[0]:
                    # The snake is moving down
                    playing_field.blit(tail_down_image, block)
                else:
                    # The snake is moving up
                    playing_field.blit(tail_up_image, block)

        playing_field.blit(apple, apple_pos)

        # Render the text
        text = font.render(" Food eaten: {}".format(food_eaten), True, WHITE)

        # Get the text rectangle
        text_rect = text.get_rect()

        # Draw the text display
        text_display.fill(BLACK)
        text_display.blit(text, text_rect)

        # Draw the playing field and the text display on the screen
        screen.blit(playing_field, (0, 0))
        screen.blit(text_display, (PLAYING_FIELD_WIDTH, 0))

        # Draw the line
        pygame.draw.line(screen, WHITE, (PLAYING_FIELD_WIDTH, 0), (PLAYING_FIELD_WIDTH, SCREEN_HEIGHT), 2)

        # Update the display
        pygame.display.update()

        # Tick the clock
        clock.tick(SNAKE_SPEED)


def display_start_screen():
    # Set the background color to white
    screen.fill(WHITE)

    # Create a start game button
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50)
    pygame.draw.rect(screen, GREEN, start_button)

    # Create a font for the button text
    button_font = pygame.font.Font(None, 36)

    # Render the text for the start button
    start_text = button_font.render("Start", True, BLACK)

    # Get the size of the start text
    start_text_rect = start_text.get_rect()

    # Center the start text on the button
    start_text_rect.center = start_button.center

    # Draw the start text to the screen
    screen.blit(start_text, start_text_rect)

    # Update the display
    pygame.display.update()

    # Wait for the user to click the start button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked the start button
                if start_button.collidepoint(event.pos):
                    # Start the game
                    start_game()
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == '__main__':
    display_start_screen()
