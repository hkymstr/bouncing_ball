import pygame
import sys
import random
import time


def initialize_game():
    """Initialize pygame and create the game window"""
    pygame.init()
    pygame.display.init()

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball Game")
    return screen


# Constants
WIDTH = 800
HEIGHT = 600
BALL_SIZE = 20
CURSOR_SIZE = 50
BALL_SPEED = 5
CURSOR_SPEED = 7
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Ball:
    def __init__(self):
        self.radius = BALL_SIZE // 2
        # Start at a random x position at the top of the screen
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = self.radius  # Start at top of screen (accounting for radius)
        # Make the ball always start moving downward, with random horizontal direction
        self.dx = random.choice([-1, 1]) * BALL_SPEED
        self.dy = BALL_SPEED  # Always start moving down

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.dx *= -1
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)


class Cursor:
    def __init__(self):
        self.width = CURSOR_SIZE
        self.height = CURSOR_SIZE
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT // 2 - self.height // 2
        self.speed = CURSOR_SPEED

    def move(self):
        keys = pygame.key.get_pressed()

        # More responsive movement with direct key state checking
        if keys[pygame.K_LEFT]:
            self.x = max(0, self.x - self.speed)
        if keys[pygame.K_RIGHT]:
            self.x = min(WIDTH - self.width, self.x + self.speed)
        if keys[pygame.K_UP]:
            self.y = max(0, self.y - self.speed)
        if keys[pygame.K_DOWN]:
            self.y = min(HEIGHT - self.height, self.y + self.speed)

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))


def check_collision(ball, cursor):
    cursor_rect = pygame.Rect(cursor.x, cursor.y, cursor.width, cursor.height)
    ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius,
                            ball.radius * 2, ball.radius * 2)
    return cursor_rect.colliderect(ball_rect)


def main():
    try:
        # Initialize the game
        screen = initialize_game()
        clock = pygame.time.Clock()

        # Create game objects
        ball = Ball()
        cursor = Cursor()
        start_time = time.time()
        font = pygame.font.Font(None, 36)
        game_over = False
        final_score = 0

        print("Game initialized successfully!")  # Debug print

        # Game loop
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif game_over and event.key == pygame.K_r:
                        # Reset game
                        ball = Ball()
                        cursor = Cursor()
                        start_time = time.time()
                        game_over = False

            if not game_over:
                # Update game objects
                cursor.move()
                ball.move()

                # Check collision
                if check_collision(ball, cursor):
                    game_over = True
                    final_score = int(time.time() - start_time)
                    print(f"Game Over! Final Score: {final_score}")  # Debug print

            # Drawing
            screen.fill(BLACK)
            ball.draw(screen)
            cursor.draw(screen)

            # Display score
            if not game_over:
                score = int(time.time() - start_time)
                score_text = font.render(f"Score: {score}", True, WHITE)
            else:
                score_text = font.render(f"Game Over! Final Score: {final_score}", True, WHITE)
                restart_text = font.render("Press R to restart", True, WHITE)
                screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

            screen.blit(score_text, (10, 10))
            pygame.display.flip()
            clock.tick(FPS)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
