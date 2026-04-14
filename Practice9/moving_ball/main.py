import pygame
from ball import Ball

# Initialize all imported pygame modules
pygame.init()

# Window configuration
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Smooth Moving Ball")

# Background color (off-white) and ball instance
bgcolor = (251, 255, 251)
ball = Ball(W, H)

# Framerate controller and main loop flag
clock = pygame.time.Clock()
running = True

# Main Game Loop
while running:
    # 1. Event Handling (Check for system events like window close)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # 2. Update Logic (Poll keyboard state and update ball position)
    keys = pygame.key.get_pressed()
    ball.update(keys)

    # 3. Rendering Pipeline
    screen.fill(bgcolor) # Clear the screen with background color
    ball.draw(screen)    # Render the ball at its updated coordinates
    
    pygame.display.flip() # Swap buffers to show the new frame
    clock.tick(60)        # Maintain consistent 60 FPS for smooth physics
    
pygame.quit()