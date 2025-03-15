import tkinter as tk
import random
import datetime
import math
from tkinter import scrolledtext

# Symbols for heads, tails, and coin flip
HEADS_SYMBOL = "₿" 
TAILS_SYMBOL ="🏚"  
COIN_SYMBOL = "🟡"

# Global variables
flip_history = []
flip_count = 0

# Function to flip the coin
def flip_coin():
    global flip_count
    flip_count += 1
    result = random.choice(["Heads", "Tails"])
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flip_history.append(f"Flip #{flip_count}: {result} ({timestamp})")
    
    # Update GUI
    if result == "Heads":
        coin_label.config(text=HEADS_SYMBOL)
    else:
        coin_label.config(text=TAILS_SYMBOL)
    result_label.config(text=result)
    count_label.config(text=f"Flip #{flip_count}")
    
    # Update statistics
    update_statistics()
    
    # Update the history display
    update_history_display()
    
    # Check if coin is fair when we have enough flips
    check_fairness()

# Function to update statistics
def update_statistics():
    heads_count = sum(1 for flip in flip_history if "Heads" in flip)
    tails_count = sum(1 for flip in flip_history if "Tails" in flip)
    
    if flip_count > 0:
        heads_label.config(text=f"{HEADS_SYMBOL} Heads: {heads_count} ({(heads_count/flip_count)*100:.1f}%)")
        tails_label.config(text=f"{TAILS_SYMBOL} Tails: {tails_count} ({(tails_count/flip_count)*100:.1f}%)")

# Function to update the history display
def update_history_display():
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)
    for entry in flip_history[-20:]:  # Show only the latest 20 flips to avoid clutter
        history_text.insert(tk.END, f"{entry}\n")
    history_text.config(state=tk.DISABLED)
    history_text.see(tk.END)  # Scroll to the end

# Function to check if the coin is fair
def check_fairness():
    if flip_count < 10:
        fairness_label.config(text="Need at least 10 flips to check fairness", fg="black")
        return
    
    heads_count = sum(1 for flip in flip_history if "Heads" in flip)
    expected = flip_count / 2
    
    # Chi-square test for fairness
    chi_square = ((heads_count - expected) ** 2) / expected + ((flip_count - heads_count - expected) ** 2) / expected
    
    # Critical value for chi-square with 1 degree of freedom at 95% confidence level is 3.84
    if chi_square < 3.84:
        fairness_label.config(text=f"Coin appears fair (Chi² = {chi_square:.2f})", fg="green")
    else:
        fairness_label.config(text=f"Coin may be biased (Chi² = {chi_square:.2f})", fg="red")

# Function to export results to tossresult.md
def export_results():
    with open("tossresult.md", "w", encoding="utf-8") as file:
        file.write("# Virtual Coin Toss Results\n\n")
        file.write(f"## Summary\n")
        heads_count = sum(1 for flip in flip_history if "Heads" in flip)
        tails_count = sum(1 for flip in flip_history if "Tails" in flip)
        
        file.write(f"- Total flips: {flip_count}\n")
        if flip_count > 0:
            file.write(f"- Heads: {heads_count} ({(heads_count/flip_count)*100:.1f}%)\n")
            file.write(f"- Tails: {tails_count} ({(tails_count/flip_count)*100:.1f}%)\n")
        
        file.write(f"\n## Complete History\n\n")
        for entry in flip_history:
            file.write(f"- {entry}\n")
    export_label.config(text="Results exported to TossResult.md")

# Function to reset the game
def reset_game():
    global flip_history, flip_count
    flip_history = []
    flip_count = 0
    coin_label.config(text=COIN_SYMBOL)
    result_label.config(text="Waiting for results...")
    count_label.config(text="")
    heads_label.config(text=f"{HEADS_SYMBOL} Heads: 0 (0%)")
    tails_label.config(text=f"{TAILS_SYMBOL} Tails: 0 (0%)")
    export_label.config(text="")
    fairness_label.config(text="")
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)
    history_text.config(state=tk.DISABLED)

# Create GUI window
root = tk.Tk()
root.title("Virtual Coin Toss")
root.geometry("500x650")
root.resizable(False, False)

# Create tabs
tab_control = tk.Frame(root)
tab_control.pack(fill="both", expand=True)

# Main frame
main_frame = tk.Frame(tab_control)
main_frame.pack(fill="both", expand=True, padx=10, pady=5)

# Heading
tk.Label(main_frame, text="Virtual Coin Toss", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(main_frame, text="Click the button to flip!", font=("Arial", 12)).pack()

# Coin display
coin_label = tk.Label(main_frame, text=COIN_SYMBOL, font=("Arial", 40))
coin_label.pack(pady=15)

# Flip result display
result_label = tk.Label(main_frame, text="Waiting for results...", font=("Arial", 14, "bold"))
result_label.pack()
count_label = tk.Label(main_frame, text="", font=("Arial", 12))
count_label.pack()

# Statistics display
stats_frame = tk.Frame(main_frame)
stats_frame.pack(pady=10, fill="x")

heads_label = tk.Label(stats_frame, text=f"{HEADS_SYMBOL} Heads: 0 (0%)", font=("Arial", 12))
heads_label.pack(side=tk.LEFT, padx=20)

tails_label = tk.Label(stats_frame, text=f"{TAILS_SYMBOL} Tails: 0 (0%)", font=("Arial", 12))
tails_label.pack(side=tk.RIGHT, padx=20)

# Fairness indicator
fairness_label = tk.Label(main_frame, text="", font=("Arial", 11, "italic"))
fairness_label.pack(pady=5)

# History area
tk.Label(main_frame, text="Recent Flip History", font=("Arial", 12, "bold")).pack(pady=(10, 5))
history_text = scrolledtext.ScrolledText(main_frame, width=50, height=10, wrap=tk.WORD)
history_text.pack(padx=10, pady=5)
history_text.config(state=tk.DISABLED)

# Buttons frame
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

flip_button = tk.Button(button_frame, text="Flip Coin", command=flip_coin, font=("Arial", 12), width=12)
flip_button.pack(side=tk.LEFT, padx=5)

reset_button = tk.Button(button_frame, text="Reset", command=reset_game, font=("Arial", 12), width=12)
reset_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(button_frame, text="Export", command=export_results, font=("Arial", 12), width=12)
export_button.pack(side=tk.LEFT, padx=5)

# Export result message
export_label = tk.Label(main_frame, text="", font=("Arial", 10, "italic"), fg="green")
export_label.pack()

# Run the GUI
root.mainloop()