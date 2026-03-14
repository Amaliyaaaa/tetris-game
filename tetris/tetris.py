#tetris
import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
REDISH = (255, 30, 10)

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
]

# Initialize game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

def draw_block(x, y):
    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_shape(shape, offset):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                draw_block(col + offset[0], row + offset[1])

def draw_board(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 1:
                draw_block(col, row)

def check_collision(board, shape, offset):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                # Print statements to debug
                #print(f"Checking board[{row + offset[1]}][{col + offset[0]}]")
                #print(f"Current board dimensions: {len(board)} rows x {len(board[0])} columns")

                if (
                    row + offset[1] < 0
                    or row + offset[1] >= len(board)
                    or col + offset[0] < 0
                    or col + offset[0] >= len(board[0])
                    or board[row + offset[1]][col + offset[0]] == 1
                ):
                    #print("Collision detected!")
                    return True
    return False


def merge_shape(board, shape, offset):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                board[row + offset[1]][col + offset[0]] = 1

def rotate_shape(shape):
    return [list(row) for row in zip(*reversed(shape))]

def clear_lines(board):
    lines_to_clear = [i for i, row in enumerate(board) if all(cell == 1 for cell in row)]
    for line in lines_to_clear:
        del board[line]
        board.insert(0, [0] * len(board[0]))

def display_game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, REDISH)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Display the message for 2000 milliseconds (2 seconds)


def main():
    board = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
    current_shape = random.choice(SHAPES)

    # Set the initial position to the middle at the top
    shape_offset = [(WIDTH // BLOCK_SIZE - len(current_shape[0])) // 2, 0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(board, current_shape, [shape_offset[0] - 1, shape_offset[1]]):
                    shape_offset[0] -= 1
                elif event.key == pygame.K_RIGHT and not check_collision(board, current_shape, [shape_offset[0] + 1, shape_offset[1]]):
                    shape_offset[0] += 1
                elif event.key == pygame.K_DOWN and not check_collision(board, current_shape, [shape_offset[0], shape_offset[1] + 1]):
                    shape_offset[1] += 1
                elif event.key == pygame.K_UP:
                    rotated_shape = rotate_shape(current_shape)
                    if not check_collision(board, rotated_shape, shape_offset):
                        current_shape = rotated_shape

        if not check_collision(board, current_shape, [shape_offset[0], shape_offset[1] + 1]):
            shape_offset[1] += 1
        else:
            merge_shape(board, current_shape, shape_offset)
            clear_lines(board)
            current_shape = random.choice(SHAPES)
            shape_offset = [(WIDTH // BLOCK_SIZE - len(current_shape[0])) // 2, 0]

        if shape_offset[1] == 0 and check_collision(board, current_shape, shape_offset):
            display_game_over()
            pygame.quit()
            quit()

        screen.fill(BLACK)
        draw_board(board)
        draw_shape(current_shape, shape_offset)  # Draw the entire shape
        pygame.display.flip()
        clock.tick(3)  # Adjust the speed of the game

if __name__ == "__main__":
    main()
