import tkinter as tk

# -----------------------------
# Calculator Functions
# -----------------------------
def on_click(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + value)

def clear():
    entry.delete(0, tk.END)

def calculate():
    try:
        expression = entry.get()
        result = str(eval(expression))
        entry.delete(0, tk.END)
        entry.insert(0, result)
    except ZeroDivisionError:
        entry.delete(0, tk.END)
        entry.insert(0, "Error (÷0)")
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# -----------------------------
# Window Setup
# -----------------------------
root = tk.Tk()
root.title("Calculator")
root.geometry("400x500")
root.resizable(False, False)

entry = tk.Entry(root, font=("Arial", 20), borderwidth=4, relief="ridge", justify="right")
entry.pack(fill="both", padx=10, pady=10, ipady=10)

# -----------------------------
# Button Layout
# -----------------------------
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
]

frame = tk.Frame(root)
frame.pack()

for (text, row, col) in buttons:
    if text == "=":
        btn = tk.Button(frame, text=text, font=("Arial", 18), width=5, height=2,
                        bg="#4CAF50", fg="white", command=calculate)
    else:
        btn = tk.Button(frame, text=text, font=("Arial", 18), width=5, height=2,
                        command=lambda t=text: on_click(t))
    btn.grid(row=row, column=col, padx=3, pady=3)

clear_btn = tk.Button(root, text="CLEAR", font=("Arial", 18), width=23, height=1,
                      bg="#f44336", fg="white", command=clear)
clear_btn.pack(pady=5)

root.mainloop()
