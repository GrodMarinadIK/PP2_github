import pygame
import os
from player import MusicPlayer 

# Initialization
pygame.init() 
W, H = 1000, 400 
# Load and set window icon
icon = pygame.image.load('Practice9/music_player/icon.png')
pygame.display.set_icon(icon)
# Enable RESIZABLE mode for manual scaling and Fullscreen transitions
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 50)

# State flags
dragging = False 
is_fullscreen = False

player = MusicPlayer()
running = True
clock = pygame.time.Clock()

def get_track_icon(track_name):
    """
    Locates the artwork for a track based on its filename.
    Looks for a .png file with the same name in the 'music_icons' directory.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_name = track_name.replace(".mp3", "")
    icon_path = os.path.join(base_path, "music_icons", f"{base_name}.png")
    
    if os.path.exists(icon_path):
        return pygame.image.load(icon_path)
    return None

while running:
    # Get current window dimensions for dynamic layout calculations
    curr_w, curr_h = screen.get_size()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Define slider position based on window mode
    slider_x, slider_y = curr_w // 2 - 250, curr_h - 100
    if is_fullscreen:
        slider_x = int(curr_w * 0.6) # Shift slider right in Fullscreen
        slider_y = int(curr_h * 0.7)
    slider_w, slider_h = 500, 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Toggle Fullscreen mode
            if event.key == pygame.K_f:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((1000, 400), pygame.RESIZABLE)
            
            # Playback controls
            if event.key == pygame.K_p: player.play() 
            elif event.key == pygame.K_s: player.stop()
            elif event.key == pygame.K_n or event.key == pygame.K_RIGHT: player.next_track()
            elif event.key == pygame.K_b or event.key == pygame.K_LEFT: player.prev_track()
            elif event.key == pygame.K_r: player.shuffle_playlist()

        # Mouse click handling for volume slider
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if click is within slider boundaries
                if slider_x <= mouse_x <= slider_x + slider_w and slider_y - 10 <= mouse_y <= slider_y + 10:
                    dragging = True
                    # Immediate volume change on click
                    new_v = (mouse_x - slider_x) / slider_w
                    player.volume = max(0.0, min(1.0, new_v))
                    pygame.mixer.music.set_volume(player.volume)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        # Continuous volume adjustment while dragging
        if event.type == pygame.MOUSEMOTION and dragging:
            new_v = (mouse_x - slider_x) / slider_w
            player.volume = max(0.0, min(1.0, new_v))
            pygame.mixer.music.set_volume(player.volume)

    # Rendering Logic
    screen.fill((117, 177, 169)) # Background color

    if player.playlist:
        raw_name = player.playlist[player.current_track_index]
        display_name = raw_name.replace(".mp3", "")

        if is_fullscreen:
            # --- FULLSCREEN LAYOUT (3W/8 Formula) ---
            margin_w = curr_w // 16
            container_w = (curr_w // 2) - (2 * margin_w)
            
            # Drawing the artwork container background
            bg_color = (42, 49, 50)
            container_rect = pygame.Rect(margin_w, curr_h // 2 - container_w // 2, container_w, container_w)
            pygame.draw.rect(screen, bg_color, container_rect, border_radius=15)
            
            # Calculate image size with 10% inner margin
            img_margin = container_w // 10
            img_size = container_w - (2 * img_margin)
            
            # Render track artwork
            icon = get_track_icon(raw_name)
            if icon:
                icon = pygame.transform.smoothscale(icon, (img_size, img_size))
                img_x = container_rect.x + img_margin
                img_y = container_rect.y + img_margin
                screen.blit(icon, (img_x, img_y))
            
            # Render track info on the right half (centered at 75% width)
            text_surf = big_font.render(display_name, True, (77, 109, 154))
            text_x = int(curr_w * 0.75) - text_surf.get_width() // 2
            screen.blit(text_surf, (text_x, curr_h // 3))
        else:
            # --- NORMAL MODE: Centered track name ---
            text_surf = big_font.render(f"Now Playing: {display_name}", True, (77, 109, 154))
            text_rect = text_surf.get_rect(center=(curr_w // 2, curr_h // 2))
            screen.blit(text_surf, text_rect)

        # Draw Volume Slider
        pygame.draw.rect(screen, (110, 102, 88), (slider_x, slider_y, slider_w, slider_h))
        current_vol_w = int(slider_w * player.volume)
        pygame.draw.rect(screen, (37, 78, 88), (slider_x, slider_y, current_vol_w, slider_h))
        pygame.draw.circle(screen, (255, 255, 255), (slider_x + current_vol_w, slider_y + slider_h // 2), 10)
        
        # Volume percentage indicator
        vol_text = font.render(f"{int(player.volume * 100)}%", True, (239, 251, 235))
        screen.blit(vol_text, (slider_x + slider_w + 20, slider_y - 10))

        # Controls hint
        hint_txt = "F: Fullscreen | R: Shuffle | P/S: Play/Stop | (N/→)/(B/←): Next/Back"
        hint_surf = font.render(hint_txt, True, (239, 251, 235))
        screen.blit(hint_surf, (curr_w // 2 - hint_surf.get_width() // 2, curr_h - 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()