import pygame
import sys
import random


CELL_SIZE = 20          
GRID_WIDTH = 30       
GRID_HEIGHT = 20        
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10                


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 180, 0)
RED = (200, 30, 30)
YELLOW = (240, 200, 0)


def random_food_position(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def draw_rect(surface, color, pos):
    rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)

def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, DARK_GRAY, (0, y), (SCREEN_WIDTH, y))


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 56)
        self.reset()

    def reset(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.snake = [(start_x - 2, start_y), (start_x - 1, start_y), (start_x, start_y)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.food = random_food_position(self.snake)
        self.score = 0
        self.game_over = False
        self.speed = FPS

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_r,) and self.game_over:
                    self.reset()
                elif event.key in (pygame.K_UP, pygame.K_w) and self.direction != (0, 1):
                    self.next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and self.direction != (0, -1):
                    self.next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and self.direction != (1, 0):
                    self.next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.direction != (-1, 0):
                    self.next_direction = (1, 0)

    def update(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[-1]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.append(new_head)

        if new_head == self.food:
            self.score += 1
            self.speed = min(25, FPS + self.score // 3)
            self.food = random_food_position(self.snake)
        else:
            self.snake.pop(0)

    def draw(self):
        self.screen.fill(BLACK)
        draw_grid(self.screen)
        draw_rect(self.screen, RED, self.food)
        for segment in self.snake[:-1]:
            draw_rect(self.screen, GREEN, segment)
        draw_rect(self.screen, YELLOW, self.snake[-1])

        score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surf, (8, 8))

        if self.game_over:
            go_text = self.big_font.render("GAME OVER", True, RED)
            instr = self.font.render("Press R to restart or Esc to quit", True, WHITE)
            rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            rect2 = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            self.screen.blit(go_text, rect)
            self.screen.blit(instr, rect2)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.speed)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()