import tkinter as tk
from tkinter import messagebox
import math

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
            ('x²', '#505050'), ('xʸ', '#505050'), ('(', '#505050'), (')', '#505050')
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
        for i in range(7):
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
        if char == 'C':
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
        else:
            self.expression += str(char)
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()