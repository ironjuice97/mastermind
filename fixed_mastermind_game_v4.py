import turtle
import random
from Marble import Marble
from Point import Point

# Constants
COLORS = ["#ff0000", "#0000ff", "#008000", "#ffff00", "#800080", "#000000"]
MAX_TRIES = 10
MARBLE_RADIUS = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCOREBOARD_WIDTH = 200
SCOREBOARD_HEIGHT = SCREEN_HEIGHT // 2
MARBLE_OFFSET_X = -200
MARBLE_OFFSET_Y = -200
MARBLE_SPACING = 10
BOARD_X = -340  # Adjusted for the guess circles to start from the left
BOARD_Y = 260   # Adjusted for the guess circles to start from the top
SCOREBOARD_X = SCREEN_WIDTH / 2 - SCOREBOARD_WIDTH / 2
SCOREBOARD_Y = SCOREBOARD_HEIGHT / 2 - SCREEN_HEIGHT / 2

BOARD_BOX_WIDTH = 680
BOARD_BOX_HEIGHT = 1294
SCOREBOARD_BOX_WIDTH = 170
SCOREBOARD_BOX_HEIGHT = 431
COLOR_BUTTONS_BOX_WIDTH = BOARD_BOX_WIDTH
COLOR_BUTTONS_BOX_HEIGHT = 100  # Height for the color buttons box

# Initialize the game window
wn = turtle.Screen()
wn.title("Mastermind Game")
wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
wn.tracer(0)  # Turn off animation

# Initialize game variables
secret_code = [random.choice(COLORS) for _ in range(4)]  # A list of 4 unique random colors
guesses = []
results = []
tries = 0
current_guess = []

# Register GIF assets
button_images = [
    'checkbutton.gif', 'xbutton.gif', 'quit.gif',
    'file_error.gif', 'leaderboard_error.gif',
    'lose.gif', 'quitmsg.gif', 'winner.gif'
]
for image in button_images:
    wn.addshape(image)

# Create Turtles for each button
check_button = turtle.Turtle('checkbutton.gif')
x_button = turtle.Turtle('xbutton.gif')
quit_button = turtle.Turtle('quit.gif')

check_button.penup()
x_button.penup()
quit_button.penup()

check_button.goto(-100, -250)  # Position of the check button
x_button.goto(-50, -250)  # Position of the x button
quit_button.goto(350, -250)  # Position of the quit button

# Make sure all buttons are shown
check_button.showturtle()
x_button.showturtle()
quit_button.showturtle()

# Turtle for drawing the board and messages
board_turtle = turtle.Turtle()
board_turtle.hideturtle()
board_turtle.penup()

# Scoreboard turtle created outside the function
scoreboard_turtle = turtle.Turtle()
scoreboard_turtle.hideturtle()
scoreboard_turtle.penup()

def bind_color_buttons():
    start_x = -340  # Adjust this to place color buttons at the correct position
    start_y = -270  # Adjust this to place color buttons at the correct position
    for i, color in enumerate(COLORS):
        button_turtle = turtle.Turtle()
        button_turtle.shape("circle")
        button_turtle.shapesize(stretch_wid=MARBLE_RADIUS/10, stretch_len=MARBLE_RADIUS/10)
        button_turtle.color(color)
        button_turtle.penup()
        button_turtle.goto(start_x + i * 50, start_y)
        # Here we bind the on_color_button_click function to the turtle's click event
        button_turtle.onclick(lambda x, y, color=color: on_color_button_click(color))


# Helper function to draw a box around an area
def draw_box(turtle, x, y, width, height, color="black"):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.color(color)
    for _ in range(2):
        turtle.forward(width)
        turtle.right(90)
        turtle.forward(height)
        turtle.right(90)
    turtle.penup()

