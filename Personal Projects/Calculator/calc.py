"""
Calculator GUI - Personal project
This project was made in my free time, completely unrelated to college tasks
Project start: 21/10/2026
Project end: 23/10/2026
"""

import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Calculator")
root.geometry("278x366")
root.resizable(False, False)
root.configure(background="#2C2C2C")

# ------------------------+---------------------------

# ------------------- CONSTANTS ----------------------

BUTTON_WIDTH = 4
BUTTON_HEIGHT = 1

# ------------------- VARIABLES ----------------------

temporary_display = False
negative_number = False

# ------------------- FUNCTIONS ----------------------

def num_input(number):
    """inputs a number into the display"""

    global temporary_display

    if temporary_display:
        history_label["text"] = ""
        display_label["text"] = "0"
        temporary_display = False

    new_display = display_label["text"] + str(number)
    if display_label["text"] == "0" and number == 0: # prevents adding excessive zeroes (like this: 000, into this: 0)
        return
    elif "." in new_display: # prevents removing the first 0 in a decimal (like this: .32, into this: 0.32)
        display_label["text"] = new_display
        return
    display_label["text"] = new_display.lstrip("0") # .lstrip("0") removes leading zeroes (like this: 025, into this: 25)


def delete_num(type):
    """removes characters from the display"""
    
    global temporary_display
    
    if temporary_display:
        history_label["text"] = ""
        display_label["text"] = "0"
        temporary_display = False
        return
    
    if type == "all": # for the clear all (C) button
        history_label["text"] = ""
        display_label["text"] = "0"

    elif type == "entry": # for the clear entry (CE) button
        display_label["text"] = "0"

    elif type == "one": # for the Del button
        temp = display_label["text"]
        display_label["text"] = temp[:-1]
        if display_label["text"] == "": # prevents the display from being fully empty and instead showing a zero
            display_label["text"] = "0"

    temporary_display = False

    


def calculate(must_return = False):
    """calculate the result of the equation"""

    global temporary_display, negative_number
    
    if not any(char in ["÷", "x", "-", "+"] for char in history_label["text"]): # if theres nothing to calculate, return
        history_label["text"] = ""
        temporary_display = True
        return

    if "=" in history_label["text"]:
        history_label["text"] = display_label["text"]
        return history_label["text"]
    else:
        history_label["text"] = history_label["text"] + display_label["text"] + "=" # sets the history label to the equation
    temp = history_label["text"]
    equation = list(temp[:-1]) # removes the "=" sign from the end of the equation, then turns it into a list
    first = [] # this is in list form, since it's going to append each item in equation to it until we find the operator
    operator = ""
    second = []
    operator_found = False

    if negative_number:
        first.append("-") # add a negative sign (-) to first
        temp = list(equation)
        temp.remove("-") # remove the negative sign from the equation to prevent an error
        equation = temp
        negative_number = False
    
    for char in equation:
        if char not in ["÷", "x", "-", "+"]: # if char is not an operator
            if not operator_found: # if we havent found the operator (first half of the equation, for example: 52)
                first.append(char)
            else: # if we HAVE found the operator (second half, 36)
                second.append(char)
        else: # if the char IS an operator
            operator = char
            operator_found = True

    # turning the first and second lists each into strings
    first = "".join(first)
    second = "".join(second)

    # checks if the number should be an integer or a float
    if "." in first:
        first = float(first)
    else:
        first = int(first)
    if "." in second:
        second = float(second)
    else:
        second = int(second)

    # calculate the result of the equation
    if operator == "÷":
        result = first / second # divide
    elif operator == "x":
        result = first * second # multiply
    elif operator == "-":
        result = first - second # subtract
    elif operator == "+":
        result = first + second # add

    # finally, if the function should return result, then return it.
    if must_return:
        return str(result)
    else: # otherwise, display it instead
        display_label["text"] = str(result)


def operate(operator):
    """takes the display label, adds the corresponding operator and then puts it in the history label.

    Uses calculate() if there was already an equation in the history label."""



    if history_label["text"] == "" or history_label["text"] == "0": # if theres nothing to further calculate before changing the history
        history_label["text"] = display_label["text"] + operator
        display_label["text"] = "0"
    else: # if there is something to calculate, then replaces the history afterwards   
        result = calculate(True)
        history_label["text"] = result + operator
        display_label["text"] = "0"


def decimal_input():
    """adds a decimal point to the display"""
    display_label["text"] += "."


def swap_polarity():
    """swap between positive and negative"""

    global negative_number

    if display_label["text"] == "0": # if the display is "0", theres no point in negating it
        return
    
    if negative_number: # if the display is already negative, turn it positive
        temp = list(display_label["text"])
        temp.remove("-")
        display_label["text"] = "".join(temp)
        negative_number = False
    else: # otherwise, turn it negative
        display_label["text"] = "-" + display_label["text"]
        negative_number = True


# ---------------------- GUI -------------------------

buttons_frame = tk.Frame(root)
buttons_frame.grid()

# Calculator design
# (just to make adding and aligning buttons easier)
# +---------------+
# |    Display    |
# +---+---+---+---+
# | CE| C |Del| ÷ |
# +---+---+---+---+
# | 7 | 8 | 9 | x |
# +---+---+---+---+
# | 4 | 5 | 6 | - |
# +---+---+---+---+
# | 1 | 2 | 3 | + |
# +---+---+---+---+
# |+/-| 0 | . | = |
# +---+---+---+---+

