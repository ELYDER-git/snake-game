import pygame, sys, random
from pygame.math import Vector2

pygame.init()
cell_number = 15
cell_size = 40
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('/home/lakshya-t/snake-game/Graphics/apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (cell_size, cell_size))
game_font = pygame.font.Font('/home/lakshya-t/snake-game/Font/SIXTY.TTF', 25)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)

        self.head_down = pygame.image.load('/home/lakshya-t/snake-game/Graphics/head_down.png').convert_alpha()
        self.head_up = pygame.image.load('/home/lakshya-t/snake-game/Graphics/head_up.png').convert_alpha()
        self.head_right = pygame.image.load('/home/lakshya-t/snake-game/Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('/home/lakshya-t/snake-game/Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('/home/lakshya-t/snake-game/Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('/home/lakshya-t/snake-game/Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('/home/lakshya-t/snake-game/Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('/home/lakshya-t/snake-game/Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('/home/lakshya-t/snake-game/Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('/home/lakshya-t/snake-game/Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('/home/lakshya-t/snake-game/Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('/home/lakshya-t/snake-game/Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('/home/lakshya-t/snake-game/Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('/home/lakshya-t/snake-game/Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
    
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                head_relation = self.body[1] - self.body[0]
                if self.direction == Vector2(1, 0):
                    screen.blit(self.head_right, block_rect)
                elif self.direction == Vector2(-1, 0):
                    screen.blit(self.head_left, block_rect)
                elif self.direction == Vector2(0, 1):
                    screen.blit(self.head_down, block_rect)
                elif self.direction == Vector2(0, -1):
                    screen.blit(self.head_up, block_rect)

            elif index == len(self.body) - 1:
                tail_relation = self.body[-2] - self.body[-1]
                if tail_relation == Vector2(-1, 0):
                    screen.blit(self.tail_right, block_rect)
                elif tail_relation == Vector2(1, 0):
                    screen.blit(self.tail_left, block_rect)
                elif tail_relation == Vector2(0, -1):
                    screen.blit(self.tail_down, block_rect)
                elif tail_relation == Vector2(0, 1):
                    screen.blit(self.tail_up, block_rect)

            elif 0 < index < len(self.body) - 1:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

class FRUIT:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        #pygame.draw.rect(screen, pygame.Color((117, 48, 4)), fruit_rect)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.body.append(self.snake.body[-1])

    def game_over(self):
            pygame.quit()
            sys.exit()
            
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                  main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                  main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                  main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                  main_game.snake.direction = Vector2(1, 0)

    screen.fill((250, 226, 0))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)