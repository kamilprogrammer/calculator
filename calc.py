import tkinter as tk
from tkinter import Button, Menu, Text, font
from turtle import window_width

from setuptools import Command

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#2EAFF5"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        #help
        def menu_command ():
            pass
        def exit_command ():
            self.window.destroy()
        my_menu = Menu(self.window)
        self.window.config(menu=my_menu) 
        help_menu = Menu(my_menu)
        my_menu.add_cascade(label="help", menu=help_menu)
        help_menu.add_command(label="مساعدة؟", command=menu_command)

        #exit
        exit_menu = Menu(my_menu)
        my_menu.add_cascade(label="exit", menu=exit_menu)
        exit_menu.add_command(label="خروج", command=exit_command)
        self.window.configure(background='#F8FAFF')

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            00: (4, 3), 0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+", "00":"00"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_radius1_button()
        self.create_radius2_button()
        self.create_equals2_button()
        self.helpmain()
        self.made_by()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()


    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**3"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b3", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=4, columnspan=2, sticky=tk.NSEW)

    def _00(self):
        self.current_expression = str(eval(f"{self.current_expression}00"))
        self.update_label()


    def create_equals2_button(self):
        button = tk.Button(self.buttons_frame, text="00", bg=OFF_WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                           borderwidth=0, command=self._00)
        button.grid(row=4, column=3, sticky=tk.NSEW)
  


    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])



    
    def help(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()
    

    def helpmain(self):
        button = Button(self.buttons_frame, text='مساعدة', width=4, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                        borderwidth=0, command=help)
        button.grid(row=2, column=5, sticky=tk.NSEW)       


    def rad1(self):
        self.current_expression = str(eval(f"{self.current_expression}**2*3.14"))
        self.update_label()

    def create_radius1_button(self):
        button = tk.Button(self.buttons_frame, text="مساحة \n الدائرة ",width=4, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.rad1)
        button.grid(row=0, column=5, sticky=tk.NSEW)



    def madeby(self):
        window3 = tk.Tk()
        window3.geometry('200x200')
        window3.title('Made by')
        window3.resizable(0, 0)
        t1= Button(window3, text='made by kamil & Alfajer school')
        t1.place(x=10, y=70)
        window3.mainloop()

    def made_by(self):
        button = tk.Button(self.buttons_frame, text="  made \n by",width=4, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.madeby)
        button.grid(row=3, column=5, sticky=tk.NSEW)    


    def rad2(self):
        self.current_expression = str(eval(f"{self.current_expression}"))
        self.update_label()

    def create_radius2_button(self):
        button = tk.Button(self.buttons_frame, text="محيط \n الدائرة ",width=4, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.rad1)
        button.grid(row=1, column=5, sticky=tk.NSEW)

             

    def run(self):
        self.window.mainloop()

#good bye

if __name__ == "__main__":
    calc = Calculator()
    calc.run()