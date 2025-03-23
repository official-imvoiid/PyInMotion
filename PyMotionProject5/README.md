# Text Reverser

A Python-based text manipulation application that reverses characters or words with both command-line and graphical user interfaces.

## Features

- **Dual Reversal Options**: Reverse text by character or by word order.
- **Simple GUI**: Built with Tkinter for an easy-to-use interface.
- **Command-Line Interface**: Alternative text-based interface when GUI is unavailable.
- **Error Handling**: Gracefully handles empty inputs and special characters.
- **Save Functionality**: Exports reversed text to a file of your choice.
- **Fallback Mechanism**: Automatically switches to CLI if GUI components cannot load.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/official-imvoiid/PyInMotion.git
   cd PyInMotion
   cd PyMotionProject5
   ```

2. **Install dependencies** (if not already installed):
   ```sh
   pip install tk
   ```

3. **Run the application**:
   ```sh
   python TextReverser.py
   ```

## Usage

### GUI Mode
1. Enter text in the input box.
2. Click **"Reverse Characters"** to flip the character order of your text.
3. Click **"Reverse Words"** to maintain character order but reverse word sequence.
4. View the result in the output box.
5. Click **"Save to File"** to export your reversed text.

### CLI Mode
1. Choose an option from the menu (1-4).
2. Enter text when prompted.
3. View the reversed output.
4. Optionally save results to a file.

## Learning Outcomes

This project demonstrates:
- String manipulation in Python
- Working with lists and array methods
- Creating interactive user interfaces
- Implementing error handling
- File I/O operations

## Project Structure

- **TextReverser.py** → Main script with both GUI and CLI implementations
- **reverse_characters()** → Function to reverse character order
- **reverse_words()** → Function to reverse word order
- **save_to_file()** → Function to export results

## Tips for Success

- Use Python's slicing feature (`[::-1]`) to efficiently reverse text
- Work with `split()` and `join()` functions to reverse word order effectively
- Test with different inputs, including single words, full sentences, and special characters

## License

This project is open-source under the [MIT License](LICENSE).