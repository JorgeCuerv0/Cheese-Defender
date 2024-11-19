# Author: Jorgé Sandoval
# Assignment 9
# Date: 11-14-2024
# This program is a game called Cheese Defender
# The player must protect the cheese from roaches by clicking on them
# The player earns points for each roach killed
# The game ends if a roach reaches the cheese
# The player can restart the game or quit after the game ends

import pygame  # Importing Pygame for game development
import random  # Importing random for randomness in roach behavior
import time    # Importing time for tracking elapsed game time
import math    # Importing math for geometric calculations

def initialize_game():
    """
    Initialize the game variables and setup.
    This function sets up the screen, loads assets, and initializes game variables.
    """
    global WIDTH, HEIGHT, FONT, screen, SCALE_FACTOR, ROACH_TYPES, ROACH_IMAGES, DEAD_IMAGES
    global cheese_image, cheese_rect, cheese_hitbox, squish_sounds, max_roaches
    global game_over, score, roach_list, start_time

    # Initialize Pygame library
    pygame.init()  # Start Pygame and prepare it for use.

    # Screen dimensions and font
    WIDTH, HEIGHT = 800, 600  # Set the screen width and height.
    FONT = pygame.font.Font(None, 36)  # Load the default font with size 36.
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game screen.
    pygame.display.set_caption("Cheese Defender")  # Set the title of the game window.

    # Scale factor for images
    SCALE_FACTOR = 0.15  # Set the uniform scaling factor for all images.

    # Load roach and cheese images
    def load_and_scale_image(path):
        """
        Load an image and scale it.
        :param path: Path to the image file.
        :return: Scaled image.
        """
        image = pygame.image.load(path)  # Load the image from the provided path.
        size = (int(image.get_width() * SCALE_FACTOR), int(image.get_height() * SCALE_FACTOR))  # Scale the image size.
        return pygame.transform.scale(image, size)  # Return the scaled image.

    # Define roach types and their images
    ROACH_TYPES = ["normal", "bigboy", "tipsy", "fast"]  # Different types of roaches.
    ROACH_IMAGES = {
        "normal": load_and_scale_image("pics/roach_normal.png"),  # Load normal roach image.
        "fast": load_and_scale_image("pics/roach_fast.png"),      # Load fast roach image.
        "bigboy": load_and_scale_image("pics/bigboy.png"),        # Load bigboy roach image.
        "tipsy": load_and_scale_image("pics/tipsy.png")           # Load tipsy roach image.
    }
    # Define dead roach images
    DEAD_IMAGES = {
        "normal": load_and_scale_image("pics/dead_roach_normal.png"),  # Load dead normal roach image.
        "fast": load_and_scale_image("pics/dead_fast.png"),            # Load dead fast roach image.
        "bigboy": load_and_scale_image("pics/dead_bigboy.png"),        # Load dead bigboy roach image.
        "tipsy": load_and_scale_image("pics/dead_tipsy.png")           # Load dead tipsy roach image.
    }

    # Load and position the cheese image
    cheese_image = load_and_scale_image("pics/cheese.png")  # Load the cheese image.
    cheese_rect = cheese_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the cheese on the screen.
    cheese_hitbox = cheese_rect.inflate(-20, -20)  # Shrink the cheese hitbox for better collision detection.

    # Load background music and squish sounds
    pygame.mixer.music.load("sounds/music.mp3")  # Load background music.
    pygame.mixer.music.set_volume(0.3)  # Set the music volume to 30%.
    squish_sounds = [pygame.mixer.Sound(f"sounds/squish{i}.mp3") for i in range(1, 7)]  # Load six squish sound effects.

    # Game variables
    max_roaches = 15  # Set the maximum number of active roaches.
    roach_list = []  # Initialize an empty list to hold active roaches.
    score = 0  # Set the initial score to 0.
    start_time = time.time()  # Record the start time of the game.
    game_over = False  # Initialize the game over flag as False.

def display_text(text, position, color=(255, 255, 255)):
    """
    Render and display text on the screen.
    :param text: The text to display.
    :param position: The position (x, y) to display the text.
    :param color: The color of the text (default is white).
    """
    text_surface = FONT.render(text, True, color)  # Render the text with the specified color.
    screen.blit(text_surface, position)  # Draw the text on the screen at the specified position.

