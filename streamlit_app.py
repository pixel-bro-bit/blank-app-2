import streamlit as st
import matplotlib.pyplot as plt
import math
import time

st.title("Stickman Fight Animation")

# Define canvas size and animation parameters.
WIDTH, HEIGHT = 800, 600
punch_cycle = 60  # frames for a full punch cycle
frame_count = 0

# Define two stickmen as dictionaries.
stickman1 = {
    'x': 200,       # Initial horizontal position
    'y': 500,       # Base y-position (feet)
    'dx': 2,        # Horizontal speed
    'facing': 'right',  # Direction facing (which arm punches)
    'phase': 0,     # Phase offset for arm animation
    'scale': 1
}

stickman2 = {
    'x': 600,
    'y': 500,
    'dx': -2,
    'facing': 'left',
    'phase': 30,    # Phase offset so that punches alternate
    'scale': 1
}

def get_punch_offset(frame, phase, max_extension=15):
    """
    Computes a smooth punch extension using a sine wave.
    """
    progress = ((frame + phase) % punch_cycle) / punch_cycle
    return max_extension * math.sin(progress * math.pi)

def draw_stickman(ax, x, y, scale, facing, punch_offset):
    """
    Draws a simple stickman on the provided Matplotlib axis.
    
    Parameters:
      ax           - Matplotlib axis
      x, y         - Base coordinates (where the feet are)
      scale        - Size scaling factor
      facing       - 'right' or 'left' (which arm will be extended)
      punch_offset - Extra pixels to extend the punching arm
    """
    # Define dimensions.
    head_radius = 10 * scale        
    body_length = 30 * scale        
    leg_length  = 20 * scale        
    arm_length  = 15 * scale

    # --- Draw Head ---
    head_center = (x, y - body_length - head_radius)
    head = plt.Circle(head_center, head_radius, fill=False, edgecolor='black', linewidth=2)
    ax.add_artist(head)

    # --- Draw Body ---
    neck_y = y - body_length
    ax.plot([x, x], [neck_y, y], 'k-', lw=2)

    # --- Draw Arms ---
    # Arms start at shoulder level.
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
    left_leg_end  = (x - 10 * scale, y + leg_length)
    right_leg_end = (x + 10 * scale, y + leg_length)
    ax.plot([x, left_leg_end[0]], [y, left_leg_end[1]], 'k-', lw=2)
    ax.plot([x, right_leg_end[0]], [y, right_leg_end[1]], 'k-', lw=2)

def update_positions():
    """
    Updates the horizontal positions of the stickmen and reverses direction 
    if they get
