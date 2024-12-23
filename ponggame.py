import turtle

win = turtle.Screen()
win.title("Pong Game")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

TARGET_SCORE = 10

score_a = 0
score_b = 0
speed_multiplier = 1.0

class Paddle(turtle.Turtle):
    def __init__(self, x_pos):
        super().__init__()
        self.speed(0)
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=6, stretch_len=1)
        self.penup()
        self.goto(x_pos, 0)

    def move_up(self):
        y = self.ycor()
        if y < 250:
            self.sety(y + 20)

    def move_down(self):
        y = self.ycor()
        if y > -240:
            self.sety(y - 20)

paddle_a = Paddle(-350)
paddle_b = Paddle(350)

class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.shape("square")
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.dx = 0.3
        self.dy = 0.3

    def move(self):
        self.setx(self.xcor() + self.dx * speed_multiplier)
        self.sety(self.ycor() + self.dy * speed_multiplier)

    def reset_position(self):
        self.goto(0, 0)
        self.dx *= -1

ball = Ball()

class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 260)
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

scoreboard = Scoreboard()

def announce_winner(winner):
    win.textinput("Game Over", f"{winner} wins! Press Enter to restart.")
    restart_game()

def restart_game():
    global score_a, score_b, speed_multiplier
    score_a = 0
    score_b = 0
    speed_multiplier = 1.0
    ball.reset_position()
    paddle_a.goto(-350, 0)
    paddle_b.goto(350, 0)
    scoreboard.update_score()
    setup_keyboard()

def increase_speed():
    global speed_multiplier
    speed_multiplier += 0.1
    if speed_multiplier > 2.0:
        speed_multiplier = 2.0

def decrease_speed():
    global speed_multiplier
    speed_multiplier -= 0.1
    if speed_multiplier < 0.5:
        speed_multiplier = 0.5

def setup_keyboard():
    win.listen()
    win.onkeypress(paddle_a.move_up, "w")
    win.onkeypress(paddle_a.move_down, "s")
    win.onkeypress(paddle_b.move_up, "Up")
    win.onkeypress(paddle_b.move_down, "Down")
    win.onkeypress(increase_speed, "+")
    win.onkeypress(decrease_speed, "-")

setup_keyboard()

while True:
    win.update()

    ball.move()

    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.reset_position()
        score_a += 1
        scoreboard.update_score()
        if score_a == TARGET_SCORE:
            announce_winner("Player A")

    if ball.xcor() < -390:
        ball.reset_position()
        score_b += 1
        scoreboard.update_score()
        if score_b == TARGET_SCORE:
            announce_winner("Player B")

    if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1

    if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.setx(-340)
        ball.dx *= -1
