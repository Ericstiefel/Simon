import tkinter as tk
from tkinter import messagebox

def run_simulation():
    try:
        yield_value = float(yield_entry.get())  # Get and convert input to float
        risk_value = float(risk_entry.get())
        email = email_entry.get().strip()
        sendByEmail = send.get()  # Boolean value from checkbox
        
        print(f"Running simulation with Yield: {yield_value}, Risk: {risk_value}")
        
        if email and "@" not in email:
            messagebox.showwarning("Warning", "Please enter a valid email.")
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Create the main window
root = tk.Tk()
root.title("Investment Simulation")
root.geometry("400x350")  
root.configure(bg="white")

# Title Label
title_label = tk.Label(root, text="Adjust Parameters", font=("Arial", 14, "bold"), bg="white")
title_label.pack(pady=10)

# Yield Entry
yield_label = tk.Label(root, text="Yield", font=("Arial", 12), bg="white")
yield_label.pack()
yield_entry = tk.Entry(root, font=("Arial", 12), width=10)
yield_entry.insert(0, "10")  # Preset Yield value to 10
yield_entry.pack()

# Risk Entry
risk_label = tk.Label(root, text="Risk", font=("Arial", 12), bg="white")
risk_label.pack()
risk_entry = tk.Entry(root, font=("Arial", 12), width=10)
risk_entry.insert(0, "4")  # Preset Risk value to 4
risk_entry.pack()

# Email Entry
email_label = tk.Label(root, text="Email", font=("Arial", 12), bg="white")
email_label.pack()
email_entry = tk.Entry(root, font=("Arial", 12), width=35)
email_entry.insert(0, 'ERIC.STIEFEL@BARUCHMAIL.CUNY.EDU')
email_entry.pack()

# Subscribe Checkbox
send = tk.BooleanVar()  # Holds True/False
send_entry = tk.Checkbutton(root, text="Send By Email", font=("Arial", 12), bg="white", variable=send)
send_entry.pack(pady=5)

# Run Button
run_button = tk.Button(root, text="Run", font=("Arial", 14, "bold"), bg="green", fg="white", command=run_simulation)
run_button.pack(pady=20)

# Run the GUI
root.mainloop()
