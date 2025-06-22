import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        """Initialize the calculator ."""
        self.root = root
        self.root.title("PRO Calc-o-Matic 🖤")
        self.root.geometry("300x450") # Slightly larger to fit buttons
        self.root.resizable(False, False)
        self.root.configure(bg="#000000") # Jet Black background

        self.expression = ""
        self.input_text = tk.StringVar()

        # Display Field
        # A sleek, dark display for input and results
        self.input_frame = tk.Frame(root, width=300, height=80, bd=0, highlightbackground="#333333", highlightthickness=1, bg="#1a1a1a")
        self.input_frame.pack(side=tk.TOP, pady=10)
        self.input_frame.pack_propagate(False) # Prevents the frame from resizing to fit contents

        self.input_field = tk.Entry(self.input_frame, font=("Inter", 24, "bold"), textvariable=self.input_text,
                                    width=50, bg="#1a1a1a", fg="#E0E0E0", bd=0, justify=tk.RIGHT,
                                    insertbackground="#E0E0E0", cursor="xterm") # Dark grey background, light text
        self.input_field.pack(ipady=10, expand=True, fill="both")
        self.input_field.focus_set()

        # Buttons Frame
        # Organize buttons in a grid for a standard calculator layout
        self.btns_frame = tk.Frame(root, bg="#000000")
        self.btns_frame.pack()

        # Button styling dictionary for reusability and theme consistency
        self.button_style = {
            "font": ("Inter", 16),
            "width": 4,
            "height": 2,
            "bd": 0,
            "fg": "#E0E0E0", # Light grey text for all buttons
            "activebackground": "#444444", # Slightly lighter black on hover
            "activeforeground": "#FFFFFF", # White text on hover
            "cursor": "hand2" # Cursor changes on hover
        }

        # Define button layout (text, row, column, background color)
        buttons = [
            # Row 1
            ('C', 1, 0, '#333333', self.clear_all), # Clear button - dark grey
            ('/', 1, 1, '#FF9500', lambda: self.button_click('/')), # Operator - orange
            ('*', 1, 2, '#FF9500', lambda: self.button_click('*')), # Operator - orange
            ('DEL', 1, 3, '#333333', self.clear_last), # Backspace - dark grey

            # Row 2
            ('7', 2, 0, '#505050', lambda: self.button_click('7')), # Number button - medium grey
            ('8', 2, 1, '#505050', lambda: self.button_click('8')),
            ('9', 2, 2, '#505050', lambda: self.button_click('9')),
            ('-', 2, 3, '#FF9500', lambda: self.button_click('-')), # Operator - orange

            # Row 3
            ('4', 3, 0, '#505050', lambda: self.button_click('4')),
            ('5', 3, 1, '#505050', lambda: self.button_click('5')),
            ('6', 3, 2, '#505050', lambda: self.button_click('6')),
            ('+', 3, 3, '#FF9500', lambda: self.button_click('+')), # Operator - orange

            # Row 4
            ('1', 4, 0, '#505050', lambda: self.button_click('1')),
            ('2', 4, 1, '#505050', lambda: self.button_click('2')),
            ('3', 4, 2, '#505050', lambda: self.button_click('3')),

            # Row 5
            ('0', 5, 0, '#505050', lambda: self.button_click('0')),
            ('.', 5, 1, '#505050', lambda: self.button_click('.')),
            ('=', 5, 2, '#FF9500', self.evaluate_expression) # Equals button - orange
        ]

        # Create and place buttons
        for (text, row, col, bg_color, command) in buttons:
            btn_kwargs = self.button_style.copy()
            btn_kwargs['bg'] = bg_color # Set specific background color
            if text == '0': # Make '0' button span two columns if desired for classic layout
                btn = tk.Button(self.btns_frame, text=text, command=command, **btn_kwargs)
                btn.grid(row=row, column=col, columnspan=2, padx=1, pady=1, sticky="nsew") # Span 2 columns
                # Adjust width for '0' button if it spans two columns, or just let sticky handle it
                # For simplicity and to fit 120 lines, we will keep width as is and use sticky.
            elif text == '=': # The '=' button will occupy the last column of the last two rows
                btn = tk.Button(self.btns_frame, text=text, command=command, **btn_kwargs)
                btn.grid(row=row-1, column=3, rowspan=2, padx=1, pady=1, sticky="nsew") # Span 2 rows
            else:
                btn = tk.Button(self.btns_frame, text=text, command=command, **btn_kwargs)
                btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

        # Configure grid column and row weights for responsive button sizing
        for i in range(4): # 4 columns
            self.btns_frame.grid_columnconfigure(i, weight=1)
        for i in range(1, 6): # 5 rows (from row 1 to 5)
            self.btns_frame.grid_rowconfigure(i, weight=1)

    def button_click(self, char):
        """Handles number and operator button clicks."""
        # Prevent multiple operators in a row (e.g., "5++")
        if char in '+-*/.' and self.expression and self.expression[-1] in '+-*/.':
            # Replace the last operator if a new one is pressed
            self.expression = self.expression[:-1] + char
        else:
            self.expression += str(char)
        self.input_text.set(self.expression)

    def clear_all(self):
        """Clears the entire expression."""
        self.expression = ""
        self.input_text.set("")

    def clear_last(self):
        """Deletes the last character from the expression (backspace functionality)."""
        self.expression = self.expression[:-1]
        self.input_text.set(self.expression)

    def evaluate_expression(self):
        """Evaluates the mathematical expression and displays the result."""
        try:
            # Using eval() for simplicity; for production, a safer parser is recommended.
            # Replace 'x' with '*' for multiplication if needed (input uses '*')
            # eval() handles standard operators directly.
            result = str(eval(self.expression))
            self.expression = result
            self.input_text.set(result)
        except ZeroDivisionError:
            messagebox.showerror("Error", "Can't divide by zero! ⛔", parent=self.root)
            self.expression = "" # Clear expression on error
            self.input_text.set("")
        except SyntaxError:
            messagebox.showerror("Error", "Invalid expression! 🤔", parent=self.root)
            self.expression = ""
            self.input_text.set("")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e} 🐛", parent=self.root)
            self.expression = ""
            self.input_text.set("")

if __name__ == "__main__":
    app_root = tk.Tk()
    calculator = CalculatorApp(app_root)
    app_root.mainloop()

