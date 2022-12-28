import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

# Initialize pygame
pygame.init()
# Initialize the mixer
pygame.mixer.init()
# Initialize the font module
pygame.font.init()

# Define a font
font = pygame.font.Font(None, 36)

# Load the music file
pygame.mixer.music.load("../music/music.mp3")

# Play the music
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load the sound file
sound = pygame.mixer.Sound("../music/eat.wav")


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


# Map key presses to directions
DIRECTION_MAP = {
    pygame.K_UP: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT
}

Point = namedtuple('Point', 'x, y')

# Snake dimensions
SNAKE_BLOCK = 20
SNAKE_SPEED = 40

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class SnakeGameAI:
    # Set the dimensions of the screen to be larger than the playing field by default
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    apple_pos = None
    frame_iteration = None
    score = None
    snake = None
    head = None
    paused = None
    direction = None

    # Define the dimensions of the playing field
    # PLAYING_FIELD_WIDTH = 600
    # PLAYING_FIELD_HEIGHT = 600

    def __init__(self, w=SCREEN_WIDTH, h=SCREEN_HEIGHT, td_width=200):

        self.w = w
        self.h = h
        self.text_display_width = td_width

        self.playing_field_w = self.w - self.text_display_width if self.w - self.text_display_width > 0 else 0
        self.playing_field_h = self.h

        # Set up the display
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")

        # Create a surface for the playing field
        self.playing_field = pygame.Surface((self.playing_field_w, self.playing_field_h))

        # Create a surface for the text display
        self.text_display = pygame.Surface((self.text_display_width, self.h))

        # Load the images
        self._load_images()

        # Set up the clock
        self.clock = pygame.time.Clock()

        self.reset()

    def _load_images(self):
        self.head_up_image = pygame.transform.scale(pygame.image.load("../Graphics/head_up.png"),
                                                    (SNAKE_BLOCK, SNAKE_BLOCK))
        self.head_down_image = pygame.transform.scale(pygame.image.load("../Graphics/head_down.png"),
                                                      (SNAKE_BLOCK, SNAKE_BLOCK))
        self.head_left_image = pygame.transform.scale(pygame.image.load("../Graphics/head_left.png"),
                                                      (SNAKE_BLOCK, SNAKE_BLOCK))
        self.head_right_image = pygame.transform.scale(pygame.image.load("../Graphics/head_right.png"),
                                                       (SNAKE_BLOCK, SNAKE_BLOCK))
        self.body_horizontal_image = pygame.transform.scale(pygame.image.load("../Graphics/body_horizontal.png"),
                                                            (SNAKE_BLOCK, SNAKE_BLOCK))
        self.body_vertical_image = pygame.transform.scale(pygame.image.load("../Graphics/body_vertical.png"),
                                                          (SNAKE_BLOCK, SNAKE_BLOCK))
        self.body_topleft_image = pygame.transform.scale(pygame.image.load("../Graphics/body_topleft.png"),
                                                         (SNAKE_BLOCK, SNAKE_BLOCK))
        self.body_topright_image = pygame.transform.scale(pygame.image.load("../Graphics/body_topright.png"),
                                                          (SNAKE_BLOCK, SNAKE_BLOCK))
        self.body_bottomleft_image = pygame.transform.scale(pygame.image.load("../Graphics/body_bottomleft.png"),
                                                            (SNAKE_BLOCK, SNAKE_BLOCK))
        self.body_bottomright_image = pygame.transform.scale(pygame.image.load("../Graphics/body_bottomright.png"),
                                                             (SNAKE_BLOCK, SNAKE_BLOCK))
        self.tail_up_image = pygame.transform.scale(pygame.image.load("../Graphics/tail_up.png"),
                                                    (SNAKE_BLOCK, SNAKE_BLOCK))
        self.tail_down_image = pygame.transform.scale(pygame.image.load("../Graphics/tail_down.png"),
                                                      (SNAKE_BLOCK, SNAKE_BLOCK))
        self.tail_left_image = pygame.transform.scale(pygame.image.load("../Graphics/tail_left.png"),
                                                      (SNAKE_BLOCK, SNAKE_BLOCK))
        self.tail_right_image = pygame.transform.scale(pygame.image.load("../Graphics/tail_right.png"),
                                                       (SNAKE_BLOCK, SNAKE_BLOCK))

        self.apple = pygame.transform.scale(pygame.image.load("../Graphics/apple.png"), (SNAKE_BLOCK, SNAKE_BLOCK))

    def reset(self):
        # Initialize the direction
        self.direction = Direction.RIGHT
        # change_to = self.direction

        # Initialize the paused flag
        self.paused = False

        # Initialize the food eaten counter
        # self.food_eaten = 0

        # Initialize the snake
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - SNAKE_BLOCK, self.head.y),
                      Point(self.head.x - (2 * SNAKE_BLOCK), self.head.y)]

        # Initialize the score and frame iteration counter
        self.score = 0
        self.frame_iteration = 0

        apple_pos_x, apple_pos_y = self.generate_new_apple_pos(self.snake,
                                                               self.playing_field_w,
                                                               self.playing_field_h,
                                                               SNAKE_BLOCK)
        self.apple_pos = Point(apple_pos_x, apple_pos_y)

    @staticmethod
    def is_apple_overlapping(apple_position, snake):
        """Returns True if the apple position overlaps with the snake's body, False otherwise."""
        for block in snake:
            if block == apple_position:
                return True
        return False

    def generate_new_apple_pos(self, snake, width, height, block_size):
        """Generates a new random apple position that doesn't overlap with the snake's body."""
        while True:
            pos = (random.randint(0, width - block_size) // block_size * block_size,
                   random.randint(0, height - block_size) // block_size * block_size)
            if not self.is_apple_overlapping(pos, snake):
                return pos

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.apple_pos:
            sound.play()
            self.score += 1
            reward = 10
            apple_pos_x, apple_pos_y = self.generate_new_apple_pos(self.snake,
                                                                   self.playing_field_w,
                                                                   self.playing_field_h,
                                                                   SNAKE_BLOCK)
            self.apple_pos = Point(apple_pos_x, apple_pos_y)
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        # Tick the clock
        self.clock.tick(SNAKE_SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    def _move(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir
        change_to = self.direction
        # Make sure the snake cannot move in the opposite direction instantaneously
        if change_to == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif change_to == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        elif change_to == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif change_to == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += SNAKE_BLOCK
        elif self.direction == Direction.LEFT:
            x -= SNAKE_BLOCK
        elif self.direction == Direction.DOWN:
            y += SNAKE_BLOCK
        elif self.direction == Direction.UP:
            y -= SNAKE_BLOCK

        self.head = Point(x, y)
        self.snake.insert(0, self.head)

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
            # hits boundary
        if pt.x > self.playing_field_w - SNAKE_BLOCK or pt.x < 0 or pt.y > self.playing_field_h - SNAKE_BLOCK or pt.y < 0:
            return True
            # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        # Draw the playing field
        self.playing_field.fill(BLACK)
        for i, block in enumerate(self.snake):
            # Draw the head
            if i == 0:
                if self.direction == Direction.UP:
                    self.playing_field.blit(self.head_up_image, block)
                elif self.direction == Direction.DOWN:
                    self.playing_field.blit(self.head_down_image, block)
                elif self.direction == Direction.LEFT:
                    self.playing_field.blit(self.head_left_image, block)
                elif self.direction == Direction.RIGHT:
                    self.playing_field.blit(self.head_right_image, block)
            # Draw the body
            elif 0 < i < len(self.snake) - 1:
                # Get the previous and next blocks
                prev_block = self.snake[i - 1]
                next_block = self.snake[i + 1]
                if prev_block.y == block.y and next_block.y == block.y:
                    # The snake is moving horizontally
                    self.playing_field.blit(self.body_horizontal_image, block)
                elif prev_block.x == block.x and next_block.x == block.x:
                    # The snake is moving vertically
                    self.playing_field.blit(self.body_vertical_image, block)
                elif prev_block.x < block.x and next_block.y < block.y:
                    # The snake is turning from the left to up
                    self.playing_field.blit(self.body_topleft_image, block)
                elif prev_block.x < block.x and next_block.y > block.y:
                    # The snake is turning from the left to down
                    self.playing_field.blit(self.body_bottomleft_image, block)
                elif prev_block.x > block.x and next_block.y < block.y:
                    # The snake is turning from the right to up
                    self.playing_field.blit(self.body_topright_image, block)
                elif prev_block.x > block.x and next_block.y > block.y:
                    # The snake is turning from the right to down
                    self.playing_field.blit(self.body_bottomright_image, block)
                elif prev_block.y < block.y and next_block.x < block.x:
                    # The snake is turning from the left to up
                    self.playing_field.blit(self.body_topleft_image, block)
                elif prev_block.y < block.y and next_block.x > block.x:
                    # The snake is turning from the right to up
                    self.playing_field.blit(self.body_topright_image, block)
                elif prev_block.y > block.y and next_block.x < block.x:
                    # The snake is turning from the left to down
                    self.playing_field.blit(self.body_bottomleft_image, block)
                elif prev_block.y > block.y and next_block.x > block.x:
                    # The snake is turning from the right to down
                    self.playing_field.blit(self.body_bottomright_image, block)
            # Draw the tail
            elif i == len(self.snake) - 1:
                # Get the previous block
                prev_block = self.snake[i - 1]
                # Check if the last element in the snake list is the tail
                if prev_block.y == block.y and prev_block.x > block.x:
                    # The snake is moving left
                    self.playing_field.blit(self.tail_left_image, block)
                elif prev_block.y == block.y and prev_block.x < block.x:
                    # The snake is moving right
                    self.playing_field.blit(self.tail_right_image, block)
                elif prev_block.y < block.y and prev_block.x == block.x:
                    # The snake is moving down
                    self.playing_field.blit(self.tail_down_image, block)
                else:
                    # The snake is moving up
                    self.playing_field.blit(self.tail_up_image, block)

        self.playing_field.blit(self.apple, self.apple_pos)

        # Render the text
        text = font.render(" Score: {}".format(self.score), True, WHITE)

        # Get the text rectangle
        text_rect = text.get_rect()

        # Draw the text display
        self.text_display.fill(BLACK)
        self.text_display.blit(text, text_rect)

        # Draw the line
        pygame.draw.line(self.screen, WHITE, (self.playing_field_w, 0), (self.playing_field_w, self.h), 2)

        # Draw the playing field and the text display on the screen
        self.screen.blit(self.playing_field, (0, 0))
        self.screen.blit(self.text_display, (self.playing_field_w, 0))

        # Update the display
        pygame.display.update()