# -------------------- BUTTONS -----------------------

# these arent buttons, but i still put them in the buttons area since they're in the buttons_frame grid
history_label = tk.Label(buttons_frame, text="", font=("Consolas", 12), bg="#2C2C2C", fg="#a0a0a0", width=BUTTON_WIDTH*2, justify="right", anchor="e")
history_label.grid(column=0, row=0, columnspan=4, sticky = "nesw")

display_label = tk.Label(buttons_frame, text="0", font=("Consolas", 36), bg="#000000", fg="#ffffff", width=BUTTON_WIDTH*2, height=BUTTON_HEIGHT, justify="right", anchor="e")
display_label.grid(column=0, row=1, columnspan=4, sticky = "nesw")


# column 1
clear_entry_button = tk.Button(buttons_frame, text="CE", font=("Consolas", 20), command=lambda: delete_num("entry"), bg="#6e6e6e", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
clear_entry_button.grid(column=0, row=2)

seven_button = tk.Button(buttons_frame, text="7", font=("Consolas", 20), command=lambda: num_input(7), bg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
seven_button.grid(column=0, row=3)
root.bind("<KP_7>", lambda: num_input(7))

four_button = tk.Button(buttons_frame, text="4", font=("Consolas", 20), command=lambda: num_input(4), bg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
four_button.grid(column=0, row=4)
root.bind("<KP_4>", lambda: num_input(4))

one_button = tk.Button(buttons_frame, text="1", font=("Consolas", 20), command=lambda: num_input(1), bg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
one_button.grid(column=0, row=5)
root.bind("<KP_1>", lambda: num_input(1))

polarity_button = tk.Button(buttons_frame, text="+/-", font=("Consolas", 20), command=swap_polarity, bg="#6e6e6e", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
polarity_button.grid(column=0, row=6)


# column 2
clear_button = tk.Button(buttons_frame, text="C", font=("Consolas", 20), command=lambda: delete_num("all"), bg="#6e6e6e", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
clear_button.grid(column=1, row=2)

eight_button = tk.Button(buttons_frame, text="8", font=("Consolas", 20), command=lambda: num_input(8), bg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
eight_button.grid(column=1, row=3)
root.bind("<KP_8>", lambda: num_input(8))

five_button = tk.Button(buttons_frame, text="5", font=("Consolas", 20), command=lambda: num_input(5), bg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
five_button.grid(column=1, row=4)
root.bind("<KP_5>", lambda: num_input(5))

two_button = tk.Button(buttons_frame, text="2", font=("Consolas", 20), command=lambda: num_input(2), bg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
two_button.grid(column=1, row=5)
root.bind("<KP_2>", lambda: num_input(2))

zero_button = tk.Button(buttons_frame, text="0", font=("Consolas", 20), command=lambda: num_input(0), bg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
zero_button.grid(column=1, row=6)
root.bind("<KP_0>", lambda: num_input(0))


# column 3
backspace_button = tk.Button(buttons_frame, text="Del", font=("Consolas", 20), command=lambda: delete_num("one"), bg="#6e6e6e", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
backspace_button.grid(column=2, row=2)
root.bind("<BackSpace>", lambda: delete_num("one"))

nine_button = tk.Button(buttons_frame, text="9", font=("Consolas", 20), command=lambda: num_input(9), bg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
nine_button.grid(column=2, row=3)
root.bind("<KP_9>", lambda: num_input(9))

six_button = tk.Button(buttons_frame, text="6", font=("Consolas", 20), command=lambda: num_input(6), bg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
six_button.grid(column=2, row=4)
root.bind("<KP_6>", lambda: num_input(6))

three_button = tk.Button(buttons_frame, text="3", font=("Consolas", 20), command=lambda: num_input(3), bg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
three_button.grid(column=2, row=5)
root.bind("<KP_3>", lambda: num_input(3))

decimal_button = tk.Button(buttons_frame, text=".", font=("Consolas", 20), command=decimal_input, bg="#6e6e6e", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
decimal_button.grid(column=2, row=6)
root.bind("<KP_Decimal>", decimal_input)


# column 4
division_button = tk.Button(buttons_frame, text="÷", font=("Consolas", 20), command=lambda: operate("÷"), bg="#ff9137", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
division_button.grid(column=3, row=2)
root.bind("<KP_Divide>", lambda: operate("÷"))

multiplication_button = tk.Button(buttons_frame, text="x", font=("Consolas", 20), command=lambda: operate("x"), bg="#ff9137", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
multiplication_button.grid(column=3, row=3)
root.bind("<KP_Multiply>", lambda: operate("x"))

subtraction_button = tk.Button(buttons_frame, text="-", font=("Consolas", 20), command=lambda: operate("-"), bg="#ff9137", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
subtraction_button.grid(column=3, row=4)
root.bind("<KP_Subtract>", lambda: operate("-"))

addition_button = tk.Button(buttons_frame, text="+", font=("Consolas", 20), command=lambda: operate("+"), bg="#ff9137", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
addition_button.grid(column=3, row=5)
root.bind("<KP_Add>", lambda: operate("+"))

calculate_button = tk.Button(buttons_frame, text="=", font=("Consolas", 20), command=calculate, bg="#000000", fg="#ffffff", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,)
calculate_button.grid(column=3, row=6)
root.bind("<KP_Enter>", calculate)


#----------------------------------------------------

root.mainloop()