class Roach:
    """
    Represents a roach in the game.
    Each roach moves towards the cheese and can be clicked to reduce its health.
    """
    def __init__(self, roach_type, speed):
        self.type = roach_type  # Store the type of roach.
        self.speed = speed  # Store the speed of the roach.
        self.health = 1 if roach_type != "bigboy" else 2  # Set health based on roach type.
        self.position = random_offscreen_position()  # Spawn the roach offscreen.
        self.target = cheese_rect.center  # Set the cheese as the target.
        self.image = ROACH_IMAGES[roach_type]  # Load the corresponding image for the roach type.
        self.dead_image = DEAD_IMAGES[roach_type]  # Load the corresponding dead image for the roach type.
        self.is_dead = False  # Initialize the dead status as False.
        self.death_time = None  # Initialize the time of death.
        self.angle_offset = random.uniform(0, 2 * math.pi)  # Set a random angle for swirling.
        self.clockwise = random.choice([True, False])  # Randomly decide swirling direction.

    def move(self):
        """Move the roach based on its type and behavior."""
        if not self.is_dead:  # Only move if the roach is alive.
            if self.type == "normal":
                self.position = move_towards(self.position, self.target, self.speed)  # Move normally.
            elif self.type == "bigboy":
                self.position = move_towards(self.position, self.target, self.speed / 2)  # Move slower.
            elif self.type == "fast":
                self.position = move_towards(self.position, self.target, self.speed * 2)  # Move faster.
            elif self.type == "tipsy":
                self.position = move_tipsy_path(self.position, self.target, self.speed, self.angle_offset, self.clockwise)  # Move in a swirl.
                self.angle_offset += 0.15 if self.clockwise else -0.15  # Adjust swirling angle.

    def get_hit(self, mouse_position):
        """
        Handle being clicked.
        :param mouse_position: The position of the mouse click.
        :return: True if the roach is killed, otherwise False.
        """
        if not self.is_dead:
            roach_rect = self.image.get_rect(center=self.position)  # Get the roach's rectangle for collision.
            if roach_rect.collidepoint(mouse_position):  # Check if the mouse click hits the roach.
                self.health -= 1  # Reduce health by 1.
                if self.health == 1 and self.type == "bigboy":  # Shrink bigboy on first hit.
                    self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.8), int(self.image.get_height() * 0.8)))
                if self.health <= 0:  # Check if the roach is dead.
                    self.is_dead = True  # Mark the roach as dead.
                    self.death_time = pygame.time.get_ticks()  # Record the time of death.
                    random.choice(squish_sounds).play()  # Play a random squish sound.
                    return True  # Indicate the roach is killed.
        return False  # Roach is not killed.

    def draw(self):
        """Draw the roach."""
        if self.is_dead:  # If the roach is dead, handle fading.
            time_since_death = (pygame.time.get_ticks() - self.death_time) / 1500  # Calculate time since death.
            if time_since_death < 1:  # Fade out over 1.5 seconds.
                dead_image = self.dead_image.copy()  # Copy the dead image for modification.
                dead_image.set_alpha(int(255 * (1 - time_since_death)))  # Reduce transparency over time.
                angle = math.degrees(math.atan2(self.target[1] - self.position[1], self.target[0] - self.position[0])) + 90  # Calculate angle to cheese.
                rotated_image = pygame.transform.rotate(dead_image, angle)  # Rotate the image.
                screen.blit(rotated_image, rotated_image.get_rect(center=self.position))  # Draw the rotated image.
            else:
                roach_list.remove(self)  # Remove the roach after fading.
        else:  # If the roach is alive, draw it normally.
            angle = math.degrees(math.atan2(self.target[1] - self.position[1], self.target[0] - self.position[0]))  # Calculate angle to cheese.
            rotated_image = pygame.transform.rotate(self.image, -angle)  # Rotate the image.
            screen.blit(rotated_image, rotated_image.get_rect(center=self.position))  # Draw the rotated image.

def random_offscreen_position():
    """
    Generate a random position offscreen for spawning roaches.
    :return: Tuple of (x, y) coordinates.
    """
    edge = random.choice(["top", "bottom", "left", "right"])  # Randomly choose an edge.
    if edge == "top":
        return random.randint(0, WIDTH), -50  # Spawn above the screen.
    elif edge == "bottom":
        return random.randint(0, WIDTH), HEIGHT + 50  # Spawn below the screen.
    elif edge == "left":
        return -50, random.randint(0, HEIGHT)  # Spawn to the left of the screen.
    else:
        return WIDTH + 50, random.randint(0, HEIGHT)  # Spawn to the right of the screen.

def move_towards(position, target, speed):
    """
    Calculate the next position for moving towards a target.
    :param position: Current position of the object (x, y).
    :param target: Target position (x, y).
    :param speed: Speed of movement.
    :return: New position (x, y).
    """
    x, y = position
    target_x, target_y = target
    dx, dy = target_x - x, target_y - y  # Calculate the direction vector.
    distance = math.sqrt(dx ** 2 + dy ** 2)  # Calculate the distance to the target.
    if distance != 0:  # Avoid division by zero.
        dx, dy = dx / distance, dy / distance  # Normalize the direction vector.
    return x + dx * speed, y + dy * speed  # Move closer to the target.

