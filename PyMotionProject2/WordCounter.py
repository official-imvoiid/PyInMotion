import tkinter as tk
from tkinter import filedialog, messagebox
import re

def count_words(text):
    """Counts words in the given text and returns word count and frequency."""
    words = re.findall(r'\b\w+\b', text.lower())  # Extract words ignoring punctuation
    word_count = len(words)
    word_freq = {}
    
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    return word_count, word_freq

def process_text():
    """Handles text input from the user and displays word count."""
    text = text_input.get("1.0", tk.END).strip()
    
    if not text:
        messagebox.showerror("Error", "Please enter some text.")
        return
    
    word_count, word_freq = count_words(text)
    output_label.config(text=f"Total Words: {word_count}")
    
    # Display top 5 most frequent words
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    freq_text = "\n".join([f"{word}: {count}" for word, count in sorted_words])
    freq_label.config(text=f"Top 5 Words:\n{freq_text}")

def load_file():
    """Loads text from a selected file."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    
    if not file_path:
        return
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, text)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")

# GUI Setup
root = tk.Tk()
root.title("Advanced Word Counter")
root.geometry("500x400")

# Widgets
tk.Label(root, text="Enter Text or Load a File:", font=("Arial", 12)).pack(pady=5)
text_input = tk.Text(root, height=5, width=50)
text_input.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Count Words", command=process_text).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Load File", command=load_file).grid(row=0, column=1, padx=5)

output_label = tk.Label(root, text="Total Words: 0", font=("Arial", 12, "bold"))
output_label.pack(pady=5)

freq_label = tk.Label(root, text="", font=("Arial", 10))
freq_label.pack(pady=5)

# Run the application
root.mainloop()
