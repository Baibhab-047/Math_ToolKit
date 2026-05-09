import tkinter as tk
from tkinter import messagebox
import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication, convert_xor

transformations = (standard_transformations + (implicit_multiplication, convert_xor))

def calculate_derivative():
    expr_input = eq_entry.get().strip()
    var_input = var_entry.get().strip()
    order_input = order_entry.get().strip()
    
    if not expr_input or not var_input:
        messagebox.showwarning("Input Error", "Please provide an expression and a variable.")
        return

    try:
        expr = parse_expr(expr_input, transformations=transformations)
        variable = sympy.symbols(var_input)
        order = int(order_input) if order_input.isdigit() else 1
        
        derivative = sympy.diff(expr, variable, order)
        final_res = sympy.simplify(derivative)
        finale=str(final_res).replace('**', '^').replace('*', '')
        
        result_label.config(text=f"d/d{var_input}: {finale}", fg="#2e7d32")
            
    except Exception as e:
        messagebox.showerror("Math Error", str(e))

root = tk.Tk()
root.title("Differentiation Tool")
root.geometry("450x400")

tk.Label(root, text="Function:", font=("Arial", 10, "bold")).pack(pady=(20, 0))
eq_entry = tk.Entry(root, width=40, font=("Consolas", 12), justify="center")
eq_entry.pack(pady=5)
eq_entry.insert(0, "3x^3 + 5x + 2")

tk.Label(root, text="Variable (wrt):", font=("Arial", 10, "bold")).pack(pady=(10, 0))
var_entry = tk.Entry(root, width=10, font=("Consolas", 12), justify="center")
var_entry.pack(pady=5)
var_entry.insert(0, "x")

tk.Label(root, text="Order:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
order_entry = tk.Entry(root, width=10, font=("Consolas", 12), justify="center")
order_entry.pack(pady=5)
order_entry.insert(0, "1")

diff_btn = tk.Button(root, text="DIFFERENTIATE", command=calculate_derivative, bg="#2e7d32", fg="white", font=("Arial", 10, "bold"), width=15)
diff_btn.pack(pady=20)

result_label = tk.Label(root, text="Result: --", font=("Consolas", 12, "bold"), wraplength=400)
result_label.pack(pady=10)

root.mainloop()