def move_tipsy_path(position, target, speed, angle_offset, clockwise):
    """
    Move in a swirling pattern towards the target.
    :param position: Current position of the roach.
    :param target: Target position (usually the cheese).
    :param speed: Speed of movement.
    :param angle_offset: Offset angle for swirling.
    :param clockwise: Boolean indicating direction of swirl.
    :return: New position (x, y).
    """
    x, y = position
    target_x, target_y = target
    dx, dy = target_x - x, target_y - y  # Calculate the direction vector.
    distance = math.sqrt(dx ** 2 + dy ** 2)  # Calculate distance to the target.

    # Calculate swirling offset
    swirl_radius = 3  # Set the radius for the swirl.
    swirl_x = math.cos(angle_offset) * swirl_radius  # X offset for swirl.
    swirl_y = math.sin(angle_offset) * swirl_radius  # Y offset for swirl.

    if distance != 0:  # Avoid division by zero.
        dx, dy = dx / distance, dy / distance  # Normalize the direction vector.

    # Combine straight and swirling motion
    return x + dx * speed + swirl_x, y + dy * speed + swirl_y

def spawn_roaches():
    """
    Spawn a new roach if the maximum number of roaches hasn't been reached.
    """
    if len(roach_list) < max_roaches:  # Check if the roach count is below the limit.
        roach_type = random.choice(ROACH_TYPES)  # Choose a random roach type.
        speed = random.uniform(1, 2)  # Assign a random speed within range.
        roach_list.append(Roach(roach_type, speed))  # Add the new roach to the list.

def game_over_screen():
    """
    Display the game over screen with options to restart or quit.
    """
    screen.fill((0, 0, 0))  # Clear the screen with a black background.
    display_text("Game Over!", (WIDTH // 2 - 80, HEIGHT // 2 - 60))  # Display "Game Over!".
    display_text("Press R to Restart", (WIDTH // 2 - 80, HEIGHT // 2))  # Display restart prompt.
    display_text("Press Q to Quit", (WIDTH // 2 - 80, HEIGHT // 2 + 30))  # Display quit prompt.
    pygame.display.flip()  # Update the screen to show the game over messages.
    pygame.mixer.music.stop()  # Stop the background music.
    wait_for_restart()  # Wait for user input to restart or quit.

def wait_for_restart():
    """
    Wait for user input to restart the game or quit.
    """
    while True:
        for event in pygame.event.get():  # Check for user events.
            if event.type == pygame.QUIT:  # If the user closes the window, quit the game.
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:  # Check for keypress events.
                if event.key == pygame.K_r:  # If 'R' is pressed, restart the game.
                    initialize_game()  # Reinitialize the game variables.
                    main_game()  # Start the main game loop.
                elif event.key == pygame.K_q:  # If 'Q' is pressed, quit the game.
                    pygame.quit()
                    exit()

def main_game():
    """
    Main game loop that handles gameplay mechanics and events.
    """
    global game_over, score
    pygame.mixer.music.play(-1)  # Start playing the background music in a loop.
    start_time = time.time()  # Record the start time of the game.

    while not game_over:  # Keep running the game while it's not over.
        screen.fill((0, 0, 0))  # Clear the screen with a black background.
        screen.blit(cheese_image, cheese_rect)  # Draw the cheese at its position.
        elapsed_time = int(time.time() - start_time)  # Calculate elapsed time.
        display_text(f"Time: {elapsed_time}s", (10, 10))  # Display elapsed time.
        display_text(f"Score: {score}", (10, 40))  # Display the current score.

        for event in pygame.event.get():  # Check for user events.
            if event.type == pygame.QUIT:  # If the user closes the window, quit the game.
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse clicks.
                mouse_position = pygame.mouse.get_pos()  # Get the mouse position.
                for roach in roach_list:  # Iterate over all roaches.
                    if roach.get_hit(mouse_position):  # Check if the roach was clicked.
                        score += 1  # Increase the score if a roach is hit.

        spawn_roaches()  # Spawn new roaches if allowed.

        for roach in roach_list:  # Iterate over all roaches.
            roach.move()  # Move the roach.
            if cheese_hitbox.collidepoint(roach.position):  # Check if a roach touches the cheese.
                game_over = True  # Set the game over flag.
            roach.draw()  # Draw the roach.

        pygame.display.flip()  # Update the display with the latest changes.
        pygame.time.delay(30)  # Add a small delay to control game speed.

    game_over_screen()  # If the game is over, show the game over screen.

# Run the game
if __name__ == "__main__":
    initialize_game()  # Initialize the game variables and setup.
    main_game()  # Start the main game loop.
    pygame.quit()  # Quit Pygame when the game loop ends.

