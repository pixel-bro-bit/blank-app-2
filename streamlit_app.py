import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Fight Animation")

# Set up the clock for controlling the FPS
clock = pygame.time.Clock()

# Global frame counter and punching cycle (in frames)
frame_count = 0
punch_cycle = 60  # One full punch cycle (extend and retract)

# Define two stickmen with initial properties.
stickman1 = {
    'x': 200,       # Starting horizontal position (left side)
    'y': 500,       # Base y-position (where feet are drawn)
    'dx': 2,        # Horizontal movement speed
    'facing': 'right',
    'phase': 0,     # Phase offset for punch timing (in frames)
    'scale': 1      # Scale factor for dimensions
}

stickman2 = {
    'x': 600,       # Starting horizontal position (right side)
    'y': 500,
    'dx': -2,
    'facing': 'left',
    'phase': 30,    # Offset phase so that punches alternate with stickman1
    'scale': 1
}

def get_punch_offset(frame, phase, max_extension=15):
    """
    Calculate an offset for the punching arm using a sine function.

    Parameters:
      frame       - current global frame
      phase       - stickman's phase offset for punch timing
      max_extension - maximum additional extension for the punch (in pixels)

    Returns:
      a value between 0 and max_extension for arm extension.
    """
    progress = ((frame + phase) % punch_cycle) / punch_cycle  # Normalize progress (0 to 1)
    return max_extension * math.sin(progress * math.pi)

def draw_stickman(surface, x, y, scale, facing, punch_offset):
    """
    Draw a stickman on the given surface.

    Parameters:
      surface      - the Pygame surface to draw on
      x, y         - the base position for the stickman (at the feet)
      scale        - scaling factor for the stickman's size
      facing       - direction the stickman is facing ("left" or "right")
      punch_offset - additional extension for the punching arm (animated)
    """
    # Define basic dimensions based on scale
    head_radius  = 10 * scale        # Radius for the head
    body_length  = 30 * scale        # Length of the body (neck to waist)
    leg_length   = 20 * scale        # Leg length
    arm_length   = 15 * scale        # Default arm extension

    # --- Draw Head ---
    head_center = (int(x), int(y - body_length - head_radius))
    pygame.draw.circle(surface, (0, 0, 0), head_center, int(head_radius), 2)

    # --- Draw Body ---
    neck_y = y - body_length
    pygame.draw.line(surface, (0, 0, 0), (x, neck_y), (x, y), 2)

    # --- Draw Arms ---
    # Draw arms starting from shoulder level (a little below the neck)
    arm_start_y = y - body_length + 10 * scale
    # Default end positions for left and right arms
    left_arm_end  = (x - arm_length, int(arm_start_y + 10 * scale))
    right_arm_end = (x + arm_length, int(arm_start_y + 10 * scale))

    if facing == "right":
        # For a stickman facing right, extend the right arm as the punch.
        right_arm_end = (x + arm_length + punch_offset, int(arm_start_y + 10 * scale))
    else:
        # For a stickman facing left, extend the left arm.
        left_arm_end = (x - arm_length - punch_offset, int(arm_start_y + 10 * scale))

    pygame.draw.line(surface, (0, 0, 0), (x, int(arm_start_y)), left_arm_end, 2)
    pygame.draw.line(surface, (0, 0, 0), (x, int(arm_start_y)), right_arm_end, 2)

    # --- Draw Legs ---
    left_leg_end  = (x - int(10 * scale), y + leg_length)
    right_leg_end = (x + int(10 * scale), y + leg_length)
    pygame.draw.line(surface, (0, 0, 0), (x, y), left_leg_end, 2)
    pygame.draw.line(surface, (0, 0, 0), (x, y), right_leg_end, 2)

def update_positions():
    """
    Update the positions of the stickmen.
    Reverse their horizontal movement when they get too close or hit the screen edges.
    """
    stickman1['x'] += stickman1['dx']
    stickman2['x'] += stickman2['dx']

    # If the stickmen get close (less than 100 pixels apart), reverse direction to simulate a clash.
    if stickman2['x'] - stickman1['x'] < 100:
        stickman1['dx'] *= -1
        stickman2['dx'] *= -1

    # Bounce off the screen edges.
    if stickman1['x'] < 50 or stickman1['x'] > WIDTH - 50:
        stickman1['dx'] *= -1
    if stickman2['x'] < 50 or stickman2['x'] > WIDTH - 50:
        stickman2['dx'] *= -1

# Main animation loop
running = True
while running:
    clock.tick(60)  # Limit to 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_count += 1

    # Clear the screen to white
    screen.fill((255, 255, 255))

    # Update stickmen positions and simulate a clash effect.
    update_positions()

    # Compute the punch offsets using the current frame and each stickman's phase
    punch1 = get_punch_offset(frame_count, stickman1['phase'])
    punch2 = get_punch_offset(frame_count, stickman2['phase'])

    # Draw both stickmen
    draw_stickman(screen, stickman1['x'], stickman1['y'], stickman1['scale'], stickman1['facing'], punch1)
    draw_stickman(screen, stickman2['x'], stickman2['y'], stickman2['scale'], stickman2['facing'], punch2)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
