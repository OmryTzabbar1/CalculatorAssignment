import tkinter as tk
from tkinter import messagebox
import math
import random
from PIL import Image, ImageTk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("380x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#2b2b2b")

        self.expression = ""

        # Display
        self.display = tk.Entry(
            root,
            font=("Arial", 24, "bold"),
            justify="right",
            bd=0,
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10, ipady=20)

        # Button layout - traditional calculator style
        buttons = [
            ('C', '#ff9500'), ('⌫', '#ff9500'), ('%', '#ff9500'), ('÷', '#ff9500'),
            ('7', '#505050'), ('8', '#505050'), ('9', '#505050'), ('×', '#ff9500'),
            ('4', '#505050'), ('5', '#505050'), ('6', '#505050'), ('-', '#ff9500'),
            ('1', '#505050'), ('2', '#505050'), ('3', '#505050'), ('+', '#ff9500'),
            ('√', '#505050'), ('0', '#505050'), ('.', '#505050'), ('=', '#ff9500'),
            ('x²', '#505050'), ('xʸ', '#505050'), ('(', '#505050'), (')', '#505050'),
            ('🦖', '#00aa00'), ('', '#2b2b2b'), ('', '#2b2b2b'), ('', '#2b2b2b')
        ]

        row = 1
        col = 0

        for button_text, color in buttons:
            cmd = lambda x=button_text: self.on_button_click(x)
            btn = tk.Button(
                root,
                text=button_text,
                font=("Arial", 18, "bold"),
                command=cmd,
                bd=0,
                bg=color,
                fg="#ffffff",
                activebackground=self.darken_color(color),
                activeforeground="#ffffff",
                relief=tk.FLAT
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

            col += 1
            if col > 3:
                col = 0
                row += 1

        # Configure grid weights for responsive layout
        for i in range(8):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

    def darken_color(self, color):
        """Darken a hex color for active state"""
        if color == '#ff9500':
            return '#cc7700'
        elif color == '#505050':
            return '#3a3a3a'
        return color

    def on_button_click(self, char):
        if char == '🦖':
            self.launch_dino_game()
        elif char == 'C':
            self.expression = ""
            self.display.delete(0, tk.END)
        elif char == '⌫':
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
        elif char == '=':
            try:
                # Replace visual symbols with Python operators
                expr = self.expression.replace('×', '*').replace('÷', '/')
                result = str(eval(expr))
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
                self.expression = result
            except Exception as e:
                messagebox.showerror("Error", "Invalid expression")
                self.expression = ""
                self.display.delete(0, tk.END)
        elif char == '√':
            try:
                expr = self.expression.replace('×', '*').replace('÷', '/')
                result = str(math.sqrt(float(eval(expr))))
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
                self.expression = result
            except Exception as e:
                messagebox.showerror("Error", "Invalid expression for square root")
        elif char == 'x²':
            try:
                expr = self.expression.replace('×', '*').replace('÷', '/')
                result = str(float(eval(expr)) ** 2)
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
                self.expression = result
            except Exception as e:
                messagebox.showerror("Error", "Invalid expression for square")
        elif char == 'xʸ':
            self.expression += '**'
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
        elif char in ['%', '×', '÷', '-', '+', '.', '(', ')']:
            self.expression += char
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
        elif char != '':
            self.expression += str(char)
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

    def launch_dino_game(self):
        game_window = tk.Toplevel(self.root)
        DinoGame(game_window)


class DinoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Dino Jump Game")
        self.root.geometry("800x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f7f7f7")

        self.canvas = tk.Canvas(root, width=800, height=400, bg="#f7f7f7", highlightthickness=0)
        self.canvas.pack()

        # Load dinosaur image
        dino_img = Image.open("dinoImage.jpg")
        dino_img = dino_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.dino_photo = ImageTk.PhotoImage(dino_img)

        # Game variables
        self.dino_x = 50
        self.dino_y = 300
        self.dino_width = 50
        self.dino_height = 50
        self.dino_velocity = 0
        self.gravity = 1
        self.jump_strength = -18
        self.is_jumping = False
        self.ground_y = 300

        # Obstacles
        self.obstacles = []
        self.obstacle_speed = 7
        self.obstacle_interval = 1500
        self.score = 0
        self.game_over = False

        # Draw initial elements
        self.dino = self.canvas.create_image(
            self.dino_x + self.dino_width // 2,
            self.dino_y + self.dino_height // 2,
            image=self.dino_photo
        )
        self.ground = self.canvas.create_line(0, 350, 800, 350, fill="#000000", width=2)
        self.score_text = self.canvas.create_text(
            750, 30, text=f"Score: {self.score}", font=("Arial", 16, "bold"), fill="#535353"
        )

        # Bind keys
        self.root.bind("<space>", self.jump)
        self.root.bind("<Up>", self.jump)

        # Start game
        self.spawn_obstacle()
        self.game_loop()

    def jump(self, event=None):
        if not self.is_jumping and not self.game_over:
            self.is_jumping = True
            self.dino_velocity = self.jump_strength

    def spawn_obstacle(self):
        if not self.game_over:
            obstacle_width = 40
            cactus_size = random.choice([40, 50, 60])
            obstacle_height = cactus_size
            obstacle_x = 800
            obstacle_y = 350 - obstacle_height

            obstacle = self.canvas.create_text(
                obstacle_x + obstacle_width // 2,
                obstacle_y + obstacle_height // 2,
                text="🌵",
                font=("Arial", cactus_size)
            )
            self.obstacles.append({
                'id': obstacle,
                'x': obstacle_x,
                'y': obstacle_y,
                'width': obstacle_width,
                'height': obstacle_height
            })

            self.root.after(self.obstacle_interval, self.spawn_obstacle)

    def check_collision(self, obs):
        dino_left = self.dino_x
        dino_right = self.dino_x + self.dino_width
        dino_top = self.dino_y
        dino_bottom = self.dino_y + self.dino_height

        obs_left = obs['x']
        obs_right = obs['x'] + obs['width']
        obs_top = obs['y']
        obs_bottom = obs['y'] + obs['height']

        if (dino_right > obs_left and dino_left < obs_right and
            dino_bottom > obs_top and dino_top < obs_bottom):
            return True
        return False

    def game_loop(self):
        if self.game_over:
            return

        # Update dino position
        self.dino_velocity += self.gravity
        self.dino_y += self.dino_velocity

        if self.dino_y >= self.ground_y:
            self.dino_y = self.ground_y
            self.dino_velocity = 0
            self.is_jumping = False

        self.canvas.coords(
            self.dino,
            self.dino_x + self.dino_width // 2,
            self.dino_y + self.dino_height // 2
        )

        # Update obstacles
        obstacles_to_remove = []
        for obs in self.obstacles:
            obs['x'] -= self.obstacle_speed
            self.canvas.coords(
                obs['id'],
                obs['x'] + obs['width'] // 2,
                obs['y'] + obs['height'] // 2
            )

            # Check collision
            if self.check_collision(obs):
                self.game_over = True
                self.canvas.create_text(
                    400, 200, text="GAME OVER!",
                    font=("Arial", 48, "bold"), fill="#ff0000"
                )
                self.canvas.create_text(
                    400, 250, text=f"Final Score: {self.score}",
                    font=("Arial", 24), fill="#535353"
                )
                self.canvas.create_text(
                    400, 290, text="Press any key to play again",
                    font=("Arial", 16), fill="#535353"
                )
                self.root.bind("<Key>", self.restart_game)
                return

            # Remove off-screen obstacles
            if obs['x'] + obs['width'] < 0:
                obstacles_to_remove.append(obs)
                self.canvas.delete(obs['id'])
                self.score += 10
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

        for obs in obstacles_to_remove:
            self.obstacles.remove(obs)

        self.root.after(30, self.game_loop)

    def restart_game(self, event=None):
        # Clear canvas
        self.canvas.delete("all")

        # Reset game variables
        self.dino_y = 300
        self.dino_velocity = 0
        self.is_jumping = False
        self.obstacles = []
        self.score = 0
        self.game_over = False

        # Redraw initial elements
        self.dino = self.canvas.create_image(
            self.dino_x + self.dino_width // 2,
            self.dino_y + self.dino_height // 2,
            image=self.dino_photo
        )
        self.ground = self.canvas.create_line(0, 350, 800, 350, fill="#000000", width=2)
        self.score_text = self.canvas.create_text(
            750, 30, text=f"Score: {self.score}", font=("Arial", 16, "bold"), fill="#535353"
        )

        # Rebind jump keys
        self.root.bind("<space>", self.jump)
        self.root.bind("<Up>", self.jump)

        # Restart game
        self.spawn_obstacle()
        self.game_loop()

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()