# Functions to draw the game board, scoreboard, and color buttons with boxes
def draw_board_with_box():
    draw_board()  # Your existing function to draw the board
    # Calculate the top-left corner of the box
    box_x = BOARD_X - (BOARD_BOX_WIDTH // 2)
    box_y = BOARD_Y + (BOARD_BOX_HEIGHT // 2)
    draw_box(board_turtle, box_x, box_y, BOARD_BOX_WIDTH, -BOARD_BOX_HEIGHT)

def draw_scoreboard_with_box():
    draw_scoreboard()  # Your existing function to draw the scoreboard
    # Calculate the top-left corner of the box
    box_x = SCOREBOARD_X - (SCOREBOARD_BOX_WIDTH // 2)
    box_y = SCOREBOARD_Y + (SCOREBOARD_BOX_HEIGHT // 2)
    draw_box(scoreboard_turtle, box_x, box_y, SCOREBOARD_BOX_WIDTH, -SCOREBOARD_BOX_HEIGHT)

def draw_color_buttons_with_box():
    draw_color_buttons()  # Your existing function to draw the color buttons
    # Calculate the top-left corner of the box
    box_x = -SCREEN_WIDTH // 2 + 10
    box_y = -SCREEN_HEIGHT // 2 + COLOR_BUTTONS_BOX_HEIGHT - 10
    draw_box(board_turtle, box_x, box_y, COLOR_BUTTONS_BOX_WIDTH, COLOR_BUTTONS_BOX_HEIGHT)


# Functions
def draw_board():
    board_turtle.clear()
    top_left_x = BOARD_X
    top_left_y = BOARD_Y
    
    # Draw the guess circles
    for i in range(MAX_TRIES):
        for j in range(4):
            x = top_left_x + j * MARBLE_SPACING + j * (MARBLE_RADIUS * 2)
            y = top_left_y - i * MARBLE_SPACING - i * (MARBLE_RADIUS * 2)
            board_turtle.penup()
            board_turtle.goto(x, y)
            board_turtle.dot(MARBLE_RADIUS * 2, "black")
    
    # Draw the result circles
    result_x_start = top_left_x + 4 * (MARBLE_RADIUS * 2 + MARBLE_SPACING) + MARBLE_SPACING
    for i in range(MAX_TRIES):
        for j in range(2):  # Usually, there are only 2 result circles, modify as needed
            x = result_x_start + (j % 2) * MARBLE_RADIUS
            y = top_left_y - i * (MARBLE_RADIUS * 2 + MARBLE_SPACING)
            board_turtle.penup()
            board_turtle.goto(x, y)
            board_turtle.dot(MARBLE_RADIUS, "black")  # Modify color if needed
    wn.update()

def draw_scoreboard():
    SCOREBOARD_X = SCREEN_WIDTH / 2 - SCOREBOARD_WIDTH / 2
    SCOREBOARD_Y = SCOREBOARD_HEIGHT / 2 - SCREEN_HEIGHT / 2
    scoreboard_turtle.speed(0)
    scoreboard_turtle.color("black")
    scoreboard_turtle.goto(SCOREBOARD_X, SCOREBOARD_HEIGHT // 2)
    scoreboard_turtle.pendown()
    scoreboard_turtle.forward(SCOREBOARD_WIDTH)
    scoreboard_turtle.right(90)
    scoreboard_turtle.forward(SCOREBOARD_HEIGHT)
    scoreboard_turtle.right(90)
    scoreboard_turtle.forward(SCOREBOARD_WIDTH)
    scoreboard_turtle.right(90)
    scoreboard_turtle.forward(SCOREBOARD_HEIGHT)
    scoreboard_turtle.hideturtle()
    
    # Add the "Leaders" title inside the scoreboard
    scoreboard_turtle.penup()
    scoreboard_turtle.goto(SCOREBOARD_X + 50, SCOREBOARD_HEIGHT // 2 - 30)
    scoreboard_turtle.write("Leaders:", font=("Arial", 16, "bold"))
    
    # Placeholder for leader names and scores
    leaders = [("Alice", 3), ("Bob", 5), ("Carol", 7)]
    for i, leader in enumerate(leaders):
        scoreboard_turtle.goto(SCOREBOARD_X + 10, SCOREBOARD_HEIGHT // 2 - 60 - (i * 20))
        scoreboard_turtle.write(f"{leader[0]} : {leader[1]}", font=("Arial", 14, "normal"))

    wn.update()

def draw_marble(marble):
    marble.turtle.fillcolor('')  # Ensure the fill color is set to none
    marble.turtle.penup()
    marble.turtle.goto(marble.position.x, marble.position.y)
    marble.turtle.pendown()
    marble.turtle.pensize(1)  # Set the border thickness
    marble.turtle.pencolor('black')  # Set the border color
    for _ in range(4):  # Draw a square
        marble.turtle.forward(100)  # Move forward by 100px
        marble.turtle.right(90)  # Turn right by 90 degrees
    marble.turtle.penup()

def draw_guess():
    global current_guess
    for marble in current_guess:
        draw_marble(marble)

def draw_results():
    for i, result in enumerate(results):
        bulls, cows = result
        for b in range(bulls):  # Black dots for correct position and color
            x = -100 + b * (MARBLE_RADIUS + 5)
            y = 250 - i * (2 * MARBLE_RADIUS + 10)
            board_turtle.goto(x, y)
            board_turtle.dot(MARBLE_RADIUS, "black")
        for c in range(cows):  # White dots for correct color, wrong position
            x = -100 + (bulls + c) * (MARBLE_RADIUS + 5)
            y = 250 - i * (2 * MARBLE_RADIUS + 10)
            board_turtle.goto(x, y)
            board_turtle.dot(MARBLE_RADIUS, "black")
    wn.update()

def show_message(message):
    board_turtle.clear()  # Clear any previous message first
    board_turtle.goto(0, -SCREEN_HEIGHT // 2 + 20)
    board_turtle.write(message, align="center", font=("Arial", 16, "normal"))
    wn.update()

def check_guess():
    global current_guess, secret_code, tries
    tries += 1
    bulls = sum(1 for g, s in zip(current_guess, secret_code) if g.color == s)
    cows = sum(min(current_guess.count(c.color), secret_code.count(c)) for c in set(current_guess)) - bulls
    current_guess = []  # Clear current guess after checking
    return bulls, cows

def on_x_button_click(x, y):
    global current_guess
    current_guess = []
    draw_board()  # Redraw the board to clear the previous guesses
    show_message("Guess cleared.")  # Give feedback that the guess was cleared

def on_check_button_click(x, y):
    global current_guess, guesses, results, tries
    if len(current_guess) < 4:
        show_message("Incomplete guess! Please select 4 colors.")
        return
    bulls, cows = check_guess()
    results.append((bulls, cows))
    draw_guess()
    draw_results()

    if bulls == 4:
        show_message("Congratulations! You've won!")
        wn.onscreenclick(None)  # Disable further clicks
    elif tries >= MAX_TRIES:
        show_message("Game over! You've used all your tries.")
        wn.onscreenclick(None)  # Disable further clicks

    current_guess = []

def on_quit_button_click(x, y):
    wn.bye()

def draw_color_buttons():
    start_x = -340  # Adjust this to place color buttons at the correct position
    start_y = -270  # Adjust this to place color buttons at the correct position
    for i, color in enumerate(COLORS):
        button_turtle = turtle.Turtle()
        button_turtle.shape("circle")
        button_turtle.shapesize(stretch_wid=MARBLE_RADIUS/10, stretch_len=MARBLE_RADIUS/10)
        button_turtle.color(color)
        button_turtle.penup()
        button_turtle.goto(start_x + i * 50, start_y)
        button_turtle.onclick(lambda x, y, color=color: on_color_button_click(color))
        wn.update()

def bind_button_clicks():
    check_button.onclick(on_check_button_click)
    x_button.onclick(on_x_button_click)
    quit_button.onclick(on_quit_button_click)

def on_color_button_click(color):
    if len(current_guess) < 4:
        marble_position = Point(MARBLE_OFFSET_X + len(current_guess) * (MARBLE_RADIUS * 2 + MARBLE_SPACING), MARBLE_OFFSET_Y)
        marble = Marble(marble_position, color, MARBLE_RADIUS)
        current_guess.append(marble)
        draw_marble(marble)

# Update the initialize_game function
def initialize_game_with_boxes():
    draw_board_with_box()
    draw_color_buttons_with_box()
    draw_scoreboard_with_box()
    bind_button_clicks()
    bind_color_buttons()
    # Finally, update the screen after all drawing commands
    wn.update()

# Main program
player_name = wn.textinput("Mastermind Game", "Enter your name:")
if not player_name:
    player_name = "Player"

# Clear the input dialog
turtle.clear()

# Initialize the game
initialize_game_with_boxes()

wn.mainloop()
