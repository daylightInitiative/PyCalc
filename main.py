import tkinter as tk

root = tk.Tk()
root.title("Calculator")
root.geometry("320x480")

expression_label = tk.Label(root, text="", anchor="e", font=("Arial", 20))
expression_label.pack(fill="both")

result_label = tk.Label(root, text="", anchor="e", font=("Arial", 30))
result_label.pack(fill="both")

special_frame = tk.Frame(root)
special_frame.pack(fill="both", expand=True)

buttons_frame = tk.Frame(root)
buttons_frame.pack(fill="both", expand=True)

button_order = [7, 8, 9, 4, 5, 6, 1, 2, 3, 0]

button_font = ("Arial", 12)

def press(num: str):
    expression = expression_label.cget("text")

    if num in math_symbols:
        if expression and expression[-1] not in math_symbols:
            expression += num
    elif num == "0":
        if expression == "" or expression[-1] in math_symbols:
            # prevent multiple leading zeros like 0005
            if len(expression) == 0 or expression[-1] in math_symbols:
                if len(expression) < 2 or not (expression[-2:].endswith("0") and (len(expression) == 1 or expression[-3] in math_symbols)):
                    expression += num
        else:
            expression += num
    else:
        # Remove a leading "0" unless it's "0." or after a symbol
        if len(expression) > 0 and expression[-1] == "0":
            if len(expression) == 1 or expression[-2] in math_symbols:
                expression = expression[:-1] + num
            else:
                expression += num
        else:
            expression += num

    expression_label.config(text=expression)

def add_decimal():
    expression = expression_label.cget("text")
    expression_arr = expression.split(',')

    if expression == "":
        expression_arr.append(".")
    elif expression_arr[-1][-1] not in math_symbols and expression_arr[-1] != "." and "." not in expression_arr[-1]:
        expression_arr.append(".")

    expr_result = ''.join(expression_arr)
    expression_label.config(text=expr_result)

def is_number(value):
    if isinstance(value, str):
        return value.isnumeric()
    return isinstance(value, (int, float, complex))

def canInsertZero(expression_array) -> bool:
    isInvalid = False
    expression_str = expression_array[0]
    for i, char in enumerate(expression_str):
        if char in math_symbols:
            index = (i + 1)
            if index < len(expression_str) and expression_str[index] is not None and is_number(expression_str[index]) and float(expression_str[index]) == 0:
                return True
    return isInvalid

def calculate(expression):
    try:
        if expression[-1] in math_symbols:
            if len(expression) > 1:
                expression_arr = expression.split(',')
                previous_number = expression[-2]

                if is_number(previous_number):
                    expression += previous_number

        result = eval(expression)
        result_label.config(text=str(result))
    except Exception as e:
        result_label.config(text="Error")
        print(e)

def clear():
    expression_label.config(text="")
    result_label.config(text="")

# Create digit buttons
digit_buttons = []
for i in range(0, 10):
    digit_order_index = button_order.index(i)
    button = tk.Button(buttons_frame, text=str(i), font=button_font, command=lambda i=i: press(str(i)))

    if i == 0:
        digit_order_index += 1  # shift 0 over one

    button.grid(row=digit_order_index // 3 + 1, column=(digit_order_index % 3), sticky="nsew")
    digit_buttons.append(button)

# Create operation buttons
display_symbols = ["÷", "×", "−", "+"]
math_symbols = ["/", "*", "-", "+"]
operation_buttons = []

for i in range(4):
    symbol_index = i % len(math_symbols)
    button_name = display_symbols[symbol_index]

    button = tk.Button(buttons_frame, text=button_name, font=button_font, command=lambda i=i: press(math_symbols[i]))
    button.grid(row=i, column=3, sticky="nsew")
    operation_buttons.append(button)

# Create special buttons
clear_button = tk.Button(buttons_frame, text="C", command=clear)
clear_button.grid(row=0, column=2, sticky="nsew")

ce_button = tk.Button(buttons_frame, text="CE", command=clear)
ce_button.grid(row=0, column=1, sticky="nsew")

equals_button = tk.Button(buttons_frame, text="=", command=lambda: calculate(expression_label.cget("text")))
equals_button.grid(row=4, column=3, sticky="nsew")

decimal_button = tk.Button(buttons_frame, text=".", command=lambda: add_decimal())
decimal_button.grid(row=4, column=2, sticky="nsew")

# Configure row/column weights for scaling
for i in range(5):  # Rows 0 to 4
    buttons_frame.rowconfigure(i, weight=1)
for j in range(4):  # Columns 0 to 3
    buttons_frame.columnconfigure(j, weight=1)

root.mainloop()
