import random
import curses
import os

# Initialize the curses library to create a screen
screen = curses.initscr()

# Hide the cursor
curses.curs_set(0)

# Start colors in curses
curses.start_color()

# Initialize color pair (pair number 1, white text on blue background)
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)


# Get max screen height and width
screen_height, screen_width = screen.getmaxyx()

# Create a new window
window = curses.newwin(screen_height, screen_width, 0, 0)

# Allow the window to receive input from the keyboard
window.keypad(1)

# Set delay for updating the screen
window.timeout(100)

# Set the background color
window.bkgd(' ', curses.color_pair(1))

# Set the x, y coordinates for the snake
snk_x = screen_width // 4
snk_y = screen_height // 2

# Define the initial position of the snake's body
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]

# Create the food in the middle of the window
food = [screen_height // 2 , screen_width // 2]

block = []


# Add the food by using the PI character of the curses module
window.addch(food[0], food[1], curses.ACS_PI)

# Set the initial movement direction
key = curses.KEY_RIGHT

# Define the character to represent the snake
snake_char = '>'


# Function to read the record from a file
def read_record():
    if os.path.exists("record.txt"):
        with open("record.txt", "r") as file:
            return int(file.read())
    else:
        return 0

# Function to write the record to a file
def write_record(record):
    with open("record.txt", "w") as file:
        file.write(str(record))


# Initialize score
score = 0

# Read the existing record from a file
Record = read_record()


# Create the game loop
while True:

    # Print the score at the top left corner
    window.addstr(0, 0, f"Score: {score}")

    window.addstr(0, 110, f"Record: {Record}")

    # Get the key pressed by the user
    next_key = window.getch()
    key = key if next_key == -1 else next_key

    # Update the snake character based on the direction
    if key == curses.KEY_RIGHT:
        snake_char = '>'
    elif key == curses.KEY_DOWN:
        snake_char = 'v'
    elif key == curses.KEY_UP:
        snake_char = '^'
    elif key == curses.KEY_LEFT:
        snake_char = '<'

    # Check if the snake collided with the wall or itself
    if (snake[0][0] in [0, screen_height - 1] or
            snake[0][1] in [0, screen_width - 1] or
            snake[0] in snake[1:]):
        curses.endwin()  # Close the window
        print("Game Over!")
        quit()  # Exit the program

    # Determine the new position of the snake's head
    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1

    # Insert the new head to the snake's body
    snake.insert(0, new_head)

    # Check if the snake ate the food
    if snake[0] == food:
        score += 10  # Increment the score
        food = None  # Remove the food if the snake ate it

        
        
        if score > Record:
            Record = score
            write_record(Record)

        # Generate new food in a random position
        while food is None:
            new_food = [
                random.randint(1, screen_height - 2),
                random.randint(1, screen_width - 2)
            ]
            new_block = [
                random.randint(5, screen_height - 3),
                random.randint(5, screen_width - 3)
            ] 
            # Ensure the new food is not placed on the snake
            food_chars = [curses.ACS_PI, curses.ACS_CKBOARD, curses.ACS_DIAMOND, curses.ACS_S1]
            food_char = random.choice(food_chars)
            food = new_food if new_food not in snake else None
        window.addch(food[0], food[1], food_char)
        
        block = new_block if new_block not in snake else None
        window.addch(block[0], block[1], curses.ACS_BLOCK)

   

    else:
        # Remove the last segment of the snake's body
        tail = snake.pop()
        window.addch(tail[0], tail[1], " ")

    # Add the new head to the screen
    window.addch(snake[0][0], snake[0][1], snake_char)
    if snake[0] == block :
        curses.endwin()  # Close the window
        print("Game Over!")
        quit()  # Exit the program