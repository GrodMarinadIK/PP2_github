import pygame

class Ball:
    def __init__(self, screen_w, screen_h):
        # Appearance settings
        self.radius = 25  # Total radius including the outline
        self.outline_thickness = 4  # Thickness of the outer ring
        
        # Colors (Geometry Dash style: lighter outline, darker core)
        self.outline_color = (248, 124, 99) # Bright coral/red outline
        self.core_color = (244, 50, 11)    # Intense red core
        
        # Position initialization (using floats for sub-pixel movement precision)
        self.x = float(screen_w // 2)
        self.y = float(screen_h // 2)
        
        # Speed constants
        self.base_speed = 5
        self.dash_speed = 15 
        
        # Screen dimensions for boundary constraints
        self.screen_w = screen_w
        self.screen_h = screen_h

    def update(self, keys):
        # Movement speed toggle: Sprint mode if Space is held
        current_speed = self.dash_speed if keys[pygame.K_SPACE] else self.base_speed
        
        # Directional input handling (supports simultaneous key presses for diagonal movement)
        if keys[pygame.K_UP] or keys[pygame.K_w]: self.y -= current_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: self.y += current_speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.x -= current_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.x += current_speed

        # Boundary Clamping: Prevent the ball from leaving the screen area
        # We ensure the distance from the center to any edge is at least the radius
        r = self.radius 
        if self.x < r: self.x = r
        if self.x > self.screen_w - r: self.x = self.screen_w - r
        if self.y < r: self.y = r
        if self.y > self.screen_h - r: self.y = self.screen_h - r

    def draw(self, screen):
        # Step 1: Draw the outer circle (Outline)
        # This defines the full size of the object
        pygame.draw.circle(screen, self.outline_color, (int(self.x), int(self.y)), self.radius)
        
        # Step 2: Overlay the inner circle (Core)
        # Offset the radius by thickness to create the outline effect
        core_r = self.radius - self.outline_thickness
        pygame.draw.circle(screen, self.core_color, (int(self.x), int(self.y)), core_r)