#Deploy a recursive learning algorith to train AI pilot avoid obstacles.
import pygame
import numpy as np
import random
import sys

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Plane Obstacle Avoidance")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Plane parameters
PLANE_SIZE = 40
PLANE_SPEED = 5
plane_x = WIDTH // 2
plane_y = HEIGHT - PLANE_SIZE
plane_color = BLUE

# Obstacle parameters
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 3
obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
obstacle_y = -OBSTACLE_HEIGHT
obstacle_color = RED

# Q-learning parameters
NUM_STATES = 100  # Total number of states (10 x 10 grid)
NUM_ACTIONS = 3  # Left, Right, Stay
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EXPLORATION_RATE = 1.0
EXPLORATION_DECAY = 0.995
MIN_EXPLORATION_RATE = 0.01

# Initialize Q-table
q_table = np.zeros((NUM_STATES, NUM_ACTIONS))

# Discretize state space
def get_state(plane_x, obstacle_x, obstacle_y):
    # Discretize plane and obstacle positions into a grid
    plane_state = min(plane_x // (WIDTH // 10), 9)  # 10 states for plane x-position
    obstacle_x_state = min(obstacle_x // (WIDTH // 10), 9)  # 10 states for obstacle x-position
    obstacle_y_state = min(obstacle_y // (HEIGHT // 10), 9)  # 10 states for obstacle y-position
    # Flatten the state into a single integer
    state = plane_state * 10 + obstacle_x_state  # Combine plane and obstacle x-position
    return min(state, NUM_STATES - 1)  # Ensure state is within bounds

# Choose action using epsilon-greedy strategy
def choose_action(state):
    if random.uniform(0, 1) < EXPLORATION_RATE:
        return random.randint(0, NUM_ACTIONS - 1)  # Explore
    else:
        return np.argmax(q_table[state])  # Exploit

# Update Q-value
def update_q_table(state, action, reward, next_state):
    best_next_action = np.argmax(q_table[next_state])
    q_table[state][action] += LEARNING_RATE * (
        reward + DISCOUNT_FACTOR * q_table[next_state][best_next_action] - q_table[state][action]
    )

# Draw plane and obstacle
def draw_plane(x, y):
    pygame.draw.rect(screen, plane_color, (x, y, PLANE_SIZE, PLANE_SIZE))

def draw_obstacle(x, y):
    pygame.draw.rect(screen, obstacle_color, (x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Main game loop
def main():
    global plane_x, obstacle_x, obstacle_y, EXPLORATION_RATE

    running = True
    episode = 0

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get current state
        state = get_state(plane_x, obstacle_x, obstacle_y)

        # Choose action
        action = choose_action(state)

        # Perform action
        if action == 0:  # Move left
            plane_x = max(plane_x - PLANE_SPEED, 0)
        elif action == 1:  # Move right
            plane_x = min(plane_x + PLANE_SPEED, WIDTH - PLANE_SIZE)

        # Update obstacle position
        obstacle_y += OBSTACLE_SPEED
        if obstacle_y > HEIGHT:
            obstacle_y = -OBSTACLE_HEIGHT
            obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)

        # Check for collision
        if (plane_x < obstacle_x + OBSTACLE_WIDTH and
            plane_x + PLANE_SIZE > obstacle_x and
            plane_y < obstacle_y + OBSTACLE_HEIGHT and
            plane_y + PLANE_SIZE > obstacle_y):
            reward = -10  # Penalty for collision
            obstacle_y = -OBSTACLE_HEIGHT  # Reset obstacle
            obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
        else:
            reward = 1  # Reward for avoiding obstacle

        # Get next state
        next_state = get_state(plane_x, obstacle_x, obstacle_y)

        # Update Q-table
        update_q_table(state, action, reward, next_state)

        # Decay exploration rate
        EXPLORATION_RATE = max(MIN_EXPLORATION_RATE, EXPLORATION_RATE * EXPLORATION_DECAY)

        # Draw objects
        draw_plane(plane_x, plane_y)
        draw_obstacle(obstacle_x, obstacle_y)

        # Display episode and exploration rate
        font = pygame.font.SysFont(None, 35)
        text = font.render(f"Episode: {episode}  Exploration Rate: {EXPLORATION_RATE:.2f}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

        episode += 1

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
