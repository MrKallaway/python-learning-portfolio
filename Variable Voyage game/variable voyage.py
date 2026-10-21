import random
import tkinter as tk

# CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
PLAYER_SIZE = 36
STAR_SIZE = 22
STAR_POINTS = 10
HAZARD_SIZE = 52
MAX_LIVES = 3
MOVE_DISTANCE = 24
TIMER_START = 60
DEFAULT_DELAY = 20


root = tk.Tk()
root.title("Variable Voyage")
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="midnight blue")
canvas.pack()

# VARIABLES
player_name = "Pilot"
score = 0
lives = MAX_LIVES
difficulty = 1
time_left = TIMER_START
delay = DEFAULT_DELAY
game_over = False
game_running = True

player = canvas.create_rectangle(
    60,
    WINDOW_HEIGHT // 2,
    60 + PLAYER_SIZE,
    WINDOW_HEIGHT // 2 + PLAYER_SIZE,
    fill="cyan",
)

star = canvas.create_oval(0, 0, STAR_SIZE, STAR_SIZE, fill="gold")
hazard = canvas.create_oval(0, 0, HAZARD_SIZE, HAZARD_SIZE, fill="red")

player_label = tk.Label(canvas, text=f"Player name: {player_name}")
score_label = tk.Label(canvas, text=f"Score: {str(score)}")
lives_label = tk.Label(canvas, text=f"lives: {str(lives)}")
difficulty_label = tk.Label(canvas, text=f"Difficulty: {str(difficulty)}")

timer_label = tk.Label(canvas, text=f"Time left: {str(time_left)}")

canvas.create_window(10, 10, window=player_label, anchor="nw")
canvas.create_window(10, 30, window=score_label, anchor="nw")
canvas.create_window(10, 50, window=lives_label, anchor="nw")
canvas.create_window(10, 50, window=difficulty_label, anchor="nw")

canvas.create_window(800, 10, window=timer_label, anchor="ne")


def move_star():
    """moves the star to a random place on the window"""
    x = random.randint(100, WINDOW_WIDTH - STAR_SIZE)
    y = random.randint(40, WINDOW_HEIGHT - STAR_SIZE)

    # applies the randomised coordinates to the star
    canvas.coords(star, x, y, x+STAR_SIZE, y+STAR_SIZE)



    # and the same with the hazard
    x2 = random.randint(100, WINDOW_WIDTH - HAZARD_SIZE)
    y2 = random.randint(40, WINDOW_HEIGHT - HAZARD_SIZE)
        
    canvas.coords(hazard, x2, y2, x2+HAZARD_SIZE, y2+HAZARD_SIZE)



    # to make sure the hazard does not spawn on top of the player:
    # gets the bounding box of the hazard
    hazard_coords = canvas.coords(hazard)
    
    # finds all items overlapping with these coordinates
    overlapping_items = canvas.find_overlapping(*hazard_coords)
    while star in overlapping_items or player in overlapping_items:
        x2 = random.randint(100, WINDOW_WIDTH - HAZARD_SIZE)
        y2 = random.randint(40, WINDOW_HEIGHT - HAZARD_SIZE)
        canvas.coords(hazard, x2, y2, x2+HAZARD_SIZE, y2+HAZARD_SIZE)




def move_player(dx, dy):
    """moves the player to the given coordinates"""

    # TODO 1: move the player using canvas.move()

    canvas.move(player, dx, dy)

    pass


def check_collision():
    """checks if the player collides with the star,
    if it does then it adds STAR_POINTS to the score
    and moves the star"""

    global score, lives, difficulty

    # TODO 2: compare the player's coordinates with the star
    # if they touch, add STAR_POINTS to score and move the star


    # gets the bounding box of the player
    player_coords = canvas.coords(player)
    
    # finds all items overlapping with these coordinates
    overlapping_items = canvas.find_overlapping(*player_coords)

    # check if the star is in that list
    if star in overlapping_items:
        # because it is in the list, add to the score
        score += STAR_POINTS
        difficulty = score/60
        # and then move the star elsewhere
        move_star()

    # check if a hazard is in the list
    if hazard in overlapping_items:
        # remove a life
        lives -= 1
        move_star()




def update_hud():
    """updates the hud text to the current variables' values"""

    # TODO 3: display player_name, score and lives
    # use str() or an f-string to convert numbers to display text

    global time_left, delay, game_over

    delay -= 1
    if delay == 0:
        time_left -= 1
        delay = DEFAULT_DELAY

    player_label["text"] = f"Player name: {player_name}"
    score_label["text"] = f"Score: {str(score)}"
    lives_label["text"] = f"Lives: {str(lives)}"
    timer_label["text"] = f"Time left: {str(time_left)}"
    difficulty_label["text"] = f"Difficulty: {str(difficulty)}"

    if time_left <= 0 or lives <= 0:
        game_over = True



def game_loop():
    """the core game loop"""
    global game_running
    if game_running:
        if game_over == True:
            game_over_label = tk.Label(canvas, text="GAME OVER", font=("Consolas", 30))
            canvas.create_window(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, window=game_over_label, anchor="center")
            game_running = False
        check_collision()
        update_hud()
        root.after(50, game_loop)


root.bind("<Left>", lambda event: move_player(-MOVE_DISTANCE, 0))
root.bind("<Right>", lambda event: move_player(MOVE_DISTANCE, 0))
root.bind("<Up>", lambda event: move_player(0, -MOVE_DISTANCE))
root.bind("<Down>", lambda event: move_player(0, MOVE_DISTANCE))

move_star()
game_loop()
root.mainloop()
