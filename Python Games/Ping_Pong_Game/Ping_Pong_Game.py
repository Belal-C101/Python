import turtle

# Setup screen game
wind = turtle.Screen() # Initialize the screen
wind.title("Ping Pong Game By Belal Tamer") # Set the title of the window
wind.bgcolor("black") # Set the background color 
wind.setup(width=1280, height=720) # Set the size of the window

# Madrab 1
madrab1 = turtle.Turtle() # Initialize the turtle
madrab1.speed(0)
madrab1.shape("square")
madrab1.color("blue")
madrab1.shapesize(stretch_wid=5, stretch_len=1)
madrab1.penup()
madrab1.goto(-600, 0)

# Madrab 2
madrab2 = turtle.Turtle() # Initialize the turtle
madrab2.speed(0) # Set the speed
madrab2.shape("square") # Set the shape
madrab2.color("red") # Set the color
madrab2.shapesize(stretch_wid=5, stretch_len=1) # Stretch the object
madrab2.penup() # Remove the lines 
madrab2.goto(600, 0) # Set the 

# Score
score1 = 0
score2 = 0
score = turtle.Turtle() # Initialize the turtle
score.speed(0)
score.color("white")
score.penup() 
score.hideturtle()
score.goto(0, 320)
score.write("Player 1 : 0    Player 2 : 0", align="center", font=("Courier", 24, "normal"))

# Ball
ball = turtle.Turtle() # Initialize the turtle
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 5
ball.dy = 5

# Function madrab 1
def madrab1_up():
    y = madrab1.ycor()
    y += 20
    madrab1.sety(y)

def madrab1_down():
    y = madrab1.ycor()
    y -= 20
    madrab1.sety(y)

# Key bindings
wind.listen()
wind.onkeypress(madrab1_up, "w")
wind.onkeypress(madrab1_down, "s")

# Function madrab 2
def madrab2_up():
    y = madrab2.ycor()
    y += 20
    madrab2.sety(y)

def madrab2_down():
    y = madrab2.ycor()
    y -= 20
    madrab2.sety(y)

# Key bindings
wind.listen()
wind.onkeypress(madrab2_up, "Up")
wind.onkeypress(madrab2_down, "Down")

# Quit game when press "Esc"
def quit_game():
    wind.bye()

wind.listen()
wind.onkeypress(quit_game, "Escape")

# Game loop
try:
    while True:
        wind.update() # Update the loop every time the loop runs

        # Ball movement
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Border check
        # If ball collides with upper wall
        if ball.ycor() > 330:
            ball.sety(330)
            ball.dy *= -1

        if ball.ycor() < -330:
            ball.sety(-330)
            ball.dy *= -1

        # If madrab 1 collides with upper wall
        if madrab1.ycor() > 300:
            madrab1.sety(300)

        if madrab1.ycor() < -300:
            madrab1.sety(-300)

        # If madrab 2 collides with upper wall
        if madrab2.ycor() > 300:
            madrab2.sety(300)

        if madrab2.ycor() < -300:
            madrab2.sety(-300)

        # If ball collides with side walls
        if ball.xcor() > 630:
            ball.goto(0, 0)
            ball.dx *= -1
            score1 += 1
            score.clear()
            score.write("Player 1 : {}    Player 2 : {}".format(score1, score2), align="center", font=("Courier", 24, "normal"))

        if ball.xcor() < -630:
            ball.goto(0, 0)
            ball.dx *= -1
            score2 += 1
            score.clear()
            score.write("Player 1 : {}    Player 2 : {}".format(score1, score2), align="center", font=("Courier", 24, "normal"))

        # Madrab and ball collision
        if ball.xcor() > 580 and ball.xcor() < 600 and ball.ycor() < madrab2.ycor() + 40 and ball.ycor() > madrab2.ycor() - 40:
            ball.setx(580)
            ball.dx *= -1

        if ball.xcor() < -580 and ball.xcor() > -600 and ball.ycor() < madrab1.ycor() + 40 and ball.ycor() > madrab1.ycor() - 40:
            ball.setx(-580)
            ball.dx *= -1

        # End the game when scoring 10
        if score1 == 10 or score2 == 10:
            quit_game()
except turtle.Terminator:
    print("Game has been terminated.")
