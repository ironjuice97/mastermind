import turtle
import random
from Marble import Marble  # Assuming custom class for representing a marble
from Point import Point    # Assuming custom class for representing a point

# Constants
SCREEN_WIDTH = 1005  # Width of the entire game screen
SCREEN_HEIGHT = 768  # Height of the entire game screen
BOARD_WIDTH = 400    # Width of the guess board
BOARD_HEIGHT = SCREEN_HEIGHT - 175
  # Height of the guess board, calculated from screen height
LEADERBOARD_WIDTH = 330  # Width of the leaderboard section
LEADERBOARD_HEIGHT = BOARD_HEIGHT  # Height of the leaderboard, same as the guess board
COLOR_PALETTE_HEIGHT = 120  # Height of the color palette section
MARBLE_RADIUS = 15  # Radius of each marble
MARBLE_SPACING = MARBLE_RADIUS + 10  # Space between marbles
GUESS_MARBLE_OFFSET_X = -SCREEN_WIDTH // 3  # X-offset for placing guess marbles
GUESS_MARBLE_OFFSET_Y = SCREEN_HEIGHT // 2 - MARBLE_SPACING  # Y-offset for placing guess marbles
COLORS = ["red", "green", "blue", "yellow", "purple", "black"]  # List of available colors

# Set up the screen
wn = turtle.Screen()  # Create a turtle screen object
wn.title("CS5001 MasterMind Code Game")  # Set the title of the window
wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)  # Set up the window size
wn.bgcolor("white")  # Set the background color of the window
wn.tracer(0)  # Turn off animation for instant drawing

# Register button shapes
wn.register_shape("checkbutton.gif")
wn.register_shape("quit.gif")
wn.register_shape("xbutton.gif")

# Initialize game variables
secret_code = [random.choice(COLORS) for _ in range(4)]  # A list of 4 unique random colors
guesses = []
results = []
tries = 0
current_guess_marbles = []
current_guess_colors = []


def draw_guess_board():
    border = turtle.Turtle()
    border.penup()
    border.color("black")  # Set the pen color to black for the border
    border.pensize(5)  # Set the pensize to make the border more visible

    # Adjust the start position further to the left by subtracting from the x-coordinate
    extend_left = 100  # Amount by which to extend the border to the left
    border_start_x = GUESS_MARBLE_OFFSET_X - MARBLE_RADIUS - extend_left
    border_start_y = GUESS_MARBLE_OFFSET_Y + MARBLE_RADIUS

    border.goto(border_start_x, border_start_y)
    border.pendown()
    
    # Increase the total width of the board to account for the extended left border
    extended_border_width = BOARD_WIDTH + extend_left

    # Draw the rectangular border
    border.forward(extended_border_width)  # Draw the bottom border line
    border.right(90)
    border.forward(BOARD_HEIGHT)
    border.right(90)
    border.forward(extended_border_width)  # Draw the top border line
    border.right(90)
    border.forward(BOARD_HEIGHT)
    border.hideturtle()

    guess_board = turtle.Turtle()
    guess_board.hideturtle()
    guess_board.speed('fastest')
    for row in range(10):
        for col in range(4):
            guess_board.penup()
            x = GUESS_MARBLE_OFFSET_X + col * (2 * MARBLE_SPACING) - 40 # Add a value to move right
            y = GUESS_MARBLE_OFFSET_Y - row * (2 * MARBLE_SPACING) - 50  # Subtract a value to move down
            guess_board.goto(x, y - MARBLE_RADIUS)
            guess_board.pendown()
            guess_board.circle(MARBLE_RADIUS)  # Draw the circle with an outline
        
        # Adjust feedback circles position and size
        feedback_offset_x = 80  # Adjust this value as needed to move the feedback circles to the right
        feedback_circle_radius = MARBLE_RADIUS // 3  # Making the feedback circles smaller
        feedback_circle_spacing = MARBLE_SPACING // 1.75  # Adjust spacing between feedback circles
        for i in range(2):  # Two columns of feedback circles
            for j in range(2):  # Two feedback circles per column
                # Adjust feedback circle position with feedback_offset_x and feedback_circle_spacing
                feedback_x = x + (2 * MARBLE_RADIUS) + feedback_offset_x + (i * feedback_circle_spacing) 
                feedback_y = y - MARBLE_RADIUS + (j * feedback_circle_spacing) 
                guess_board.penup()
                guess_board.goto(feedback_x, feedback_y)
                guess_board.pendown()
                guess_board.circle(feedback_circle_radius)  # Draw smaller feedback circle

