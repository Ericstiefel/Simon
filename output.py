import tkinter as tk
from tkinter import ttk

def show_popup():
    popup = tk.Toplevel()
    popup.title("Stock Data")

    tree = ttk.Treeview(popup, columns=("Ticker", "Metric"), show="headings")
    
    # Define column headers
    tree.heading("Ticker", text="Ticker")
    tree.heading("Metric", text="Metric")
    
    # Adjust column width
    tree.column("Ticker", width=100, anchor="center")
    tree.column("Metric", width=100, anchor="center")

    # Insert data into the table
    for _, ticker, metric in data:
        tree.insert("", "end", values=(ticker, f"{metric:.2f}"))

    tree.pack(expand=True, fill="both")

data = [
    ("Apple Inc.", "AAPL", 150.25),
    ("Microsoft Corp.", "MSFT", 302.50),
    ("Tesla Inc.", "TSLA", 700.10)
]

root = tk.Tk()
root.withdraw()
show_popup()
root.mainloop()
