import pygame
from clock import MickeyClockLogic

# Initialization
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock by GrodMarinad2k")
clock = pygame.time.Clock()

# Main rotation pivot point (center of the screen)
CENTER = (WIDTH // 2, HEIGHT // 2)

# LOAD ASSETS
# .convert_alpha() is used for optimized transparent PNG rendering
body_img = pygame.image.load("Practice9\\mickeys_clock\\images\\mickey_clocks.png").convert_alpha()
original_hand = pygame.image.load("Practice9\\mickeys_clock\\images\\mickey_hand.png").convert_alpha()

# Create different hand versions by scaling the original asset
# Second hand: Longest and thinnest, fully white but semi-transparent for a subtle effect
hand_s = pygame.transform.scale(original_hand, (300, 80))
hand_s.fill((255, 255, 255, 150), special_flags=pygame.BLEND_RGBA_MULT)

# Minute hand: Medium length, slightly tinted blue for distinction, and semi-transparent
hand_m = pygame.transform.scale(original_hand, (200, 100))
# Adding 180 as the 4th value (Alpha) to make it semi-transparent
hand_m.fill((200, 200, 255, 180), special_flags=pygame.BLEND_RGBA_MULT)

# Hour hand: Short and thick, tinted red, and semi-transparent for a softer look
hand_h = pygame.transform.scale(original_hand, (150, 120))
# Adding 180 as the 4th value (Alpha)
hand_h.fill((255, 200, 200, 180), special_flags=pygame.BLEND_RGBA_MULT)


# Resize the clock body to fit the window dimensions
body_img = pygame.transform.scale(body_img, (700, 700))

# Initialize time calculation logic
clock_logic = MickeyClockLogic()

def draw_hand(surf, image, angle, center_pos):
    """
    Rotates the hand image around its starting edge (wrist) rather than its center.
    The 90-degree offset aligns the horizontal hand asset to the 12 o'clock position.
    """
    # Rotate the surface: negative angle for clockwise rotation
    rotated_image = pygame.transform.rotate(image, 90 - angle)
    
    # Calculate the offset vector from the center of the rotated image to the pivot point
    # This keeps the "wrist" of the hand fixed at the clock's center
    offset = pygame.math.Vector2(image.get_width() // 2, 0).rotate(angle - 90)
    
    # Create the rect and blit using the calculated center position
    new_rect = rotated_image.get_rect(center = center_pos + offset)
    surf.blit(rotated_image, new_rect)

# Main Application Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Retrieve current rotation angles from the logic module
    sec_angle, min_angle, hour_angle = clock_logic.get_angles()

    # RENDERING PIPELINE
    screen.fill((255, 255, 255)) # Clear screen with white background
    
    # 1. Draw the clock face (Body)
    body_rect = body_img.get_rect(center=CENTER)
    screen.blit(body_img, body_rect)
    
    # 2. Draw the hands in order (Hour -> Minute -> Second)
    draw_hand(screen, hand_h, hour_angle, CENTER) # The lowest layer (hours)
    draw_hand(screen, hand_m, min_angle, CENTER)  # The middle layer (minutes)
    draw_hand(screen, hand_s, sec_angle, CENTER)  # The top layer (seconds)

    # REFRESH
    pygame.display.flip()
    clock.tick(60) # Maintain 60 FPS for smooth rotation

pygame.quit()