def draw_leaderboard():
    leaderboard_border = turtle.Turtle()  # Create a turtle for the leaderboard border
    leaderboard_border.hideturtle()  # Hide the turtle
    leaderboard_border.speed('fastest')  # Set the drawing speed to fastest
    leaderboard_border.penup()  # Lift the pen
    leaderboard_border.pencolor("dark blue")  # Set the pencolor to dark blue
    leaderboard_border.pensize(5)  # Set the pensize to make the border more visible

    # Position the turtle at the top-left corner of the leaderboard
    leaderboard_border.goto(GUESS_MARBLE_OFFSET_X + BOARD_WIDTH + 50, GUESS_MARBLE_OFFSET_Y + MARBLE_RADIUS)
    leaderboard_border.pendown()  # Begin drawing the border

    # Draw the dark blue rectangular border
    for _ in range(2):
        leaderboard_border.forward(LEADERBOARD_WIDTH)
        leaderboard_border.right(90)
        leaderboard_border.forward(LEADERBOARD_HEIGHT)
        leaderboard_border.right(90)
    leaderboard_border.hideturtle()  # Hide the border turtle

   # Now, add text to the leaderboard
    leaderboard_text = turtle.Turtle()
    leaderboard_text.hideturtle()
    leaderboard_text.penup()
    leaderboard_text.color("dark blue")  # Set the text color to dark blue for visibility

    # Make sure the position is within the visible area of the leaderboard
    text_x = GUESS_MARBLE_OFFSET_X + BOARD_WIDTH + 60  # X coordinate within the leaderboard
    text_y = GUESS_MARBLE_OFFSET_Y + MARBLE_RADIUS - 40  # Y coordinate within the leaderboard
    
    leaderboard_text.goto(text_x, text_y)
    leaderboard_text.write("Leaders:", align="left", font=("Arial", 24, "bold"))

# Adjusted function to draw the color palette with a border
def draw_color_pallete_board():
    color_palette = turtle.Turtle()
    color_palette.hideturtle()
    color_palette.speed('fastest')
    color_palette.penup()

    # Define the starting position for the color palette border
    palette_x = -SCREEN_WIDTH // 2 + 50  # This should be aligned with the left side of the color palette
    palette_y = -SCREEN_HEIGHT // 2 + 20  # This should be just below the color palette

    # Set the dimensions of the color palette border
    palette_width = SCREEN_WIDTH - 100  # Adjust if necessary to span the width of the color palette area
    palette_height = COLOR_PALETTE_HEIGHT  # Set to the height of the color palette area

    # Draw the border for the color palette
    palette_border = turtle.Turtle()
    palette_border.hideturtle()
    palette_border.speed('fastest')
    palette_border.penup()
    palette_border.pencolor("black")  # Set the pencolor for the palette border
    palette_border.pensize(5)  # Set the pensize for visibility
    palette_border.goto(palette_x, palette_y)
    palette_border.pendown()
    for _ in range(2):
        palette_border.forward(palette_width)
        palette_border.left(90)
        palette_border.forward(palette_height)
        palette_border.left(90)
    palette_border.hideturtle()

    # Adjust these values to move the color dots
    base_x = -SCREEN_WIDTH // 2 + 75   # Increase or decrease to move left or right
    base_y = palette_y + 55  # Increase or decrease to move up or down

    # Draw the color dots
    for i, color in enumerate(COLORS):
        color_palette.goto(base_x + i * (2 * MARBLE_SPACING), base_y - MARBLE_RADIUS)
        color_palette.pendown()
        color_palette.color('black', color)  # Set the border and fill color
        color_palette.begin_fill()
        color_palette.circle(MARBLE_RADIUS)  # Draw the circle with a radius of MARBLE_RADIUS
        color_palette.end_fill()
        color_palette.penup()
    
    wn.update()  # Update the window to show the drawn elements

def draw_buttons():
    # Define button positions independently
    check_button_y = -SCREEN_HEIGHT // 2 + 70
    x_button_y = -SCREEN_HEIGHT // 2 + 70
    quit_button_y = -SCREEN_HEIGHT // 2 + 70

    # Create and position the Check button
    check_button = turtle.Turtle()
    check_button.shape("checkbutton.gif")
    check_button.penup()
    check_button.goto(-100, check_button_y)  # Adjust the x coordinate as needed
    check_button.onclick(on_check_button_click)

    # Create and position the X button
    x_button = turtle.Turtle()
    x_button.shape("xbutton.gif")
    x_button.penup()
    x_button.goto(0, x_button_y)  # Adjust the x coordinate as needed
    x_button.onclick(on_x_button_click)

    # Create and position the Quit button
    quit_button = turtle.Turtle()
    quit_button.shape("quit.gif")
    quit_button.penup()
    quit_button.goto(350, quit_button_y)  # Adjust the x coordinate as needed
    quit_button.onclick(on_quit_button_click)

    wn.update()

def on_check_button_click(x, y):
    # Placeholder function for check button click
    print("Check button clicked")

def on_x_button_click(x, y):
    # Placeholder function for X button click
    print("X button clicked")

def on_quit_button_click(x, y):
    # Placeholder function for quit button click
    print("Quit button clicked")
    turtle.bye()

# Call the drawing functions
draw_guess_board()
draw_leaderboard()
draw_color_pallete_board()
draw_buttons()

# Main loop
wn.mainloop()