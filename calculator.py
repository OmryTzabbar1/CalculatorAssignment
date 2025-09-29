import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        self.expression = ""

        # Display
        self.display = tk.Entry(root, font=("Arial", 20), justify="right", bd=10)
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Button layout
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        row = 1
        col = 0

        for button in buttons:
            cmd = lambda x=button: self.on_button_click(x)
            tk.Button(
                root,
                text=button,
                font=("Arial", 18),
                command=cmd,
                bd=5,
                relief=tk.RAISED
            ).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

            col += 1
            if col > 3:
                col = 0
                row += 1

        # Configure grid weights for responsive layout
        for i in range(5):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display.delete(0, tk.END)
        elif char == '=':
            try:
                result = str(eval(self.expression))
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
                self.expression = result
            except Exception as e:
                messagebox.showerror("Error", "Invalid expression")
                self.expression = ""
                self.display.delete(0, tk.END)
        else:
            self.expression += str(char)
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()