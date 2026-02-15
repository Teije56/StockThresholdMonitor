# Stock Monitor that tracks up to 5 stocks prices and sets a threshhold price that notifies the user when the stock is bellow the threshold.
# Small personal project to experiment with APIs  and Tkinter
# Upgraded from my old PowerShell script which could only track on stock at a time.

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import requests
import ctypes
import time

import os
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
MIN_BETWEEN_CHECKS = 60  # Time in minutes between stock updates
START_TIME = datetime.now()
TIMEOUT_HOURS = 5 # Sets the timout for when the script with end currently set to 5 as there is a maxium of 25 api calls per day

#Code for managing the addition of a stock to the table
def add_stock():
    code = code_entry.get().upper().strip()
    price_val = price_entry.get().strip()
    
    if code and price_val:
        if len(tree.get_children()) < 5:
            tree.insert("", "end", values=(code, f"${price_val}", "Pending...", "-"))
            code_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Note", "Maximum 5 stocks reached.")
    else:
        messagebox.showwarning("Input Error", "Please enter both a Stock Code and a Price.")

def remove_stock():
    selected = tree.selection()
    if selected:
        for item in selected:
            tree.delete(item)

def update_stock_logic():
    # Checks if the script has exceeded its run time
    elapsed = datetime.now() - START_TIME
    if elapsed > timedelta(hours=TIMEOUT_HOURS):
        print(f"{TIMEOUT_HOURS}-hour runtime limit reached. Closing.")
        root.destroy()
        return

    # Loop through all the stocks
    for item in tree.get_children():
        values = tree.item(item, 'values')
        symbol = values[0]
        try:
            target_price = float(values[1].replace('$', ''))
        except ValueError: continue
        
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        
        try:
            response = requests.get(url, timeout=10).json()
            if "Global Quote" in response and "05. price" in response["Global Quote"]:
                current_price = float(response["Global Quote"]["05. price"])
                prev_price = values[2] # Move current to previous

                # Update Grid row
                tree.item(item, values=(symbol, f"${target_price:.2f}", f"${current_price:.2f}", prev_price))
                
                # Alert user if threshold is meet
                if current_price <= target_price:
                    ctypes.windll.user32.MessageBoxW(0, f"{symbol} hit {current_price}!", "Stock Alert", 48)
            else:
                # Handle API rate limits and 
                tree.item(item, values=(symbol, f"${target_price:.2f}", "API Limit", values[2]))
        except Exception:
            tree.item(item, values=(symbol, f"${target_price:.2f}", "Conn Error", values[2]))
        
        # Small stagger delay between api calls to precent api spamming
        root.update()
        time.sleep(0.5)

    #Waits a set time in minutes before updating the stocks this prevents exceeding the api call limit
    root.after(MIN_BETWEEN_CHECKS * 60*1000, update_stock_logic)

# UI setup and configuration
root = tk.Tk()
root.title("Stock Monitor")
root.geometry("550x500")
root.configure(bg="white")

# Header formatte
tk.Label(root, text="STOCK WATCHLIST", font=("Arial", 9, "bold"), bg="white", fg="#888").pack(pady=(20, 10))

# Input Area
input_frame = tk.Frame(root, bg="white")
input_frame.pack(pady=10)

# Labels for the inputs
tk.Label(input_frame, text="Stock Code (e.g. AAPL)", font=("Arial", 8), bg="white", fg="#888").grid(row=0, column=0, sticky="w", padx=5)
tk.Label(input_frame, text="Threshold Price (USD)", font=("Arial", 8), bg="white", fg="#888").grid(row=0, column=1, sticky="w", padx=5)

# Formatte the entry boxes
code_entry = tk.Entry(input_frame, width=15, font=("Arial", 10), bd=0, highlightthickness=1, highlightbackground="#eee")
code_entry.grid(row=1, column=0, padx=5, pady=5)

price_entry = tk.Entry(input_frame, width=15, font=("Arial", 10), bd=0, highlightthickness=1, highlightbackground="#eee")
price_entry.grid(row=1, column=1, padx=5, pady=5)

# Code to formatte the add stock button
tk.Button(root, text="ADD TO LIST", command=add_stock, font=("Arial", 7, "bold"), 
          bg="#f9f9f9", fg="#444", relief="flat", padx=15, pady=5, cursor="hand2").pack(pady=5)

# Excel Grid formating
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", fieldbackground="white", rowheight=35, font=("Arial", 10))
style.configure("Treeview.Heading", background="#f9f9f9", font=("Arial", 8, "bold"), foreground="#666", relief="flat")
style.map("Treeview", background=[('selected', '#e1f5fe')], foreground=[('selected', 'black')])

tree = ttk.Treeview(root, columns=("code", "threshold", "curr", "prev"), show="headings", height=5)
tree.heading("code", text="STOCK")
tree.heading("threshold", text="THRESHOLD PRICE")
tree.heading("curr", text="CURRENT PRICE")
tree.heading("prev", text="PREVIOUS PRICE")

for col in ("code", "threshold", "curr", "prev"):
    tree.column(col, width=120, anchor="center")
tree.pack(pady=20, padx=20)

# The delete stock button controls
remove_btn = tk.Button(root, text="remove selected row", command=remove_stock, 
                       font=("Arial", 8), bg="white", fg="#ccc", bd=0, cursor="hand2")
remove_btn.pack()

# Wait 30 seconds before the very first API check 
# This gives the user time to enter their stocks
root.after(30000, update_stock_logic)

root.mainloop()