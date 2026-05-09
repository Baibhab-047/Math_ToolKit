import tkinter as tk
from tkinter import messagebox
import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication, convert_xor

transformations = (standard_transformations + (implicit_multiplication, convert_xor))

def solve_logic():
    equation_str = eq_entry.get()
    var_str = var_entry.get()
    
    if not equation_str or not var_str:
        messagebox.showwarning("Input Error", "Please fill in both fields.")
        return

    try:
        if '=' not in equation_str:
            raise ValueError("Equation must contain an '=' sign.")
        
        left_str, right_str = equation_str.split('=')
        left_expr = parse_expr(left_str.strip(), transformations=transformations)
        right_expr = parse_expr(right_str.strip(), transformations=transformations)
        
        variable = sympy.symbols(var_str.strip())
        solutions = sympy.solve(sympy.Eq(left_expr, right_expr), variable)
        
        if solutions:
            res = solutions[0].evalf(4)
            str_res=str(res).replace('I', 'i')
            result_label.config(text=f"Solution: {str_res}", fg="#cc2e2e")
        else:
            result_label.config(text="No solution found.", fg="#e13ce7")
            
    except Exception as e:
        messagebox.showerror("Math Error", str(e))

root = tk.Tk()
root.title("Equation Solver")
root.geometry("450x350")

tk.Label(root, text="Equation:", font=("Arial", 10, "bold")).pack(pady=(20, 0))
eq_entry = tk.Entry(root, width=40, font=("Consolas", 12))
eq_entry.pack(pady=5)
eq_entry.insert(0, "x**2 + 2x = 8")

tk.Label(root, text="Variable:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
var_entry = tk.Entry(root, width=10, font=("Consolas", 12))
var_entry.pack(pady=5)
var_entry.insert(0, "x")

solve_btn = tk.Button(root, text="SOLVE", command=solve_logic, bg="#3f34db", fg="white", font=("Arial", 10, "bold"), width=15)
solve_btn.pack(pady=20)

result_label = tk.Label(root, text="Solution: --", font=("Consolas", 12, "bold"))
result_label.pack(pady=10)

root.mainloop()