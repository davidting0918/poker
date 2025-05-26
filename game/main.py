import pygame

# Step 1: Initialize
pygame.init()
screen = pygame.display.set_mode((1600, 1200))
clock = pygame.time.Clock()

# Step 2: Game loop
running = True
while running:
    # 2.1: Handle input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Custom input (like clicking a button) goes here

    # 2.2: Update game logic (your poker engine)
    # (e.g., check who won, deal next card, etc.)

    # 2.3: Draw everything
    screen.fill((0, 128, 0))  # Green table background
    # (draw cards, players, chips, buttons here)

    pygame.display.flip()  # Update the screen

    # 2.4: Control FPS
    clock.tick(60)

pygame.quit()
