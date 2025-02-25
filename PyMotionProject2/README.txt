
---

# **Word Counter**  

A simple Python GUI application that counts words in user-inputted text or from a loaded file.  

## **Project Overview**  

This project was developed as part of a Python Programming Internship to strengthen Python programming concepts such as input handling, string manipulation, function creation, and basic control flow. The application provides an interactive way to count words and display their frequency.  

## **Features**  

- **User Input:** Allows users to enter text manually or load a file for processing.  
- **Word Counting Logic:** Implements a function to count words efficiently.  
- **Output Display:** Shows the total word count and the most frequently used words.  
- **Error Handling:** Alerts the user if no text is entered.  
- **User-Friendly Interface:** Simple GUI built with Tkinter for easy interaction.  

## **Requirements**  

- Python 3.x  
- Tkinter (built into Python)  
- Regular Expressions (`re` module)  

## **Installation & Usage**  

1. Clone or download this repository.  
2. Run the script:  
   ```bash
   python WordCounter.py
   ```
3. Enter text or load a `.txt` file to analyze word count.  

## **Code Structure**  

- **`count_words(text)`** → Processes and counts words.  
- **`process_text()`** → Handles user input and updates the GUI.  
- **`load_file()`** → Loads text from a file into the input box.  
- **GUI Setup** → Built with Tkinter for ease of use.  

---
