import streamlit as st
import matplotlib.pyplot as plt
import math
import time

st.title("Stickman Fight Animation")

# Canvas dimensions and animation parameters.
WIDTH, HEIGHT = 800, 600
punch_cycle = 60  # Number of frames for one full punch cycle.
frame_count = 0

# Define two stickmen as dictionaries with initial properties.
stickman1 = {
    'x': 200,        # Initial horizontal position (left side).
    'y': 500,        # Base y-position (where the feet are).
    'dx': 2,         # Horizontal speed.
    'facing': 'right',  # Which direction the stickman faces.
    'phase': 0,      # Phase offset for punch timing.
    'scale': 1
}

stickman2 = {
    'x': 600,        # Initial horizontal position (right side).
    'y': 500,
    'dx': -2,
    'facing': 'left',
    'phase': 30,     # Phase offset so that punches alternate.
    'scale': 1
}

def get_punch_offset(frame, phase, max_extension=15):
    """
    Computes a smooth punch extension using a sine wave.
    
    Parameters:
      frame        - Current global frame number.
      phase        - Stickman's phase offset for punch timing.
      max_extension - Maximum extra extension for the punch (in pixels).
    
    Returns:
      A float value between 0 and max_extension for the arm extension.
    """
    progress = ((frame + phase) % punch_cycle) / punch_cycle
    return max_extension * math.sin(progress * math.pi)

def draw_stickman(ax, x, y, scale, facing, punch_offset):
    """
    Draws a simple stickman on a provided Matplotlib axis.
    
    Parameters:
      ax           - Matplotlib axis.
      x, y         - Base coordinates (where the feet are).
      scale        - Size scaling factor.
      facing       - 'right' or 'left' (which arm will be extended as a punch).
      punch_offset - Extra pixels to extend the punching arm.
    """
    head_radius = 10 * scale
    body_length = 30 * scale
    leg_length = 20 * scale
    arm_length = 15 * scale

    # --- Draw Head ---
    head_center = (x, y - body_length - head_radius)
    head = plt.Circle(head_center, head_radius, fill=False, edgecolor='black', linewidth=2)
    ax.add_artist(head)

    # --- Draw Body ---
    neck_y = y - body_length
    ax.plot([x, x], [neck_y, y], 'k-', lw=2)

    # --- Draw Arms ---
    arm_start_y = y - body_length + 10 * scale
    left_arm_end = (x - arm_length, arm_start_y + 10 * scale)
    right_arm_end = (x + arm_length, arm_start_y + 10 * scale)
    if facing == 'right':
        # Extend the right arm for a punch.
        right_arm_end = (x + arm_length + punch_offset, arm_start_y + 10 * scale)
    else:
        # Extend the left arm.
        left_arm_end = (x - arm_length - punch_offset, arm_start_y + 10 * scale)
    ax.plot([x, left_arm_end[0]], [arm_start_y, left_arm_end[1]], 'k-', lw=2)
    ax.plot([x, right_arm_end[0]], [arm_start_y, right_arm_end[1]], 'k-', lw=2)

    # --- Draw Legs ---
    left_leg_end = (x - 10 * scale, y + leg_length)
    right_leg_end = (x + 10 * scale, y + leg_length)
    ax.plot([x, left_leg_end[0]], [y, left_leg_end[1]], 'k-', lw=2)
    ax.plot([x, right_leg_end[0]], [y, right_leg_end[1]], 'k-', lw=2)

def update_positions():
    """
    Updates the horizontal positions of the stickmen, reversing direction
    if they get too close to each other or reach the canvas boundaries.
    """
    stickman1['x'] += stickman1['dx']
    stickman2['x'] += stickman2['dx']

    # Reverse direction if the stickmen get too close (simulate a clash).
    if stickman2['x'] - stickman1['x'] < 100:
        stickman1['dx'] *= -1
        stickman2['dx'] *= -1

    # Bounce off the left/right boundaries.
    if stickman1['x'] < 50 or stickman1['x'] > WIDTH - 50:
        stickman1['dx'] *= -1
    if stickman2['x'] < 50 or stickman2['x'] > WIDTH - 50:
        stickman2['dx'] *= -1

# Create a placeholder to update the image in Streamlit.
placeholder = st.empty()

# Animation loop.
while True:
    frame_count += 1
    update_positions()
    punch1 = get_punch_offset(frame_count, stickman1['phase'])
    punch2 = get_punch_offset(frame_count, stickman2['phase'])
    
    # Set up a Matplotlib figure.
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)

    # Invert the y-axis so (0, 0) is at the top-left (mimicking screen coordinates).
    ax.invert_yaxis()  
    ax.axis('off')
    
    # Draw both stickmen.
    draw_stickman(ax, stickman1['x'], stickman1['y'], stickman1['scale'], stickman1['facing'], punch1)
    draw_stickman(ax, stickman2['x'], stickman2['y'], stickman2['scale'], stickman2['facing'], punch2)
    
    # Display the updated frame in Streamlit.
    placeholder.pyplot(fig)
    
    # Brief pause to control the frame rate.
    time.sleep(0.03)
