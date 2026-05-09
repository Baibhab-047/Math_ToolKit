import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication, convert_xor
import tkinter as tk
from tkinter import messagebox

transformations = (standard_transformations + (implicit_multiplication, convert_xor))

def integrate_expression(expr_str, var_str):
    try:
        expr = parse_expr(expr_str, transformations=transformations)
        var = sp.symbols(var_str)
        integral = sp.integrate(expr, var)
        int_txt = str(integral).replace("**", "^").replace("*", "")
        return f"∫ ({expr_str}) d{var_str} = {int_txt} + C"
    except:
        return None

def calculate_integral():
    expr_input = eq_entry.get().strip()
    var_input = var_entry.get().strip()
    
    if not expr_input or not var_input:
        messagebox.showwarning("Input Error", "Please provide an expression and a variable.")
        return

    result = integrate_expression(expr_input, var_input)
    if result:
        result_label.config(text=result)
    else:
        messagebox.showerror("Error", "Invalid syntax.")

root = tk.Tk()
root.title("Integration Tool")
root.geometry("450x450")

tk.Label(root, text="Function:", font=("Arial", 10, "bold")).pack(pady=(20, 0))
eq_entry = tk.Entry(root, width=40, font=("Consolas", 12), justify="center")
eq_entry.pack(pady=5)
eq_entry.insert(0, "3x^2 + 5x + 2")

tk.Label(root, text="Variable (wrt):", font=("Arial", 10, "bold")).pack(pady=(10, 0))
var_entry = tk.Entry(root, width=10, font=("Consolas", 12), justify="center")
var_entry.pack(pady=5)
var_entry.insert(0, "x")

calc_button = tk.Button(root, text="Integrate", command=calculate_integral, bg="#1976d2", fg="white", font=("Arial", 10, "bold"))
calc_button.pack(pady=15)

result_label = tk.Label(root, text="", font=("Consolas", 11, "bold"), wraplength=400, fg="#2e7d32")
result_label.pack(pady=20)

root.mainloop()