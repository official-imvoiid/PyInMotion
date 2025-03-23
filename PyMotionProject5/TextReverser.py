def reverse_characters(text):
    """Reverse the characters in a string."""
    if not text:
        return "Error: Empty string provided."
    return text[::-1]

def reverse_words(text):
    """Reverse the order of words while maintaining their original spelling."""
    if not text:
        return "Error: Empty string provided."
    words = text.split()
    if not words:
        return "Error: No words found."
    return " ".join(words[::-1])

def save_to_file(text):
    """Save the reversed text to a file."""
    try:
        filename = input("Enter filename to save (e.g., reversed.txt): ")
        with open(filename, 'w') as file:
            file.write(text)
        return f"Text successfully saved to {filename}"
    except Exception as e:
        return f"Error saving to file: {str(e)}"

def text_reverser_cli():
    """Command-line interface for the Text Reverser program."""
    print("\n" + "="*50)
    print("Welcome to Text Reverser".center(50))
    print("="*50)
    
    while True:
        print("\nMenu Options:")
        print("1. Reverse Character Order")
        print("2. Reverse Word Order")
        print("3. Save Last Result to File")
        print("4. Exit Program")
        
        last_result = ""
        
        try:
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                text = input("\nEnter text to reverse characters: ")
                if not text.strip():
                    print("Warning: Empty string provided. Please enter valid text.")
                    continue
                result = reverse_characters(text)
                print("\nReversed characters:", result)
                last_result = result
                
            elif choice == '2':
                text = input("\nEnter text to reverse words: ")
                if not text.strip():
                    print("Warning: Empty string provided. Please enter valid text.")
                    continue
                result = reverse_words(text)
                print("\nReversed words:", result)
                last_result = result
                
            elif choice == '3':
                if not last_result:
                    print("No reversed text available to save. Please reverse some text first.")
                else:
                    result = save_to_file(last_result)
                    print(result)
                    
            elif choice == '4':
                print("\nThank you for using Text Reverser. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again.")

# GUI implementation using tkinter
def create_gui():
    """Create a GUI for the Text Reverser program using tkinter."""
    try:
        import tkinter as tk
        from tkinter import messagebox, filedialog
        
        def reverse_chars_action():
            text = input_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Warning", "Please enter some text.")
                return
            result = reverse_characters(text)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, result)
        
        def reverse_words_action():
            text = input_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Warning", "Please enter some text.")
                return
            result = reverse_words(text)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, result)
        
        def save_action():
            result = output_text.get("1.0", tk.END).strip()
            if not result:
                messagebox.showwarning("Warning", "No reversed text to save.")
                return
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, 'w') as file:
                        file.write(result)
                    messagebox.showinfo("Success", f"Text saved to {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        
        # Create the main window
        root = tk.Tk()
        root.title("Text Reverser")
        root.geometry("600x400")
        
        # Create and place widgets
        tk.Label(root, text="Enter text to reverse:", font=("Arial", 12)).pack(pady=5)
        
        input_text = tk.Text(root, height=5, width=60)
        input_text.pack(pady=5)
        
        # Frame for buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        reverse_chars_btn = tk.Button(button_frame, text="Reverse Characters", command=reverse_chars_action, width=15)
        reverse_chars_btn.grid(row=0, column=0, padx=5)
        
        reverse_words_btn = tk.Button(button_frame, text="Reverse Words", command=reverse_words_action, width=15)
        reverse_words_btn.grid(row=0, column=1, padx=5)
        
        save_btn = tk.Button(button_frame, text="Save to File", command=save_action, width=15)
        save_btn.grid(row=0, column=2, padx=5)
        
        tk.Label(root, text="Reversed text:", font=("Arial", 12)).pack(pady=5)
        
        output_text = tk.Text(root, height=5, width=60)
        output_text.pack(pady=5)
        
        # Start the GUI
        root.mainloop()
        
    except ImportError:
        print("Tkinter module not found. Running command-line version instead.")
        text_reverser_cli()

if __name__ == "__main__":
    try:
        # Try to use GUI version first
        create_gui()
    except Exception as e:
        print(f"Error starting GUI: {str(e)}")
        print("Falling back to command line interface.")
        text_reverser_cli()