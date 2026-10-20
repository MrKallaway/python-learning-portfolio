import random
import tkinter as tk

# CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
PLAYER_SIZE = 36
STAR_SIZE = 22
STAR_POINTS = 10
MAX_LIVES = 3
MOVE_DISTANCE = 24

root = tk.Tk()
root.title("Variable Voyage")
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="midnight blue")
canvas.pack()

# VARIABLES
player_name = "Pilot"
score = 0
lives = MAX_LIVES
game_running = True

player = canvas.create_rectangle(
    60,
    WINDOW_HEIGHT // 2,
    60 + PLAYER_SIZE,
    WINDOW_HEIGHT // 2 + PLAYER_SIZE,
    fill="cyan",
)

star = canvas.create_oval(0, 0, STAR_SIZE, STAR_SIZE, fill="gold")

player_label = tk.Label(canvas, text=f"Player name: {player_name}")
score_label = tk.Label(canvas, text=f"Score: {str(score)}")
lives_label = tk.Label(canvas, text=f"lives: {str(lives)}")

canvas.create_window(10, 10, window=player_label, anchor="nw")
canvas.create_window(10, 30, window=score_label, anchor="nw")
canvas.create_window(10, 50, window=lives_label, anchor="nw")


def move_star():
    """moves the star to a random place on the window"""
    x = random.randint(100, WINDOW_WIDTH - STAR_SIZE)
    y = random.randint(40, WINDOW_HEIGHT - STAR_SIZE)

    canvas.coords(star, x, y, x+STAR_SIZE, y+STAR_SIZE)


def move_player(dx, dy):
    """moves the player to the given coordinates"""
    # TODO 1: move the player using canvas.move()

    canvas.move(player, dx, dy)

    pass


def check_collision():
    """checks if the player collides with the star,
    if it does then it adds STAR_POINTS to the score
    and moves the star"""
    global score
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
        # and then move the star elsewhere
        move_star()


def update_hud():
    """updates the hud text to the current variables' values"""
    # TODO 3: display player_name, score and lives
    # use str() or an f-string to convert numbers to display text
    
    player_label["text"] = f"Player name: {player_name}"
    score_label["text"] = f"Score: {str(score)}"
    lives_label["text"] = f"Lives: {str(lives)}"


def game_loop():
    """the core game loop"""
    if game_running:
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