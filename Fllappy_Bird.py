
import pygame
import random
import sys
import math

pygame.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Normal Edition")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 28, bold=True)
big_font = pygame.font.SysFont("Arial", 45, bold=True)

# Colors
BLUE = (100, 190, 255)
YELLOW = (255, 220, 0)
ORANGE = (255, 130, 0)
GREEN = (20, 180, 40)
DARK_GREEN = (0, 120, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bird settings
bird_x = 80
bird_y = 250
velocity = 0

GRAVITY = 0.32
JUMP = -6.5
MAX_FALL_SPEED = 5

# Pipe settings
PIPE_WIDTH = 60
PIPE_GAP = 190
PIPE_SPEED = 2.5

pipes = []

score = 0
best_score = 0

started = False
game_over = False


# Create pipe
def create_pipe():

    height = random.randint(90, 300)

    pipes.append({
        "x": WIDTH,
        "height": height,
        "passed": False
    })


# Reset game
def reset_game():

    global bird_y, velocity
    global pipes, score
    global started, game_over

    bird_y = 250
    velocity = 0

    pipes = []
    create_pipe()

    score = 0

    started = True
    game_over = False


# Draw bird
def draw_bird():

    x = bird_x
    y = int(bird_y)

    wing = math.sin(pygame.time.get_ticks() * 0.015) * 3

    # Tail
    pygame.draw.polygon(
        screen, ORANGE,
        [(x-12, y), (x-27, y-8), (x-25, y+8)]
    )

    # Wing
    pygame.draw.ellipse(
        screen, (230, 165, 0),
        (x-14, y-5+wing, 19, 13)
    )

    # Body
    pygame.draw.ellipse(
        screen, YELLOW,
        (x-18, y-16, 38, 32)
    )

    # Eye
    pygame.draw.circle(
        screen, WHITE,
        (x+8, y-8), 7
    )

    pygame.draw.circle(
        screen, BLACK,
        (x+10, y-8), 3
    )

    # Beak
    pygame.draw.polygon(
        screen, ORANGE,
        [(x+17, y-2), (x+30, y+3), (x+17, y+8)]
    )


# Draw pipes
def draw_pipes():

    for pipe in pipes:

        x = int(pipe["x"])
        h = pipe["height"]

        # Top pipe
        pygame.draw.rect(
            screen, GREEN,
            (x, 0, PIPE_WIDTH, h-20)
        )

        pygame.draw.rect(
            screen, DARK_GREEN,
            (x, 0, 7, h-20)
        )

        pygame.draw.rect(
            screen, GREEN,
            (x-5, h-20, PIPE_WIDTH+10, 20)
        )

        # Bottom pipe
        bottom = h + PIPE_GAP

        pygame.draw.rect(
            screen, GREEN,
            (x, bottom+20, PIPE_WIDTH,
             HEIGHT-bottom-20)
        )

        pygame.draw.rect(
            screen, DARK_GREEN,
            (x, bottom+20, 7,
             HEIGHT-bottom-20)
        )

        pygame.draw.rect(
            screen, GREEN,
            (x-5, bottom, PIPE_WIDTH+10, 20)
        )


# Background
def draw_background():

    screen.fill(BLUE)

    # Clouds
    pygame.draw.circle(screen, WHITE, (60, 90), 22)
    pygame.draw.circle(screen, WHITE, (85, 90), 28)
    pygame.draw.circle(screen, WHITE, (110, 90), 20)

    pygame.draw.circle(screen, WHITE, (260, 150), 20)
    pygame.draw.circle(screen, WHITE, (285, 150), 27)
    pygame.draw.circle(screen, WHITE, (310, 150), 20)

    # Ground
    pygame.draw.rect(
        screen, (220, 190, 80),
        (0, HEIGHT-25, WIDTH, 25)
    )

    pygame.draw.rect(
        screen, (100, 200, 50),
        (0, HEIGHT-30, WIDTH, 8)
    )


# Initial pipe
create_pipe()


# Main game loop
while True:

    clock.tick(60)

    draw_background()

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if game_over:
                    reset_game()

                else:
                    started = True
                    velocity = JUMP

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_over:
                reset_game()

            else:
                started = True
                velocity = JUMP

    # Game update
    if started and not game_over:

        # Bird movement
        velocity += GRAVITY

        velocity = min(
            velocity,
            MAX_FALL_SPEED
        )

        bird_y += velocity

        # Pipe creation
        if pipes[-1]["x"] < 210:
            create_pipe()

        # Move pipes
        for pipe in pipes:
            pipe["x"] -= PIPE_SPEED

        # Collision box
        bird_rect = pygame.Rect(
            bird_x-13,
            int(bird_y)-12,
            26, 24
        )

        # Collision detection
        for pipe in pipes:

            x = int(pipe["x"])
            h = pipe["height"]

            top_rect = pygame.Rect(
                x, 0, PIPE_WIDTH, h-20
            )

            bottom_rect = pygame.Rect(
                x, h+PIPE_GAP+20,
                PIPE_WIDTH,
                HEIGHT-h-PIPE_GAP-20
            )

            if bird_rect.colliderect(top_rect):
                game_over = True

            if bird_rect.colliderect(bottom_rect):
                game_over = True

            # Score
            if not pipe["passed"]:

                if x + PIPE_WIDTH < bird_x:

                    score += 1
                    pipe["passed"] = True

                    best_score = max(best_score, score)

        # Remove old pipes
        pipes = [
            p for p in pipes
            if p["x"] > -PIPE_WIDTH
        ]

        # Ground and sky collision
        if bird_y > HEIGHT-40 or bird_y < 10:
            game_over = True

    # Draw game objects
    draw_pipes()
    draw_bird()

    # Score
    score_text = font.render(
        "Score: " + str(score),
        True, WHITE
    )

    screen.blit(score_text, (10, 10))

    best_text = font.render(
        "Best: " + str(best_score),
        True, WHITE
    )

    screen.blit(best_text, (10, 45))

    # Start screen
    if not started:

        title = big_font.render(
            "FLAPPY BIRD",
            True, WHITE
        )

        instruction = font.render(
            "PRESS SPACE TO START",
            True, BLACK
        )

        screen.blit(title, (65, 230))
        screen.blit(instruction, (45, 300))

    # Game over
    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 130))
        screen.blit(overlay, (0, 0))

        title = big_font.render(
            "GAME OVER",
            True, WHITE
        )

        final_score = font.render(
            "Score: " + str(score),
            True, WHITE
        )

        restart = font.render(
            "SPACE TO RESTART",
            True, WHITE
        )

        screen.blit(title, (65, 220))
        screen.blit(final_score, (125, 285))
        screen.blit(restart, (65, 350))

    pygame.display.flip()