import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 400, 200
BUTTON_WIDTH, BUTTON_HEIGHT = 80, 40
VOLUME_MIN, VOLUME_MAX = 0.0, 1.0
VOLUME_STEP = 0.1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Initial volume
current_volume = 0.5


message_box_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Volume Control")

# Initial volume
current_volume = 0.5

# Function to draw volume buttons
def draw_volume_buttons():
    volume_text = f"Volume: {current_volume:.1f}"
    font = pygame.font.Font(None, 36)
    text_surface = font.render(volume_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))

    pygame.draw.rect(message_box_screen, GRAY, increase_button)
    pygame.draw.rect(message_box_screen, GRAY, decrease_button)

    message_box_screen.blit(text_surface, text_rect)

    increase_font = pygame.font.Font(None, 36)
    increase_text = increase_font.render("+", True, BLACK)
    increase_rect = increase_text.get_rect(center=increase_button.center)
    message_box_screen.blit(increase_text, increase_rect)

    decrease_font = pygame.font.Font(None, 36)
    decrease_text = decrease_font.render("-", True, BLACK)
    decrease_rect = decrease_text.get_rect(center=decrease_button.center)
    message_box_screen.blit(decrease_text, decrease_rect)

# Button rectangles
increase_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)
decrease_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)

# Main game loop for the volume control interface
volume_screen_running = True
while volume_screen_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            volume_screen_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if increase_button.collidepoint(event.pos):
                current_volume = min(VOLUME_MAX, current_volume + VOLUME_STEP)
                pygame.mixer.music.set_volume(current_volume)
            elif decrease_button.collidepoint(event.pos):
                current_volume = max(VOLUME_MIN, current_volume - VOLUME_STEP)
                pygame.mixer.music.set_volume(current_volume)

    message_box_screen.fill(WHITE)
    draw_volume_buttons()
    pygame.display.flip()

# Close the message box window but keep Pygame running
pygame.display.quit()







# Example usage:

# Button rectangles
increase_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)
decrease_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if increase_button.collidepoint(event.pos):
                current_volume = min(VOLUME_MAX, current_volume + VOLUME_STEP)
                pygame.mixer.music.set_volume(current_volume)
            elif decrease_button.collidepoint(event.pos):
                current_volume = max(VOLUME_MIN, current_volume - VOLUME_STEP)
                pygame.mixer.music.set_volume(current_volume)

    screen.fill(WHITE)
    run_volume_control_interface()
    pygame.display.flip()

pygame.quit()
sys.exit()
