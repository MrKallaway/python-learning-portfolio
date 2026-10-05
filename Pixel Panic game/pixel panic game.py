"""
Reccomended install:
    pip install pillow pygame

the game still runs without pygame on windows by using winsound. On other systems, it falls back to a simple Tkinter bell if no audio backend is available.

Controls:
    ENTER = start
    LEFT/RIGHT/UP/DOWN or WASD = move
    P = pause/resume
    R = restart
    M = mute/unmute sound
"""

from __future__ import annotations

import json
import os
import random
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog, messagebox

try:
    from PIL import Image, ImageTk
except ImportError as exc:
    raise SystemExit("Install Pillow first: pip install pillow") from exc

WIDTH = 960
HEIGHT = 600
BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "assets"
SOUND_DIR = BASE_DIR / "sounds"
SAVE_FILE = BASE_DIR / "pixel_panic_sound_high_score.json"


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class SoundManager:
    # small sound manager using pygame if available, otherwise use winsound on windows

    def __init__(self, root: tk.Tk):
        self.root = root
        self.muted: bool = False
        self.backend: str = "bell"
        self.pygame = None
        self.winsound = None
        self.sounds = {}
        self._load_backend()

    def _load_backend(self):
        os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
        try:
            import pygame
            pygame.mixer.init()
            self.pygame = pygame
            self.backend = "pygame"
            for path in SOUND_DIR.glob("*.wav"):
                self.sounds[path.stem] = pygame.mixer.Sound(str(path))
            return
        except Exception:
            pass

        try:
            import winsound
            self.winsound = winsound
            self.backend = "winsound"
        except Exception:
            self.backend = "bell"

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted and self.pygame:
            self.pygame.mixer.stop()

    def play(self, name: str):
        if self.muted:
            return
        path = SOUND_DIR / f"{name}.wav"
        try:
            if self.backend == "pygame" and name in self.sounds:
                self.sounds[name].play()
            elif self.backend == "winsound" and path.exists():
                self.winsound.PlaySound(str(path), self.winsound.SND_FILENAME | self.winsound.SND_ASYNC)
            else:
                self.root.bell()
        except Exception:
            self.root.bell()


class FallingSprite:
    # one falling visual object: star, glitch, shield orb or super star.

    def __init__(self, game, kind: str, speed: float, image, score_value: int = 0):
        self.game = game
        self.canvas = game.canvas
        self.kind = kind
        self.speed = speed
        self.image = image
        self.score_value = score_value
        self.item_id = self.canvas.create_image(0, 0, image=self.image)
        self.spawn()

    def spawn(self):
        x = random.randint(48, WIDTH - 48)
        y = random.randint(-760, -45)
        self.canvas.coords(self.item_id, x, y)

    def move(self, multiplier: float):
        self.canvas.move(self.item_id, 0, self.speed * multiplier)

    def reset(self, extra_speed: float = 0.0):
        self.speed += extra_speed
        self.spawn()

    def off_screen(self) -> bool:
        return self.canvas.coords(self.item_id)[1] > HEIGHT + 70

    def bbox(self):
        return self.canvas.bbox(self.item_id)

    def position(self):
        return self.canvas.coords(self.item_id)


class PixelPanicSoundGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pixel Panic: Sound + Visual Advanced Edition")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0, bg="#070b18")
        self.canvas.pack()

        self.sfx = SoundManager(self.root)

        # Standard data types used in the game
        self.player_name: str = "Pilot"       # string
        self.score: int = 0                   # integer
        self.combo: int = 0                   # integer
        self.multiplier: int = 1              # integer
        self.lives: int = 3                   # integer
        self.level: int = 1                   # integer
        self.player_speed: float = 16.5        # float
        self.difficulty: float = 1.0          # float
        self.shield_active: bool = False      # boolean
        self.is_running: bool = False         # boolean
        self.is_paused: bool = False          # boolean
        self.shield_timer: int = 0            # integer
        
        self.high_score: int = self.load_high_score()
        self.starfield: list[int] = []
        self.particles: list[tuple[int, int, int]] = []
        self.stars: list[FallingSprite] = []
        self.glitches: list[FallingSprite] = []
        self.powerups: list[FallingSprite] = []
        self.superstars: list[FallingSprite] = []
        
        self.load_images()
        self.bind_keys()
        self.draw_start_screen()

    def resized(self, filename: str, size: tuple[int, int]):
        resample = getattr(Image, "Resampling", Image).LANCZOS
        return ImageTk.PhotoImage(Image.open(ASSET_DIR / filename).resize(size, resample))

    def load_images(self):
        self.bg_img = self.resized("background.png", (WIDTH, HEIGHT))
        self.cover_img = self.resized("cover.png", (WIDTH, HEIGHT))
        self.ship_img = self.resized("ship.png", (94, 94))
        self.star_img = self.resized("star.png", (66, 66))
        self.super_star_img = self.resized("star.png", (66, 66))
        self.glitch_img = self.resized("glitch.png", (60, 60))
        self.shield_img = self.resized("shield.png", (55, 55))
        self.shield_ring_img = self.resized("shield.png", (138, 138))

    def bind_keys(self):
        self.root.bind("<Return>", lambda even: self.start_game())
        self.root.bind("<Left>", lambda even: self.move_player(-self.player_speed, 0))
        self.root.bind("<Right>", lambda even: self.move_player(self.player_speed, 0))
        self.root.bind("<Up>", lambda even: self.move_player(0, -self.player_speed * 0.65))
        self.root.bind("<Down>", lambda even: self.move_player(0, self.player_speed * 0.65))
        for key in ("a", "A"):
            self.root.bind("<Left>", lambda even: self.move_player(-self.player_speed, 0))
        for key in ("d", "D"):
            self.root.bind("<Right>", lambda even: self.move_player(self.player_speed, 0))
        for key in ("w", "W"):
            self.root.bind("<Up>", lambda even: self.move_player(0, -self.player_speed * 0.65))
        for key in ("s", "S"):
            self.root.bind("<Down>", lambda even: self.move_player(0, self.player_speed * 0.65))
        for key in ("p", "P"):
            self.root.bind(key, lambda event: self.toggle_pause())
        for key in ("r", "R"):
            self.root.bind(key, lambda event: self.start_game())
        for key in ("m", "M"):
            self.root.bind(key, lambda event: self.toggle_mute())

    def load_high_score(self) -> int:
        if not SAVE_FILE.exists():
            return 0
        try:
            return int(json.loads(SAVE_FILE.read_text()).get("high_score", 0))
        except Exception:
            return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            SAVE_FILE.write_text(json.dumps({"high_score": self.high_score}, indent=2))

    def ask_difficulty(self):
        choice = simpledialog.askstring("Difficulty", "Choose easy, normal or hard", parent=self.root)
        value = (choice or "normal").strip().lower()
        if value == "easy":
            self.difficulty = 0.88
            self.player_speed = 18.5
        elif value == "hard":
            self.difficulty = 1.25
            self.player_speed = 15.5
        else:
            self.difficulty = 1.0
            self.player_speed = 16.5

    def draw_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_image (WIDTH // 2, HEIGHT // 2, image=self.cover_img)
        self.canvas.create_rectangle(32, 438, 928, 574, fill="#050814", outline="#2ce8ff", width=2)
        self.canvas.create_text(WIDTH // 2, 475, text="Press ENTER to launch", fill = "#ffffff", font=("Consolas", 28, "bold"))
        self.canvas.create_text(WIDTH // 2, 515, text="Collect stars, Dodge glitches, Grab shield orbs, M = mute sound", fill="#80f7ff", font=("Aptos", 15, "bold"))
        self.canvas.create_text(WIDTH // 2, 546, text=f"High score: {self.high_score}   Audio backend: {self.sfx.backend}", fill="#ffd94d", font=("Aptos", 14, "bold"))

    def create_starfield(self):
        self.starfield.clear()
        for _ in range(65):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.choice((1, 2, 2, 3))
            colour = random.choice(("#ffffff", "#b6eaff", "#a983ff"))
            self.starfield.append(self.canvas.create_oval(x, y, x + size, y + size, fill=colour, outline=""))

    def draw_world(self):
        self.canvas.delete("all")
        self.canvas.create_image(WIDTH // 2, HEIGHT // 2, image=self.bg_img)
        self.create_starfield()
        self.player = self.canvas.create_image(WIDTH // 2, HEIGHT - 86, image=self.ship_img)
        self.shield_overlay = self.canvas.create_image(WIDTH // 2, HEIGHT - 86, image=self.shield_ring_img, state="hidden")
        self.hud = self.canvas.create_text(16, 14, anchor="nw", fill="#eef7ff", font=("Consolas", 14, "bold"), text="")
        self.message = self.canvas.create_text(WIDTH // 2, HEIGHT // 2, fill="#ffd94d", font=("Consolas", 28, "bold"), text="")

        self.stars = [FallingSprite(self, "star", 3.3, self.star_img, 1) for _ in range(4)]
        self.glitches = [FallingSprite(self, "glitch", 3.9, self.glitch_img, 0) for _ in range(3)]
        self.powerups = [FallingSprite(self, "shield", 2.6, self.shield_img, 2)]
        self.superstars = [FallingSprite(self, "super", 2.4, self.super_star_img, 5)]
        self.update_hud()

    def start_game(self):
        if not self.player_name or self.player_name == "Pilot":
            name = simpledialog.askstring("Pilot name", "Enter your pilot name:", parent=self.root)
            self.player_name = name.strip() if name else "Pilot"
            self.ask_difficulty()
        self.score = 0
        self.combo = 0
        self.multiplier = 1
        self.lives = 3
        self.level = 1
        self.shield_active = False
        self.is_running = True
        self.is_paused = False
        self.shield_timer = 0
        self.particles.clear()
        self.sfx.play("menu")
        self.draw_world()
        self.game_loop()


    def update_hud(self):
        shield_text = f"ON {self.shield_timer // 25}s" if self.shield_active else "OFF"
        mute_text = "MUTED" if self.sfx.muted else "ON"
        self.canvas.itemconfigure(
            self.hud,
            text=(
                f"Pilot: {self.player_name} | Score: {self.score} | Lives: {self.lives} | "
                f"Level: {self.level} | Combo: {self.combo} | x{self.multiplier} | "
                f"Shield: {shield_text} | Sound: {mute_text} | Best: {self.high_score}"
            )
        )

    def toggle_mute(self):
        self.sfx.toggle_mute()
        self.update_hud()

    def move_player(self, dx: float, dy: float):
        if not self.is_running or self.is_paused:
            return
        x, y = self.canvas.coords(self.player)
        new_x = clamp(x + dx, 50, WIDTH - 50)
        new_y = clamp(y + dy, HEIGHT - 320, HEIGHT - 60)
        self.canvas.coords(self.player, new_x, new_y)
        self.canvas.coords(self.shield_overlay, new_x, new_y)
        self.create_engine_particles(new_x, new_y + 35)

    def toggle_pause(self):
        if not self.is_running:
            return
        self.is_paused = not self.is_paused
        self.canvas.itemconfigure(self.message, text="PAUSED" if self.is_paused else "")
        if not self.is_paused:
            self.game_loop()

    @staticmethod
    def touching(a, b) -> bool:
        if not a or not b:
            return False
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

    def create_particles(self, x, y, colour, count=8):
        for _ in range(count):
            p = self.canvas.create_oval(x, y, x + 5, y + 5, fill=colour, outline="")
            self.particles.append((p, random.randint(-4, 4), random.randint(-5, 3)))

    def create_engine_particles(self, x, y):
        for offset in (-16, 16):
            p = self.canvas.create_oval(x + offset, y, x + offset + 4, y + 4, fill="#7cf7ff", outline="")
            self.particles.append((p, random.randint(-1, 1), random.randint(3, 6)))

    def update_particles(self):
        for particle, dx, dy in self.particles[:]:
            self.canvas.move(particle, dx, dy)
            if random.random() < 0.16:
                self.canvas.delete(particle)
                self.particles.remove((particle, dx, dy))

    def update_starfield(self):
        for item in self.starfield:
            speed = random.choice((1, 1, 2, 2, 3))
            self.canvas.move(item, 0, speed)
            x1, y1, x2, y2 = self.canvas.coords(item)
            if y1 > HEIGHT:
                new_x = random.randint(0, WIDTH)
                self.canvas.coords(item, new_x, 0, new_x + (x2 - x1), (y2 - y1))

    def set_shield(self, active: bool):
        self.shield_active = active
        self.canvas.itemconfigure(self.shield_overlay, state="normal" if active else "hidden")
        self.shield_timer = 125 if active else 0

    def collect_star(self, obj: FallingSprite):
        gained = obj.score_value * self.multiplier
        self.score += gained
        self.combo += 1
        old_multiplier = self.multiplier
        self.multiplier = min(5, 1 + self.combo // 4)
        x, y = obj.position()
        self.create_particles(x, y, "#ffd94d", 12 if obj.kind == "super" else 7)
        obj.reset(extra_speed=0.04 if obj.kind == "star" else 0.06)
        self.sfx.play("combo" if self.multiplier > old_multiplier or obj.kind == "super" else "collect")
        self.check_level_up()

    def collect_shield(self, obj: FallingSprite):
        self.score += 2
        self.combo += 1
        self.multiplier = min(5, 1 + self.combo // 4)
        x, y = obj.position()
        self.create_particles(x, y, "#7cf7ff", 10)
        self.set_shield(True)
        obj.reset()
        self.sfx.play("shield")

    def hit_glitch(self, obj: FallingSprite):
        x, y = obj.position()
        self.create_particles(x, y, "#ff4b98", 14)
        obj.reset()
        self.combo = 0
        self.multiplier = 1
        if self.shield_active:
            self.set_shield(False)
            self.sfx.play("shield")
            return
        self.lives -= 1
        self.sfx.play("hit")
        if self.lives <= 0:
            self.end_game()

    def check_level_up(self):
        new_level = self.score // 12 + 1
        if new_level > self.level:
            self.level = new_level
            self.difficulty += 0.08
            self.sfx.play("level_up")
            self.canvas.itemconfigure(self.message, text=f"LEVEL {self.level}!")
            self.root.after(800, lambda: self.canvas.itemconfigure(self.message, text=""))
            if self.level in (3, 5, 7):
                self.glitches.append(FallingSprite(self, "glitch", 4.1 + self.level * 0.08, self.glitch_img, 0))

    def end_game(self):
        self.is_running = False
        self.save_high_score()
        self.update_hud()
        self.canvas.itemconfigure(self.message, text=f"GAME OVER\nScore: {self.score}\nPress R to restart")
        self.sfx.play("game_over")
        if self.score >= self.high_score and self.score > 0:
            messagebox.showinfo("New high score!", f"Amazing! New best score: {self.high_score}")        

    def game_loop(self):
        if not self.is_running or self.is_paused:
            return
        self.update_starfield()
        player_box = self.canvas.bbox(self.player)

        for obj in self.stars:
            obj.move(self.difficulty)
            if self.touching(player_box, obj.bbox()):
                self.collect_star(obj)
            elif obj.off_screen():
                self.combo = max(0, self.combo - 1)
                self.multiplier = min(5, 1 + self.combo // 4)
                obj.reset()

        for obj in self.superstars:
            obj.move(self.difficulty * 1.05)
            if self.touching(player_box, obj.bbox()):
                self.collect_star(obj)
            elif obj.off_screen():
                obj.reset()

        for obj in self.powerups:
            obj.move(self.difficulty)
            if self.touching(player_box, obj.bbox()):
                self.collect_shield(obj)
            elif obj.off_screen():
                obj.reset()

        for obj in self.glitches:
            obj.move(self.difficulty)
            if self.touching(player_box, obj.bbox()):
                self.hit_glitch(obj)
            elif obj.off_screen():
                obj.reset()

        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.set_shield(False)

        self.canvas.tag_raise(self.shield_overlay)
        self.canvas.tag_raise(self.player)
        self.update_particles()
        self.update_hud()
        self.root.after(24, self.game_loop)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    PixelPanicSoundGame().run()